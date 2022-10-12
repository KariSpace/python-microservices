from itertools import product
import json
from flask import abort
import requests
from flask import Flask, jsonify

from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from flask_migrate import Migrate
from dataclasses import dataclass

from producer import publish

# https://stackabuse.com/using-sqlalchemy-with-flask-and-postgresql/

DATABASE_CONNECTION_URI = 'postgresql://postgres:postgres@db:5432/main'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION_URI 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

CORS(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


@dataclass
class Product(db.Model):
    id: int
    title: str
    image: str
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))
    
@dataclass
class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    
    __table_args__ = (
        db.UniqueConstraint(user_id, product_id),
    )

    
@app.route('/api/products')
def index():
    return jsonify(Product.query.all())


@app.route('/api/products/like/<int:id>')
def like(id):
    print(id)
    json = (requests.get('http://host.docker.internal:8000/api/user')).json()
    print(json)
    try:
        productUser = ProductUser(user_id=json['id'], product_id=id)
        db.session.add(productUser)
        db.session.commit()
        
        publish('product_liked', id)
        
    except:
        abort(400, 'Already liked')
    
    
    return ({'result' : "ok"})

# with app.app_context():
#     db.create_all()
    
migrate = Migrate(app, db)
       
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')