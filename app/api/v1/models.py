from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
import uuid
app = Flask(__name__)
api = Api(app)


class User(Resource):
    """This class defines methods that perform CRUD operations on a list of users"""

    def __init__(self):
        self.users = {}

        self.u_token = {}

    def get(self, id):
        pass

    def post(self, id):
        data = request.get_json()

    def put(self, id):
        pass

    def delete(self, id):
        pass


api.add_resource(User, '/users/<int:id>')


class ProductList(Resource):
    """This class defines methods that fetch products from the list and post products to the list"""
    def get(self):
        pass

    def post(self):
        pass


class Product(Resource):
    """This class defines methods that get, post, put and delete an item from the list of product
    using the id"""
    def get(self, id):
        pass

    def post(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass


api.add_resource(ProductList, '/api/v1/products')
api.add_resource(Product, '/api/v1/products/<int:id>')


class Sale(Resource):
    """This class defines methods that get, post, put, delete a sales record using the id
    of that record"""
    def get(self, id):
        pass

    def post(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass


class SaleList(Resource):
    """This class defines methods that fetch all sales records and post sales records to the list
    of sales records"""
    def get(self):
        pass

    def post(self):
        pass


api.add_resource(SaleList, '/api/v1/sales')
api.add_resource(Sale, '/api/v1/sales/<int:id>')
