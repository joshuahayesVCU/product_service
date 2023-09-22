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

# GET ONE
@app.route('/products/<int:product_id>', methods=["GET"])
def get_product(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({"id": product.id,
                        "name": product.name,
                        "price": product.price,
                        "quantity": product.quantity})
    else:
        return jsonify({"error": "Product not found"}), 404

# CREATE NEW
@app.route('/products', methods=['POST'])
def create_product():
    data = request.json
    if "name" or "price" or "quantity" not in data:
        return jsonify({"error": "All JSON fields must be filled. "})


    new_product = Product(name=data['name'], price=data['price'], quantity=data['quantity'])
    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "Product created", "product":
                    {"id": new_product.id,
                     "name": new_product.name,
                     "price": new_product.price,
                     "quantity": new_product.quantity}})

# UPDATE STOCK
@app.route('/products/update/quantity/<int:product_id>', methods=["POST"])
def update_quantity(product_id):
    product = Product.query.get(product_id)

    desired_quantity_json = request.json
    quantity_modifier = int(desired_quantity_json['quantity'])

    if not product:
        return jsonify({"error": "Error updating product stock, error fetching from database"})

    current_quantity = product.quantity
    if (current_quantity < quantity_modifier):
        return jsonify({"error": "Error updating product stock, not enough stock"})

    product.quantity = product.quantity - quantity_modifier
    db.session.commit()
    return jsonify({"success": f"Product quantity updated by {quantity_modifier}"})

if __name__ == "__main__":
    # db.create_all()
    app.run(debug=True, port=5001)


