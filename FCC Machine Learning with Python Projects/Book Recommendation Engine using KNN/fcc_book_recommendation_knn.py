# -*- coding: utf-8 -*-
"""Copy of fcc_book_recommendation_knn.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PGrpWOo3HuAIH433m5RvxC2BUmx8osNZ
"""

# import libraries (you may add additional imports but you may not have to)
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt

# get data files
!wget https://cdn.freecodecamp.org/project-data/books/book-crossings.zip

!unzip book-crossings.zip

books_filename = 'BX-Books.csv'
ratings_filename = 'BX-Book-Ratings.csv'

# import csv data into dataframes
df_books = pd.read_csv(
    books_filename,
    encoding = "ISO-8859-1",
    sep=";",
    header=0,
    names=['isbn', 'title', 'author'],
    usecols=['isbn', 'title', 'author'],
    dtype={'isbn': 'str', 'title': 'str', 'author': 'str'})

df_ratings = pd.read_csv(
    ratings_filename,
    encoding = "ISO-8859-1",
    sep=";",
    header=0,
    names=['user', 'isbn', 'rating'],
    usecols=['user', 'isbn', 'rating'],
    dtype={'user': 'int32', 'isbn': 'str', 'rating': 'float32'})

# Merging the dataframes
df = df_ratings.merge(df_books,on="isbn",how="left")

# Plotting the dataset for exploratory analysis
fig, axes = plt.subplots(2, 1, figsize=(9, 9))
axes[0].set_title("user")
axes[0].set_xlabel("Number of reviews per user")
axes[0].set_ylabel("Frequency of a review")
axes[1].set_title("title")
axes[1].set_xlabel("Number of reviews per book")
axes[1].set_ylabel("Frequency of a review")
user_unique= df["user"].value_counts()
user_unique[user_unique<1000].hist(bins=100, ax = axes[0])
isbn_unique= df["isbn"].value_counts()
isbn_unique[isbn_unique<1000].hist(bins=100, ax = axes[1])

# Selecting indices of books with more than 100 reviews and users with more than
# 200 reviews.
user_unique = user_unique[user_unique >= 200].index
isbn_unique = isbn_unique[isbn_unique >= 100].index

# Filtering the dataset for to ensure statistical significance.
df_f = df.loc[(df["user"].isin(user_unique.values)) & (df["isbn"].isin(isbn_unique.values))]

# Checking one example of duplicated entries in the dataframe.
# In some cases one user has review the same book with two or more different
# ISBN.
df_f.loc[(df_f["user"]==11676) & (df_f["title"]=='The Summons')]

# Droping of duplicates
df_f = df_f.drop_duplicates(['title', 'user'])

# Rearranging the data in a sparse matrix for using it as input for the model.
df_p = df_f.pivot(index = 'title', columns = 'user', values = 'rating').fillna(0)
df_m = csr_matrix(df_p.values)

# Creating and training the model
neigh = NearestNeighbors(metric='cosine')
neigh.fit(df_m)

# function to return recommended books - this will be tested
def get_recommends(book = ""):
    recommended_books = [book,[]]
    dist,idx = neigh.kneighbors([df_p.loc[book]], 6, return_distance=True)

    recom_str = df_p.iloc[np.flip(idx[0])[:-1]].index.to_list()
    recom_dist = list(np.flip(dist[0])[:-1])
    for r in zip(recom_str,recom_dist):
        recommended_books[1].append(list(r))

    return recommended_books

books = get_recommends("Where the Heart Is (Oprah's Book Club (Paperback))")
print(books)

def test_book_recommendation():
  test_pass = True
  recommends = get_recommends("Where the Heart Is (Oprah's Book Club (Paperback))")
  if recommends[0] != "Where the Heart Is (Oprah's Book Club (Paperback))":
    test_pass = False
  recommended_books = ["I'll Be Seeing You", 'The Weight of Water', 'The Surgeon', 'I Know This Much Is True']
  recommended_books_dist = [0.8, 0.77, 0.77, 0.77]
  for i in range(2):
    if recommends[1][i][0] not in recommended_books:
      test_pass = False
    if abs(recommends[1][i][1] - recommended_books_dist[i]) >= 0.05:
      test_pass = False
  if test_pass:
    print("You passed the challenge! 🎉🎉🎉🎉🎉")
  else:
    print("You haven't passed yet. Keep trying!")

test_book_recommendation()