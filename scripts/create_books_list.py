import pandas as pd
import codecs,json

us_canada_user_rating = pd.read_csv('data/data.csv', sep=',', error_bad_lines=False, encoding="utf-8")
us_canada_user_rating.columns = ['userID','ISBN', 'bookRating', 'bookTitle', 'totalRatingCount', 'Location']
array=us_canada_user_rating.bookTitle.unique()


b = array.tolist()
json_file = "books.json" 
json.dump(b, codecs.open(json_file, 'w', encoding='utf-8'), sort_keys=True, indent=4)


