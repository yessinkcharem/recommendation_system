from flask import Flask, render_template, request
import numpy as np
from neo4j import GraphDatabase
import pandas as pd
from IPython.display import HTML


db = GraphDatabase.driver(uri="bolt://localhost:7687", auth=("neo4j","lose ur self"))

app = Flask(__name__)


# @app.route('/')
# def index():
#     return render_template('index.html')


# @app.route('/predict', methods=['GET', 'POST'])
# def predict():
#     val1 = request.form['bedrooms']
#     val2 = request.form['bathrooms']
#     val3 = request.form['floors']
#     val4 = request.form['yr_built']
#     arr = np.array([val1, val2, val3, val4])
#     arr = arr.astype(np.float64)
#     pred = model.predict([arr])

#     return render_template('index.html', data=int(pred))

session=db.session()

#methods to create Queries
def create_possible_destinations_query(country , city):
    return "match (s:Airport{country:'" + country + "',city:'" + city + "'})<-[:from]-(r:Route)-[:to]->(d:Airport) return s.country+' '+s.city as source ,collect(d.country+' '+d.city) as dest,count(*) as number"


def create_possible_destinations_airlines_query(country , city):
    return "match (s:Airport{country:'" + country + "',city:'" + city + "'})<-[:from]-(r:Route)-[:to]->(d:Airport) match (r)-[:by]->(airline:Airline)return s.name as source , d.name as destination , collect(airline.name) as possible_airlines"
     
def create_airlines_rating_query():
    return "match (a:Airline)<-[:ABOUT]-(tweet1:Tweet {class:'positive'}) match (a:Airline)<-[:ABOUT]-(tweet2:Tweet{class:'negative'}) return a.name as airline , count(distinct tweet1) as positive_tweets ,count(distinct tweet2) as negative_tweets ,count(distinct tweet1) - count(distinct tweet2) as diffrence order by diffrence desc"






#request waited : a json with attributes country and city
@app.route('/possible_dest' ,methods=['GET', 'POST'])
def possible_destinations():
    response = request.json

    country = response['country']
    city = response['city']

    print(country + ' ' + city)
    possible_destinations_query = create_possible_destinations_query(country,city)
    print(possible_destinations_query)

    result = session.run(possible_destinations_query)
    data=result.data()
    df = pd.DataFrame(data)
    to_return = df.to_json()
    #print(df)
    print(to_return)
    response = df.to_html()
    return response



#request waited : a json with attributes country and city
@app.route('/possible_destinations_airlines' ,methods=['GET', 'POST'])
def possible_destinations_airlines():
    response = request.json

    country = response['country']
    city = response['city']

    print(country + ' ' + city)
    possible_destinations_airlines_query = create_possible_destinations_airlines_query(country,city)
    print(possible_destinations_airlines_query)

    result = session.run(possible_destinations_airlines_query)
    data=result.data()
    df = pd.DataFrame(data)
    to_return = df.to_json()
    #print(df)
    print(to_return)
    response = df.to_html()
    return response


#request waited : no params
@app.route('/airlines_rating' ,methods=['GET', 'POST'])
def airline_rating():
    response = request.json

    airlines_rating_query = create_airlines_rating_query()
    print(airlines_rating_query)

    result = session.run(airlines_rating_query)
    data=result.data()
    df = pd.DataFrame(data)
    to_return = df.to_json()
    #print(df)
    print(to_return)
    response = df.to_html()
    return response
    


# @app.route('/predict', methods=['GET', 'POST'])
# def predict():
    


    


if __name__ == '__main__':
    app.run(debug=True)
