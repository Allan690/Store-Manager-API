from flask_api import FlaskAPI
# from instance.config import app_config
from flask import request, jsonify, session, Blueprint
api = Blueprint('app', __name__)


def create_app():
    from app.api.v1.models import Product
    from app.api.v1.models import User
    from app.api.v1.models import Sale

    # create instance of flask-api in app
    app = FlaskAPI(__name__)

    app.secret_key = 'i-love-coding'
    app.register_blueprint(api)

    @app.route("/")
    def welcome():
        message = "Welcome to our Store Manager API"
        response = jsonify({"welcome": message})
        return response

    """Defining authentication"""

    # api functionality
    @app.route('/api/v1/auth/register', methods=['POST', 'GET'])
    def register():
        """
        This end point will register a user by getting info from the request
        """
        if request.method == 'GET':
            message = "method not allowed when registering user. Use post"
            response = jsonify({"message": message, "status_code": 405})
            response.status_code = 405
            return response

        else:
            email = str(request.data.get('email', ''))
            password = str(request.data.get('password', ''))
            confirm_password = str(request.data.get('confirm_password', ''))

            if email and password and confirm_password:
                value = User.check_email_exists(email)
                validate_password = User.validate_password(password)
                validate_email = User.validate_email(email)
                validate_password_format = User.validate_password_format(password)

                if value:
                    response = jsonify({"message": "email already exists", "status_code": 400})
                    response.status_code = 400
                    return response

                elif validate_password:
                    response = jsonify({"message": "password must be longer than 6 characters", "status_code": 400})
                    response.status_code = 400
                    return response

                elif validate_email:
                    response = jsonify({"message": "Enter a valid email format", "status_code": 400})
                    response.status_code = 400
                    return response

                elif validate_password_format:
                    response = jsonify({"message": "Password cannot be empty", "status_code": 400})
                    response.status_code = 400
                    return response

                else:
                    user = User(email=email, password=password, confirm_password=confirm_password)
                    message = user.create_user(email, password, confirm_password)
                    """turn message into json"""
                    response = jsonify({"message": message, "status_code": 201})
                    """response.status_code=201"""
                    return response

            else:
                response = jsonify({"message": "enter all details", "status_code": 400})
                response.status_code = 400
                return response

    @app.route('/api/v1/auth/login', methods=['POST', 'GET'])
    def login():
        """this end point will log in a user based on username and password"""

        if request.method == 'GET':
            message = "method not allowed when logging in user. Use post"
            response = jsonify({"message": message, "status_code": 405})
            response.status_code = 405
            return response
        else:
            email = str(request.data.get('email', ''))
            password = str(request.data.get('password', ''))

            if email and password:
                session["email"] = email
                message = User.login(email, password)
                response = jsonify({"message": message, "status_code": 200})
                return response

            else:
                response = jsonify({"message": "enter all details", "status_code": 400})
                response.status_code = 400
                return response

    @app.route('/api/v1/auth/logout', methods=["POST", "GET"])
    def logout():
        """This endpoint logs out the user and destroys the current session"""

        if request.method == "GET":
            message = "Method not allowed. Use POST request to logout"
            response = jsonify({"message": message, "status_code": 405})
            response.status_code = 405
            return response
        else:
            if session.get("email") is not None:
                session.pop("email", None)
                return jsonify({"message": "Logout successful!"})
            return jsonify({"message": "You are not logged in"})

    @app.route('/api/v1/auth/reset-password', methods=['POST'])
    def reset():
        """This endpoint resets the password of a user"""
        email = str(request.data.get('email', ''))
        password = str(request.data.get('password', ''))
        confirm_password = str(request.data.get('confirm_password', ''))

        if email and password and confirm_password:
            resp_msg = User.reset_password(email, password, confirm_password)

            if resp_msg == "Password reset was successful":
                response = jsonify({"message": "password reset successfully", "status_code": 200})
                response.status_code = 200
                return response

            elif resp_msg == "Password and confirm password must be the same":
                response = jsonify({"message": "password and confirm must be the same", "status_code": 409})
                response.status_code = 409
                return response

            elif resp_msg == "Account does not exist":
                response = jsonify({"message": "password and confirm must be the same", "status_code": 404})
                response.status_code = 404
                return response

        else:
            response = jsonify({"message": "enter all details", "status_code": 400})
            response.status_code = 400
            return response

    """Product end points"""

    @app.route('/api/v1/products', methods=['POST', 'GET'])
    def product():
        if request.method == 'POST':
            """gets data from request and saves a product"""

            name = str(request.data.get('name', ''))
            description = str(request.data.get('description', ''))
            category = str(request.data.get('category', ''))

            if name and description and category:
                """Validate for non-duplication"""
                check_name = Product.check_product_name_exists(name)
                valid_prod_name = Product.validate_product_name(name)
                valid_descr = Product.validate_product_description(description)
                valid_category = Product.validate_category_name(category)
                if check_name:
                    response = jsonify({"message": "Product name already exists", "status_code": 400})
                    response.status_code = 400
                    return response

                elif valid_prod_name:
                    response = jsonify({"message": "product name missing", "status_code": 400})
                    response.status_code = 400
                    return response

                elif valid_descr:
                    response = jsonify({"message": "description is missing", "status_code": 400})
                    response.status_code = 400
                    return response

                elif valid_category:
                    response = jsonify({"message": "category is missing", "status_code": 400})
                    response.status_code = 400
                    return response

                else:
                    """create product object"""
                    prod = Product(name=name, description=description, category=category)
                    new_prod = prod.add_product(name, description, category)
                    response = jsonify(new_prod)
                    response.status_code = 201
                    return response

            elif not name:
                response = jsonify({"message": "name is missing", "status_code": 400})
                response.status_code = 400
                return response

            elif not description:
                response = jsonify({"message": "description missing", "status_code": 400})
                response.status_code = 400
                return response

            else:
                response = jsonify({"message": "category is missing", "status_code": 400})
                response.status_code = 400
                return response

        else:
            """if its a get request"""
            products = Product.get_all_products()
            print(products)
            if not products:
                response = jsonify({"message": "product not exist", "status": 200})
                response.status_code = 200

                response = jsonify({"message": "product does not exist", "status": 400})
                response.status_code = 400

                return response

            response = jsonify({"products": products})
            response.status_code = 200
            return response

    @app.route('/api/v1/products/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def prod_rud(id):
        """Fetches the id of a product and uses it to get one product"""

        prod_found = Product.find_product_by_id(id)

        if request.method == "GET":
            if prod_found:
                response = jsonify({"product": prod_found})
                response.status_code = 200
                return response

            else:
                response = jsonify({"message": "product does not exist", "status": 404})
                response.status_code = 404
                return response

        elif request.method == "PUT":
            if prod_found:

                name = str(request.data.get('name', ''))
                description = str(request.data.get('description', ''))
                category = str(request.data.get('category', ''))

                prod_found[0]["name"] = name
                prod_found[0]["description"] = description
                prod_found[0]["category"] = category

                response = jsonify({"product": prod_found})
                response.status_code = 200
                return response

            else:
                response = jsonify({"message": "Cannot update a product that does not exist", "status": 404})
                response.status_code = 404
                return response

        else:
            if prod_found:
                products = Product.get_all_products()
                products.remove(prod_found[0])
                response = jsonify({"product": "product successfully deleted", "status": 200})
                response.status_code = 200
                return response
            else:
                response = jsonify({"message": "Cannot delete product that does not exist", "status": 404})
                response.status_code = 404
                return response

    @app.route('/api/v1/products/<string:name>', methods=['GET', 'PUT'])
    def product_manipulation_by_name(name):
        """get the name from the route"""
        """uses the name to find the product"""

        prod_found = Product.find_product_name(name)
        if not prod_found:
            """if no product is found that matches the name"""
            response = jsonify({"message": "product does not exist", "status": 404})
            response.status_code = 404
            return response

        if request.method == "GET":
            if prod_found:
                response = jsonify({"Product": prod_found})
                response.status_code = 200
                return response

            else:
                response = jsonify({"message": "product does not exist", "status": 404})
                response.status_code = 404
                return response

        elif request.method == 'PUT':
            if prod_found:
                name = str(request.data.get('name', ''))
                description = str(request.data.get('description', ''))
                category = str(request.data.get('category', ''))

                prod_found[0]["name"] = name
                prod_found[0]["description"] = description
                prod_found[0]["category"] = category

                response = jsonify({"product": prod_found})
                response.status_code = 200
                return response

            else:
                response = jsonify({"message": "Cannot update product that does not exist", "status": 404})
                response.status_code = 404
                return response

        else:
            if prod_found:

                products = Product.get_all_products()
                products.remove(prod_found[0])
                response = jsonify({"product": "product successfully deleted", "status": 200})
                response.status_code = 200
                return response
            else:
                response = jsonify({"message": "Cannot delete product that does not exist", "status": 404})
                response.status_code = 404
                return response

    """Sales end points"""
    @app.route('/api/v1/sales', methods=['POST', 'GET'])
    def sale():
        if request.method == 'POST':
            """gets data from request and saves a sale"""

            name = str(request.data.get('name', ''))
            description = str(request.data.get('description', ''))
            quantity = str(request.data.get('quantity', ''))
            total = str(request.data.get('total', ''))

            if name and description and quantity and total:
                """Validate for non-duplication"""
                check_name = Sale.check_sale_name_exists(name)
                valid_sale_name = Sale.validate_sale_name(name)
                valid_descr = Sale.validate_sale_description(description)
                valid_quantity = Sale.validate_sale_quantity(quantity)
                valid_category = Sale.validate_total_sales(total)
                if check_name:
                    response = jsonify({"message": "Sale name already exists", "status_code": 400})
                    response.status_code = 400
                    return response

                elif valid_sale_name:
                    response = jsonify({"message": "Enter Sale name", "status_code": 400})
                    response.status_code = 400
                    return response

                elif valid_descr:
                    response = jsonify({"message": "Enter sale description", "status_code": 400})
                    response.status_code = 400
                    return response

                elif valid_quantity:
                    response = jsonify({"message": "Enter sale quantity", "status_code": 400})
                    response.status_code = 400
                    return response

                elif valid_category:
                    response = jsonify({"message": "Enter product category", "status_code": 400})
                    response.status_code = 400
                    return response

                else:
                    """create sales object"""
                    sale = Sale(name=name, description=description, quantity=quantity, total=total)
                    new_sale = sale.add_sale(name, description, quantity, total)
                    response = jsonify(new_sale)
                    response.status_code = 201
                    return response

            elif not name:
                response = jsonify({"message": "name is missing", "status_code": 400})
                response.status_code = 400
                return response

            elif not description:
                response = jsonify({"message": "description missing", "status_code": 400})
                response.status_code = 400
                return response

            elif not quantity:
                response = jsonify({"message": "quantity missing", "status_code": 400})
                response.status_code = 400
                return response

            else:
                response = jsonify({"message": "total is missing", "status_code": 400})
                response.status_code = 400
                return response

        else:
            # if its a get request
            sales = Sale.get_all_sales()
            print(sales)
            if not sales:
                response = jsonify({"message": "sale record not exist", "status": 200})
                response.status_code = 200

                response = jsonify({"message": "sale record does not exist", "status": 400})
                response.status_code = 400

                return response

            response = jsonify({"sales": sales})
            response.status_code = 200
            return response

    @app.route('/api/v1/sales/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def sale_RUD(id):
        """Fetches the id of a sale recprd and uses it to get the sale"""

        sale_found = Sale.find_sale_by_id(id)

        if request.method == "GET":
            if sale_found:
                response = jsonify({"product": sale_found})
                response.status_code = 200
                return response

            else:
                response = jsonify({"message": "sale record does not exist", "status": 404})
                response.status_code = 404
                return response

        elif request.method == "PUT":
            if sale_found:

                name = str(request.data.get('name', ''))
                description = str(request.data.get('description', ''))
                quantity = str(request.data.get('quantity', ''))
                total = str(request.data.get('total', ''))

                sale_found[0]["name"] = name
                sale_found[0]["description"] = description
                sale_found[0]["quantity"] = quantity
                sale_found[0]["total"] = total

                response = jsonify({"product": sale_found})
                response.status_code = 200
                return response

            else:
                response = jsonify({"message": "Cannot update a sale that does not exist", "status": 404})
                response.status_code = 404
                return response

        else:
            if sale_found:
                sales = Sale.get_all_sales()
                sales.remove(sale_found[0])
                response = jsonify({"product": "sale successfully deleted", "status": 200})
                response.status_code = 200
                return response
            else:
                response = jsonify({"message": "Cannot delete a sale that does not exist", "status": 404})
                response.status_code = 404
                return response

    @app.route('/api/v1/sales/<string:name>', methods=['GET', 'PUT'])
    def sale_manipulation_by_name(name):
        """get the id from the route"""
        """uses the name to find the sale record"""

        sale_found = Product.find_product_name(name)
        if not sale_found:
            """if no sale is found that matches the name"""
            response = jsonify({"message": "sale record does not exist", "status": 404})
            response.status_code = 404
            return response

        if request.method == "GET":
            if sale_found:
                response = jsonify({"Sale": sale_found})
                response.status_code = 200
                return response

            else:
                response = jsonify({"message": "sale does not exist", "status": 404})
                response.status_code = 404
                return response

        elif request.method == 'PUT':
            if sale_found:
                name = str(request.data.get('name', ''))
                description = str(request.data.get('description', ''))
                quantity = str(request.data.get('quantity', ''))
                total = str(request.data.get('total', ''))

                sale_found[0]["name"] = name
                sale_found[0]["description"] = description
                sale_found[0]["quantity"] = quantity
                sale_found[0]["total"] = total

                response = jsonify({"product": sale_found})
                response.status_code = 200
                return response

            else:
                response = jsonify({"message": "Cannot update sale that does not exist", "status": 404})
                response.status_code = 404
                return response

        else:
            if sale_found:

                sales = Sale.get_all_sales()
                sales.remove(sale_found[0])
                response = jsonify({"sale": "sale record successfully deleted", "status": 200})
                response.status_code = 200
                return response
            else:
                response = jsonify({"message": "Cannot delete sale that does not exist", "status": 404})
                response.status_code = 404
                return response
    return app


