import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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

# convert lowercase column using str.lower()
df_BooksUsersRate['Book-Title']= df_BooksUsersRate['Book-Title'].str.lower()
#df_BooksUsersRate['Book-Title']= df_BooksUsersRate['Book-Title'].str.replace(' ','')

df_BooksUsersRate['Book-Title'] = df_BooksUsersRate['Book-Title'].str.replace(r"\(.*\)",'')
df_BooksUsersRate['Book-Title'] = df_BooksUsersRate['Book-Title'].str.replace(r",",'')
df_BooksUsersRate['Book-Title'] = df_BooksUsersRate['Book-Title'].str.replace(r":",'')
df_BooksUsersRate['Book-Title'] = df_BooksUsersRate['Book-Title'].str.strip()

Author = df_BooksUsersRate['Book-Author']
#Title = df_BooksUsersRate['Book-Title'].astype('str')
df_BooksUsersRate['Book-Title'] = df_BooksUsersRate['Book-Title'].astype('str')
#Location = df_BooksUsersRate['Location']
df_BooksUsersRate['Book-Rating'] = df_BooksUsersRate['Book-Rating'].astype('int')
#User_ID = df_BooksUsersRate['User-ID']

df_union['Age'] = df_union['Age'].astype('int')
df_union['Book-Title'] = df_union['Book-Title'].str.\
    replace('the hobbit  the enchanting prelude to the lord of the rings', 'the hobbit') # post result adjustemnt
df_union['Book-Title'] = df_union['Book-Title'].str.\
    replace('the return of the king', 'the lord of the rings')
df_union['Book-Title'] = df_union['Book-Title'].str.\
    replace('the fellowship of the ring', 'the lord of the rings')
df_union['Book-Title'] = df_union['Book-Title'].str.\
    replace('the two towers', 'the lord of the rings')



#print(df_BooksUsersRate['Book-Title'].to_string())

# create basic categories


#print(Author)

# similar rating - far streched assumption that this is our reference class (we know nothing about our stakeholder). For
#z>7 it was fairly small. Plus what does enjoy mean numerically?

# Create a list of people (user-ID) that have read the lord of the rings



Tolkien_list_rating = [x for x,y,z in zip(df_BooksUsersRate['User-ID'],df_BooksUsersRate['Book-Title'],
                                          df_BooksUsersRate['Book-Rating']) if ('the lord of the rings' in y and z>=7)]

#print(len(Tolkien_list_rating))

count_check = []
for i in df_BooksUsersRate['Book-Title']:
    if 'the lord of the rings' in i:
        count_check.append(i)

print(len(count_check))

df_BooksUsersRate['Book-Rating'] = df_BooksUsersRate['Book-Rating'].astype('int')



list_Similar_Rate = []

for x in Tolkien_list_rating:
    k = df_BooksUsersRate.loc[(df_BooksUsersRate['User-ID'] == x) & (df_BooksUsersRate['Book-Rating'] >= 7)]
    k_rate_book = k[['Book-Title', 'Book-Rating', 'Age']]
    list_Similar_Rate.append(k_rate_book)

df_union = pd.concat(list_Similar_Rate)



#df_union['Age'] = df_union['Age'].astype('int')
#df_union['Book-Title'] = df_union['Book-Title'].str.\
#   replace('the hobbit  the enchanting prelude to the lord of the rings', 'the hobbit') # post result adjustemnt
#df_union['Book-Title'] = df_union['Book-Title'].str.\
#    replace('the return of the king', 'the lord of the rings')
#df_union['Book-Title'] = df_union['Book-Title'].str.\
#    replace('the fellowship of the ring', 'the lord of the rings')
#df_union['Book-Title'] = df_union['Book-Title'].str.\
#    replace('the two towers', 'the lord of the rings')


df_union_grouped_count = df_union.groupby(['Book-Title'],sort=False).agg(Count=('Book-Title', 'count'),
                                                                         Mean_Rating=('Book-Rating', 'mean'),
                                                                         Median_Age=('Age', 'median'))\
    .sort_values(by=['Count','Mean_Rating'],ascending=[False,False]).reset_index()

df_union_grouped_count = df_union_grouped_count[df_union_grouped_count['Count'] >= 20]
df_union_grouped_count.Mean_Rating=df_union_grouped_count.Mean_Rating.round(2)
df_union_grouped_count.Median_Age=df_union_grouped_count.Median_Age.round(0).astype('int')
df_union_grouped_count = df_union_grouped_count.iloc[1:]



print("--- %s seconds ---" % (time.time() - start_time))

sns.set_theme(style="whitegrid")
plt.figure()
sns.countplot(x=df_BooksUsersRate['Book-Rating'])


plt.figure()
sns.histplot(x=df_BooksUsersRate['Age'],binrange=(10,80))



print(df_union_grouped_count.to_string())
print("--- %s seconds ---" % (time.time() - start_time))
plt.show()

