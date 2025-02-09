# app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(_name_)
CORS(app)

# Configure your database (SQLite for simplicity)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'
db = SQLAlchemy(app)

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    source = db.Column(db.String(100), nullable=False)

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.json['url']
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract news details (this example assumes a specific structure)
    title = soup.find('h1').text
    content = soup.find('div', {'class': 'content'}).text
    source = url.split('/')[2]

    news = News(title=title, url=url, content=content, source=source)
    db.session.add(news)
    db.session.commit()

    return jsonify({'message': 'News added successfully'}), 201

@app.route('/news', methods=['GET'])
def get_news():
    news_list = News.query.all()
    news_data = [{'title': news.title, 'url': news.url, 'content': news.content, 'source': news.source} for news in news_list]
    return jsonify(news_data)

if _name_ == '_main_':
    db.create_all()
    app.run(debug=True)
