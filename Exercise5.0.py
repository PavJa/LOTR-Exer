import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
import re

start_time = time.time()

data_Books = 'BX-Books.csv'
data_Users = 'BX-Users.csv'
data_Ratings = 'BX-Book-Ratings.csv'

pd.set_option('display.max_columns', 4)
pd.set_option('max_colwidth', None)
pd.options.display.max_colwidth = 60

# 1.1 DATA FRAME AND CLEANING

df_Books = pd.read_csv(data_Books, dtype = 'str', sep=';', encoding='latin-1', on_bad_lines='skip')
df_Books = df_Books.drop(['Image-URL-S', 'Image-URL-M','Image-URL-L'], axis=1) # drop pictures
df_Users = pd.read_csv(data_Users, sep=';', encoding='latin-1', on_bad_lines='skip')
df_Ratings = pd.read_csv(data_Ratings, sep=';', encoding='latin-1', on_bad_lines='skip')
#print(df_Books.dtypes)
#df_Ratings.groupby(['User-ID'])
#print(df_Users.columns)  # see shape and some columns
#print(df_Ratings.head)
#print(df_Books.shape)

df_UsersRate = df_Ratings.merge(df_Users, on='User-ID', how = 'inner')
df_BooksUsersRate = df_UsersRate.merge(df_Books, on='ISBN', how = 'inner')
#print(df_BooksUsersRate['Book-Rating'].dtype)

#print(df_BooksUsersRate.isna().sum())
NaN_Columns = df_BooksUsersRate.columns[df_BooksUsersRate.isna().any()].tolist() # check null values, obviously they are
#print(NaN_Columns) # gives me columns with null values, publisher is important information but not a selection criterion
# age and book author might be important in constructing selection criteria
#print(df_BooksUsersRate.isnull().values.any()) # just checking we have no NaN values
df_BooksUsersRate['Book-Author'] = df_BooksUsersRate['Book-Author'].fillna('Missing')
df_BooksUsersRate['Publisher'] = df_BooksUsersRate['Publisher'].fillna('Missing')

# mala pismena, odstranit carky, dvojtecky a zavorky, odtraneni indentu
df_BooksUsersRate['Book-Title']= df_BooksUsersRate['Book-Title'].str.lower()
df_BooksUsersRate['Book-Title'] = df_BooksUsersRate['Book-Title'].str.replace(r'\(.*\)', '',regex=True)
df_BooksUsersRate['Book-Title'] = df_BooksUsersRate['Book-Title'].str.replace(r",",'', regex=True)
df_BooksUsersRate['Book-Title'] = df_BooksUsersRate['Book-Title'].str.replace(r":",'', regex=True)
df_BooksUsersRate['Book-Title'] = df_BooksUsersRate['Book-Title'].replace(r'\s+', ' ', regex=True)
df_BooksUsersRate['Book-Title'] = df_BooksUsersRate['Book-Title'].str.strip()

#print(df_BooksUsersRate.loc[df_BooksUsersRate['User-ID'] == '237451'].to_string()) # 4 lord of the rings books

def NameChangePref(*args):
    for title in args:
            df_BooksUsersRate['Book-Title'] = df_BooksUsersRate['Book-Title'].str.\
            replace(title, 'lord of the rings')


def NameChangeGen(Mtitle, *args):
    for title in args:
        df_BooksUsersRate['Book-Title'] = df_BooksUsersRate['Book-Title'].str.\
            replace(title, Mtitle)

NameChangeGen('the hobbit', 'the hobbit the enchanting prelude to the lord of the rings',
           'the hobbit or there and back again')

#must come last, so it does not change things
NameChangePref('the return of the king','the fellowship of the ring', 'the two towers', 'the lord of the rings')
#NameChangePref('dune',)



# 1.1 PLOTS

# Delete Rows by Checking Conditions
df_NoZero_ranking = df_BooksUsersRate.loc[df_BooksUsersRate['Book-Rating']>0]
#print(df_NoZero_ranking)
sns.set_theme(style="whitegrid")
f, axes = plt.subplots(1, 2, figsize=(15,5))
# sns.countplot(x=df_BooksUsersRate['Book-Rating'], ax=axes[0]).set(title = 'Rating distribution')
sns.countplot(x=df_NoZero_ranking['Book-Rating'], ax=axes[1]).set(title='Book-Rating distribution (0 values excluded)')
sns.histplot(x=df_BooksUsersRate['Age'], ax=axes[0], binrange=(10,80), binwidth=1).set(title='Age distribution'
                                                                                               '(NaN values excluded)')

# STEP 2 FINDING A DECISION RULE

# similar rating - far streched assumption that this is our reference class (we know nothing about our stakeholder).
# Create a list of people (user-ID) that have read the lord of the rings na dgave it a rating of 7 or more.

df_BooksUsersRate['Book-Title'] = df_BooksUsersRate['Book-Title'].astype('str') # for left join to work

Tolkien_list_rating = [x for x, y, z in zip(df_BooksUsersRate['User-ID'],df_BooksUsersRate['Book-Title'],
                                          df_BooksUsersRate['Book-Rating']) if ('lord of the rings' == y and z>=9)]

list_Similar_Rate = []

for x in Tolkien_list_rating:
    k = df_BooksUsersRate.loc[(df_BooksUsersRate['User-ID'] == x) & (df_BooksUsersRate['Book-Rating'] >= 6) &
                              (10 <= df_BooksUsersRate['Age']) & (df_BooksUsersRate['Age'] <= 20)]
    k_rate_book = k[['User-ID','Book-Title', 'Book-Rating', 'Age']]
    list_Similar_Rate.append(k_rate_book)

df_union = pd.concat(list_Similar_Rate)


df_union_grouped_count = df_union.groupby(['Book-Title'],sort=False).agg(Count=('Book-Title', 'count'),
                                                                         Mean_Rating=('Book-Rating', 'mean'),
                                                                         Median_Age=('Age', 'median'))\
    .sort_values(by=['Count','Mean_Rating'], ascending=[False,False]).reset_index()

df_union_grouped_count = df_union_grouped_count[df_union_grouped_count['Count'] >= 10]
df_union_grouped_count.Mean_Rating = df_union_grouped_count.Mean_Rating.round(2)
df_union_grouped_count.Median_Age = df_union_grouped_count.Median_Age.round(0).astype('int')
#df_union_grouped_count = df_union_grouped_count.iloc[1:]

print(df_union_grouped_count.to_string())
print("--- %s seconds ---" % (time.time() - start_time))
#plt.show()

