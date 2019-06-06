from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Product Class/Model
class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  StoreID = db.Column(db.Integer)
  Category = db.Column(db.String(100))
  Quantity = db.Column(db.Integer)

  def __init__(self, StoreID, Category, Quantity):
    self.StoreID = StoreID
    self.Category = Category
    self.Quantity = Quantity

# Product Schema
class ProductSchema(ma.Schema):
  class Meta:
    fields = ('id','StoreID', 'Category', 'Quantity')

# Init schema
product_schema = ProductSchema(strict=True)
products_schema = ProductSchema(many=True, strict=True)

# Create a Product
@app.route('/Tesco', methods=['POST'])
def add_product():
  StoreID =request.json['StoreID']
  Category = request.json['Category']
  Quantity = request.json['Quantity']


  new_product = Product(StoreID, Category, Quantity)

  db.session.add(new_product)
  db.session.commit()

  return product_schema.jsonify(new_product)

# Get All Products
@app.route('/Tesco', methods=['GET'])
def get_products():
  all_products = Product.query.all()
  result = products_schema.dump(all_products)
  return jsonify(result.data)

# Get Single Products
@app.route('/Tesco/<id>', methods=['GET'])
def get_product(id):
  product = Product.query.filter(Product.StoreID == id)
  return products_schema.jsonify(product)

# Update a Product
@app.route('/Tesco/<id>', methods=['PUT'])
def update_product(id):
  product = Product.query.get(id)

  StoreID = request.json['StoreID']
  Category = request.json['Category']
  Quantity = request.json['Quantity']

  product.StoreID = StoreID
  product.Category = Category
  product.Quantity = Quantity

  db.session.commit()

  return product_schema.jsonify(product)

# Delete Product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
  product = Product.query.get(id)
  db.session.delete(product)
  db.session.commit()

  return product_schema.jsonify(product)

# Run Server
if __name__ == '__main__':
  app.run(debug=True, port=4000)
