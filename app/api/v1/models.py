import re


class Product(object):
    """Product model"""
    prod_list = []

    def __init__(self, name, description, category):
        self.id = len(Product.prod_list) + 1
        self.name = name
        self.description = description
        self.category = category

    def add_product(self, name, description, category):
        """This method add a dictionary to the product list"""
        """the dictionary contains details of the product"""

        new_prod = {"id": self.id, "name": name, "description": description, "category": category}
        Product.prod_list.append(new_prod)
        return new_prod

    @classmethod
    def get_all_products(cls):
        """This method will return all products in the products list
                print(cls.prod_list)"""
        return cls.prod_list

    @classmethod
    def find_product_by_id(cls, id):
        """This method returns product in product list based on supplied id"""
        prod = [prod for prod in cls.prod_list if prod['id'] == id]
        print(prod)
        return prod

    @classmethod
    def check_product_name_exists(cls, name):
        """This method checks if a product name exists in the product list"""
        for prod in cls.prod_list:
            if prod.get("name") == name or prod.get("name") == name.lower() or prod.get(
                    "name") == name.upper():
                return True
            return False

    @classmethod
    def find_product_name(cls, name):
        """This method will return a product that matches the supplied name"""
        prod = [prod for prod in cls.prod_list if prod['name'] == name]
        print(prod)
        return prod

    @staticmethod
    def validate_product_name(name):
        if not re.match(r"^[A-Za-z0-9\.\+_-]*$", name):
            return True
        return False

    @staticmethod
    def validate_product_description(description):
        if not re.match(r"^[A-Za-z0-9\.\+_-]*$", description):
            return True
        return False

    @staticmethod
    def validate_category_name(name):
        if not re.match(r"^[A-Za-z0-9\.\+_-]*$", name):
            return True
        return False


class Sale(object):
    """Sales model"""
    sales_list = []

    def __init__(self, name, description, quantity, total):
        self.id = len(Sale.sales_list) + 1
        self.name = name
        self.description = description
        self.quantity = quantity
        self.total = total

    def add_sale(self, name, description, quantity, total):
        """This method add a sales record dictionary to the sales list"""

        new_sale = {"id": self.id, "name": name, "description": description, "quantity": quantity, "total": total}

        Sale.sales_list.append(new_sale)
        return new_sale

    @classmethod
    def get_all_sales(cls):
        """This method will return all sales in the sales list
                print(cls.sales_list)"""
        return cls.sales_list

    @classmethod
    def find_sale_by_id(cls, id):
        """This method returns a sale in sales list based on supplied id"""

        sale = [sale for sale in cls.sales_list if sale['id'] == id]
        print(sale)
        return sale

    @classmethod
    def check_sale_name_exists(cls, name):
        """This method checks if a sales name exists in the sales list"""
        for sale in cls.sales_list:
            if sale.get("name") == name or sale.get("name") == name.lower() or sale.get(
                    "name") == name.upper():
                return True
            return False

    @classmethod
    def find_sale_name(cls, name):
        """This method will return a sale record that matches the supplied name"""
        sale = [sale for sale in cls.sales_list if sale['name'] == name]
        print(sale)
        return sale

    @staticmethod
    def validate_sale_name(name):
        if not re.match(r"^[A-Za-z0-9\.\+_-]*$", name):
            return True
        return False

    @staticmethod
    def validate_sale_description(description):
        if not re.match(r"^[A-Za-z0-9\.\+_-]*$", description):
            return True
        return False

    @staticmethod
    def validate_sale_quantity(quantity):
        if not re.match(r"^[A-Za-z0-9\.\+_-]*$", quantity):
            return True
        return False

    @staticmethod
    def validate_category_name(name):
        if not re.match(r"^[A-Za-z0-9\.\+_-]*$", name):
            return True
        return False

    @staticmethod
    def validate_total_sales(total):
        if not re.match(r"^[A-Za-z0-9\.\+_-]*$", total):
            return True
        return False


class User(object):
    """
   This class creates a user model
    """
    """ the user list will contain a dictionary of created users"""
    user_list = []

    def __init__(self, username, email, password, confirm_password):
        self.username = username
        self.email = email
        self.password = password
        self.confirm_password = confirm_password

    def create_user(self, email, password, confirm_password):
        """
        this method gets user details as parameters,
        uses them to create a dict and append dict
        to the user_list
        """
        new_user = {"email": email, "password": password, "confirm_password": confirm_password}

        if new_user["password"] == new_user["confirm_password"]:
            User.user_list.append(new_user)

            message = "User has been added successfully."
            return message

        message = "password must match the confirm_password"
        return message

    @classmethod
    def login(cls, email, password):
        """This method logs in user after checking for existence in user list"""
        for user in cls.user_list:
            if user["email"] == email and user["password"] == password:
                message = "you have successfully logged in"
                return message

            message = "username or email is invalid"
            return message

    @classmethod
    def check_email_exists(cls, email):
        """validates email to avoid two accounts with same user email"""
        for user in cls.user_list:
            if user.get("email") == email:
                return True

            return False

    @classmethod
    def check_name_exists(cls, username):
        """validate username to avoid two accounts with same username"""
        for user in cls.user_list:
            if user.get("username") == username:
                return True

            return False

    @staticmethod
    def validate_password(password):
        if len(password) < 6:
            return True

        return False

    @staticmethod
    def reset_password(email, password, confirm_password):
        """This method resets a user's password"""
        for user in User.user_list:
            if user["email"] == email:
                if password == confirm_password:
                    user["password"] = password
                    user["confirm_password"] = confirm_password
                    message = "Password reset successfully!"
                    return message

                else:
                    message = "Password and confirm password must be the same"
                    return message
            else:
                message = "Sorry, this account does not exist"
                return message

    @staticmethod
    def validate_email(email):
        """This method uses a regular expression to validate email entered by user"""
        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
            return True
        return False

    @staticmethod
    def validate_password_format(password):
        """This method uses a reg expression to validate user password"""
        if not re.match(r"^[A-Za-z0-9\.\+_-]*$", password):
            return True
        return False
