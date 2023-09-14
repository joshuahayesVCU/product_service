import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))

# Initalizing the flask application and connecting to the database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'task.sqlite')
db = SQLAlchemy(app)

# Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# GET ALL
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list = [{"id": product.id, "name": product.name, "price": product.price, "quantity": product.quantity} for product in products]
    return jsonify({"products": product_list})

# CREATE NEW
@app.route('/products', methods=['POST'])
def create_product():
    data = request.json
    if "name" or "price" or "quantity" not in data:
        return jsonify({"error": "Product name is required"}), 400

    new_product = Product(name=data['name'], price=data['price'], quantity=data['quantity'])
    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "Product created", "product":
                    {"id": new_product.id,
                     "name": new_product.name,
                     "price": new_product.price,
                     "quantity": new_product.quantity}})

if __name__ == "__main__":
    # db.create_all()
    app.run(debug=True)


