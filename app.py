import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask import jsonify
import json 
from flask_cors import CORS,cross_origin
from flask import request

app=Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/",methods=['GET'])
@cross_origin()
def home():
    s="Routes  1) GET /categories --returns a list of categories to choose from \n 2)POST /data -body json  categories:[list of categories]"
    return jsonify(s)

@app.route("/data",methods=['POST'])
@cross_origin()
def data():
    if request.headers['Content-Type'] == 'application/json':
        d=json.dumps(request.json)
    #print(d)
    d=json.loads(d)
    print(d)
    print(type(d))
    print(d["categories"])

    
    def getNews(category):
    
        newsDictionary = {
            'success': True,
            'category': category,
            'data': []
        }
        datares=[]
        for i in category:
            count=5

            try:
                htmlBody = requests.get('https://www.inshorts.com/en/read/' + i)
            except requests.exceptions.RequestException as e:
                newsDictionary['success'] = False
                newsDictionary['errorMessage'] = str(e.message)
                return newsDictionary

            soup = BeautifulSoup(htmlBody.text, 'lxml')
            newsCards = soup.find_all(class_='news-card')
            if not newsCards:
                newsDictionary['success'] = False
                newsDictionary['errorMessage'] = 'Invalid Category'
                return newsDictionary

            for card in newsCards:
                try:
                    title = card.find(class_='news-card-title').find('a').text
                except AttributeError:
                    title = None

                try:
                    imageUrl = card.find(
                        class_='news-card-image')['style'].split("'")[1]
                except AttributeError:
                    imageUrl = None

                try:
                    url = ('https://www.inshorts.com' + card.find(class_='news-card-title')
                        .find('a').get('href'))
                except AttributeError:
                    url = None

                try:
                    content = card.find(class_='news-card-content').find('div').text
                except AttributeError:
                    content = None

                try:
                    author = card.find(class_='author').text
                except AttributeError:
                    author = None

                try:
                    date = card.find(clas='date').text
                except AttributeError:
                    date = None

                try:
                    time = card.find(class_='time').text
                except AttributeError:
                    time = None

                try:
                    readMoreUrl = card.find(class_='read-more').find('a').get('href')
                except AttributeError:
                    readMoreUrl = None

                newsObject = {
                    'title': title,
                    'imageUrl': imageUrl,
                    'url': url,
                    'content': content,
                    'category':i,
                    'author': author,
                    'date': date,
                    'time': time,
                    'readMoreUrl': readMoreUrl
                }
                
                if(count!=0):
                    newsDictionary['data'].append(newsObject)
                    count=count-1

        datares.append(newsDictionary)

        return datares
    
    return jsonify(getNews(d["categories"]))
@app.route("/categories",methods=['GET'])
@cross_origin()
def categories():
    l=['Sports','Technology','Business','World','Politics','Startup','Entertainment','Science','Automobile','National','Miscellaneous']
    return jsonify(l)

if __name__ == "__main__":
    app.run(debug=True)




