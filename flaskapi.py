import pandas as pd
import numpy as np
import csv
import seaborn as sns
from sklearn.neighbors import NearestNeighbors
import os

df = pd.read_csv('/content/drive/MyDrive/RestaurantRecommendationData/restaurants.csv') #importing dataset
df.describe()

ratings_df = df['ratings']
ratings_df.dropna(inplace=True) #gets rid of NaN values
ratings_df.head()

ratings_df.info()

sns.countplot(x=ratings_df)

print("If one of the factors doesn't apply, just hit enter. Also, zip code is mandatory.")
zipCode=input("Enter your zip code: ")
#city= input("Enter you city:")
categoryInput=input("Enter your category of food you're interested to eat. ex:(Chinese, Halal, Seafood, Healthy, Fast Food): ")

#categoryInput.upper() #turn into uppercase

priceInput=input("Enter the price range you are looking for ex:($, $$, or $$$?): ")
userScore=input("Do you want a minimum score (1-5): ")
userRatings=input("Do you want a minimum amount of reviews for each restaurants selected: ")

filter_list= [zipCode]

filterDF = df.loc[df['zip_code'].isin(filter_list)]
'''
if city != '' :
  filterDF = filterDF[df['full_address'].str.contains(city)==True]
'''

if priceInput != '' :
  filterDF = filterDF[df['price_range'].str.contains(priceInput)==True]

if userScore != '':
  filterDF = filterDF[df['score'] >= float(userScore)]

if userRatings != '':
  filterDF = filterDF[df['ratings'] > int(userRatings)]

if categoryInput != '' :
  filterDF = filterDF[df['category'].str.contains(categoryInput)==True] #adding only what the category of categoryInput

filterDF = filterDF[df['category'].str.contains('Convenience')==False] #taking out any resturants that has that specific value like cafe in category
filterDF = filterDF[df['category'].str.contains('Desserts')==False]
filterDF = filterDF[df['category'].str.contains('Juice')==False]
filterDF = filterDF[df['category'].str.contains('Bakery')==False]
filterDF = filterDF[df['category'].str.contains('Cafe')==False]
#df.loc[df['zip_code']=='23060']

rsltdf = df.query('zip_code=="23233" and category=="Indian"' ) #testing with queries
rsltdf

score_df= df['score']
score_df.dropna(inplace=True)
#userInput = input("Enter a : ")
#total_score_df= (score_df.loc[:, "score"] + ratings_df.loc["ratings")
score_df

df_length = len(df)
n_scores = len(df['score'].unique())
n_ratings = len(df['ratings'].unique())
print(f"Length of data frame: {df_length}")
print(f"Scores: {n_scores}")
print(f"Ratings: {n_ratings}")
#n_users = len(ratings_df['userId'].unique())

mean_rating = filterDF['ratings'].mean() #mean of ratings column
#filterDF.groupby('zip_code')['ratings'].mean()
#.apply(lambda x: x.mean().index[0])
mean_score = filterDF['score'].mean()
print(mean_rating)
print(mean_score)

m= filterDF['ratings'].quantile(.50)

'''
# loop through the rows using iterrows()
list_ratings = df['ratings'].tolist()
list_score = df['score'].tolist()

for index, row in filterDF.iterrows():
     n_ranking = (list_score[index]*mean_rating)+list_ratings[index]

#def test(x):
for index, row in filterDF.iterrows():
   n_ranking= (row['score']* mean_rating)+row['ratings']
   #df['rankings']=n_ranking
   print(n_ranking)
  # list = df[''].tolist() #can make smth a list
   df.assign(rankings= [n_ranking])
'''
#filterDF['ranking'] = (filterDF['score']*mean_rating)+ filterDF['ratings'] #equation to get final value to determine the best resturant

filterDF['ranking'] = (filterDF['ratings']/(filterDF['ratings']+ m))* mean_rating + (m/(filterDF['ratings']+m))* mean_score

print(df)

# df.apply(test, axis=1)
   # add the zip code next to the columns that correspond (hopefully instead of ID number)

filterDF.dropna(inplace=True) #get rid of NaN values
filterDF = filterDF.sort_values(by = ['ranking', 'score', 'ratings'], ascending=False) #sort the dataset so that best rated places are top to bottom


from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/get-data', methods=['POST'])
def get_data():
    zip_code = request.json.get('zip_code')
    #df = pd.read_csv('your_data.csv') # Load your DataFrame
    #filtered_data = df[df['zip_code'] == zip_code]
    #return jsonify(filtered_data.to_dict(orient='records'))
    return jsonify(filterDF.to_dict(orient='records'))
if __name__ == '__main__':
    app.run(debug=True)


# import ipywidgets as widgets
# from IPython.display import display

# text = widgets.Text(
#     value='',
#     placeholder='Type something',
#     description='Input:',
#     disabled=False
# )
# button = widgets.Button(description='Submit')
# output = widgets.Output()

# def on_button_clicked(b):
#     with output:
#         # Here you can call your Flask app's endpoint with the input from the text widget
#         # For demonstration, let's just print the input
#         print(filterDf)

# button.on_click(on_button_clicked)
# display(text, button, output)

import ipywidgets as widgets
from IPython.display import display
import requests

text = widgets.Text(
    value='',
    placeholder='Enter Zip Code',
    description='Zip Code:',
    disabled=False
)
button = widgets.Button(description='Submit')
output = widgets.Output()

def on_button_clicked(b):
    with output:
        url = 'http://localhost:5000/get-data' # Adjust the URL as needed
        data = {'zip_code': text.value}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            display(pd.DataFrame(response.json()))
        else:
            print("Error:", response.status_code)

button.on_click(on_button_clicked)
display(text, button, output)
