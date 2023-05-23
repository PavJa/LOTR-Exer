import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns # creating the heatmap
import matplotlib.pyplot as plt # data visualization
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve
from sklearn.metrics import classification_report
import time
start_time = time.time()

data_Books = 'BX-Books.csv'
data_Users = 'BX-Users.csv'
data_Ratings = 'BX-Book-Ratings.csv'

pd.set_option('display.max_columns', 4)
pd.set_option('max_colwidth', None)
pd.options.display.max_colwidth = 43

df_Books = pd.read_csv(data_Books, dtype = 'str', sep=';', encoding='latin-1', on_bad_lines='skip')
df_Books_NL = df_Books.drop(['Image-URL-S', 'Image-URL-M','Image-URL-L'], axis=1)
# I wanted to raise warnings to
df_Users = pd.read_csv(data_Users, dtype = 'str', sep=';', encoding='latin-1', on_bad_lines='skip')
#print(df_Users.columns)
df_Ratings = pd.read_csv(data_Ratings, dtype = 'str', sep=';', encoding='latin-1', on_bad_lines='skip')
df_Ratings.groupby(['User-ID'])
#print(df_Ratings.head)
#print(df_Books.shape)
#print(df_Users.shape)
#print(df_Ratings.shape)
# print(df_Users.loc[318]) #testing some suspicious data points

#print(df_Users.head()) # I was just checking how the data were presented in the table

df_UsersRate = df_Ratings.merge(df_Users, on='User-ID', how = 'left')
df_BooksUsersRate = df_UsersRate.merge(df_Books_NL, on='ISBN', how = 'left')
df_BooksUsersRate.style.set_properties(**{'Book-Title-align': 'left'})
#print(df_BooksUsersRate.shape)
#print(df_BooksUsersRate['Location'].to_string())

# check what lines cause problems on_bad_lines='warn'

#print(df.shape)
#print(df_BooksUsersRate.loc[318])

NaN_Columns = df_BooksUsersRate.columns[df_BooksUsersRate.isna().any()].tolist() # check null values, obviously they are
# print(NaN_Columns) # gives me columns with null values, publisher is important information but not a selection criterion
# age and book author might be important in constructing selection criteria

df_BooksUsersRate['Age'] = df_BooksUsersRate['Age'].fillna(0)
df_BooksUsersRate['Book-Author'] = df_BooksUsersRate['Book-Author'].fillna('Missing')
df_BooksUsersRate['Publisher'] = df_BooksUsersRate['Publisher'].fillna('Missing')
df_BooksUsersRate['Book-Title'] = df_BooksUsersRate['Book-Title'].fillna('Missing')
#print(df_BooksUsersRate.isnull().values.any()) # just checking we have no NaN values


# Below are the quick examples

# Example 1: convert lowercase column using str.lower()
df_BooksUsersRate['Book-Title']= df_BooksUsersRate['Book-Title'].str.lower()
#df_BooksUsersRate['Book-Title']= df_BooksUsersRate['Book-Title'].str.replace(' ','')


df_BooksUsersRate['Book-Title'] = df_BooksUsersRate['Book-Title'].str.replace(r"\(.*\)",'')
df_BooksUsersRate['Book-Title'] = df_BooksUsersRate['Book-Title'].str.replace(r",",'')
df_BooksUsersRate['Book-Title'] = df_BooksUsersRate['Book-Title'].str.replace(r":",'')


#print(df_BooksUsersRate['Book-Title'].to_string())

# create basic categories



Author = df_BooksUsersRate['Book-Author']
Title = df_BooksUsersRate['Book-Title'].astype('str')
Location = df_BooksUsersRate['Location']
Rating = df_BooksUsersRate['Book-Rating'].astype('int')
User_ID = df_BooksUsersRate['User-ID']
#print(Author)



# key word search
#Tolkien_list = [y for x,y,z in zip(Author,Title,Location) if (x == 'J. R. R. Tolkien' and ('usa' or 'united kingdom' or
                                                                #                           'canada' or 'australia' or
                                                               #                            'new zealand') in z and
                                                              #('lord of the rings' or 'two towers' or
                                                             #  'the return of the king' or 'the fellowship of the ring')
                                                             # not in y)]
#new_Tolkien_list = list(set(Tolkien_list)) #remove duplicates by changing list to a set and back
#new_Tolkien_list.remove('Farmer Giles of Ham: Aegidii Ahenobarbi Julii Agricole De Hammo Domini De Domito Aule '
                        #'Draconarie Comitis Regni Minimi Regis Et Basilei Mira Facinora')
#print(new_Tolkien_list)

# problems:  Tolkien wrote other things than Lord of The Rings, so this recommendation is flawed since it can recommend
# something the reader will not like

# similar rating - far streched assumption that this is our reference class (we know nothing about our stakeholder). For
#z>7 it was fairly small. Plus what does enjoy mean numerically?

Tolkien_list_rating = [x for x,y,z in zip(User_ID,Title,Rating) if ('the lord of the rings' in y and z>=8)]

df_BooksUsersRate['Book-Rating'] = df_BooksUsersRate['Book-Rating'].astype('int')

print(len(Tolkien_list_rating))


list_Similar_Rate = []

for x in Tolkien_list_rating:
    k = df_BooksUsersRate.loc[(df_BooksUsersRate['User-ID'] == x) & (df_BooksUsersRate['Book-Rating'] >= 7)]
    k_rate_book = k[['Book-Title', 'Book-Rating', 'Age']]
    list_Similar_Rate.append(k_rate_book)

df_union = pd.concat(list_Similar_Rate)

df_union['Book-Title'] = df_union['Book-Title'].str.strip()
#df_union['Book-Title'] = df_union.style.set_properties(**{'Book-Title-align': 'right'})


#df_union_grouped_count = df_union.groupby(['Book-Title'],sort=False)['Book-Title'].count().
# sort_values(ascending=False).reset_index(name="Count")

#
df_union['Age'] = df_union['Age'].astype('int')
df_union['Book-Title'] = df_union['Book-Title'].str.\
    replace('the hobbit  the enchanting prelude to the lord of the rings', 'the hobbit') # post result adjustemnt
df_union['Book-Title'] = df_union['Book-Title'].str.\
    replace('the return of the king', 'the lord of the rings')
df_union['Book-Title'] = df_union['Book-Title'].str.\
    replace('the fellowship of the ring', 'the lord of the rings')
df_union['Book-Title'] = df_union['Book-Title'].str.\
    replace('the two towers', 'the lord of the rings')


df_union_grouped_count = df_union.groupby(['Book-Title'],sort=False).agg(Count=('Book-Title', 'count'),
                                                                         Mean_Rating=('Book-Rating', 'mean'),
                                                                         Median_Age=('Age', 'median'))\
    .sort_values(by=['Count','Mean_Rating'],ascending=[False,False]).reset_index()



df_union_grouped_count = df_union_grouped_count[df_union_grouped_count['Count'] >= 20]
df_union_grouped_count.Mean_Rating=df_union_grouped_count.Mean_Rating.round(2)
df_union_grouped_count.Median_Age=df_union_grouped_count.Median_Age.round(0).astype('int')
df_union_grouped_count = df_union_grouped_count.iloc[1:]



print("--- %s seconds ---" % (time.time() - start_time))

print(df_union_grouped_count.to_string())

#print(df_union_grouped_mean)

