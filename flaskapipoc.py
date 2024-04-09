from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    html_table = None
    if request.method == 'POST':
        zip_code = request.form.get('zip_code')
        print("The zipcode is {}".format(zip_code))
        # Assuming you have a function to get the filtered data based on zip_code
        results = get_filtered_data(zip_code)
        html_table = results.to_html(classes='dataframe')
        print("The result is {}".format(results))
    #return render_template('index.html', results=results, results_not_empty=not results.empty if results is not None else False)
    return render_template('index.html', html_table=html_table)
def get_filtered_data(zip_code):
    print("I am in get filtered data")
    df = pd.read_csv('restaurants.csv')
    filter_list= [zip_code]
    filterDF = df.loc[df['zip_code'].isin(filter_list)]

    filterDF = filterDF[df['category'].str.contains('Convenience')==False] #taking out any resturants that has that specific value like cafe in category
    filterDF = filterDF[df['category'].str.contains('Desserts')==False]
    filterDF = filterDF[df['category'].str.contains('Juice')==False]
    filterDF = filterDF[df['category'].str.contains('Bakery')==False]
    filterDF = filterDF[df['category'].str.contains('Cafe')==False]
    
    rankedDf = get_ranking(filterDF)

    return rankedDf

def get_ranking(filterDF):
    #df_length = len(filterDF)
    #n_scores = len(filterDF['score'].unique())
    #n_ratings = len(filterDF['ratings'].unique())
    mean_rating = filterDF['ratings'].mean() #mean of ratings column
    mean_score = filterDF['score'].mean()
    m = filterDF['ratings'].quantile(.50)
    filterDF['ranking'] = (filterDF['ratings']/(filterDF['ratings']+ m))* mean_rating + (m/(filterDF['ratings']+m))* mean_score
    filterDF.dropna(inplace=True) #get rid of NaN values
    filterDF = filterDF.sort_values(by = ['ranking', 'score', 'ratings'], ascending=False) #sort the dataset so that best rated places are top to bottom
    return filterDF
if __name__ == '__main__':
    app.run(debug=True)
