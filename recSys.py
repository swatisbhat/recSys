import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
import sklearn
from sklearn.decomposition import TruncatedSVD

us_canada_user_rating = pd.read_csv('data/data.csv', sep=',', error_bad_lines=False, encoding="latin-1")
us_canada_user_rating.columns = ['userID','ISBN', 'bookRating', 'bookTitle', 'totalRatingCount', 'Location']


us_canada_user_rating_pivot = us_canada_user_rating.pivot(index = 'bookTitle', columns = 'userID', values = 'bookRating').fillna(0)
us_canada_user_rating_matrix = csr_matrix(us_canada_user_rating_pivot.values)

from sklearn.neighbors import NearestNeighbors

model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
model_knn.fit(us_canada_user_rating_matrix)


us_canada_book_title = us_canada_user_rating_pivot.index
us_canada_book_list = list(us_canada_book_title)

def recommend(book_like):
    query_index = us_canada_book_list.index(book_like)  
    distances, indices = model_knn.kneighbors(us_canada_user_rating_pivot.iloc[query_index, :].reshape(1, -1), n_neighbors = 6)
    result=[]
    for i in range(0, len(distances.flatten())):
        if i!=0:
        	result.append(us_canada_user_rating_pivot.index[indices.flatten()[i]])
    return result
