import requests

def create_product(name, price, quantity):
    new_product = {"name": name, "price": price, "quantity": quantity}
    response = requests.post('http://127.0.0.1:5000/products', json=new_product)
    data = response.json()
    return data

def initalize_data(product_list):
    for entries in product_list:
        product = entries.split()
        create_product(product[0], float(product[1]), product[2])

    return

if __name__ == "__main__":
    product_list = ["Melon 12.99 200", "Pizza 6.00 12", "Rice 2.89 999"]
    initalize_data(product_list)



