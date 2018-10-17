import unittest
import json
from app.api.v1.models import Product
from app.api.v1 import create_app


class ProductTestCase(unittest.TestCase):
    product_url = '/api/v1/products'
    product_id_url = '/api/v1/products/{}'

    def setUp(self):
        # initialize our app
        self.app = create_app()
        # get the app test client
        self.client = self.app.test_client
        # data to use as test payload
        self.product = {"name": "Dining chair", "description": "Mahogany wood dining chair", "category": "furniture"}
        self.testProduct = {"name": "Dining table", "description": "Mahogany wood dining table ",
                            "category": "furniture"}

        # data for testing response when a field is missing
        self.product_name_missing = {"name": "", "description": "Mahogany wood dining chair", "category": "furniture",
                                     }
        self.product_description_missing = {"name": "Dining chair", "description": "", "category": "furniture"}
        self.product_category_missing = {"name": "Dining chair", "description": "Mahogany wood dining chair",
                                         "category": ""}

    def addProduct(self) -> object:
        """this method adds a product to the data structure"""
        product_url = '/api/v1/products'
        return self.client().post(product_url, data=self.product)

    def test_product_creation(self):
        # tests if the api can create a product
        add_product = self.client().post('/api/v1/products',
                                             data=json.dumps({"name": "Spoon", "description": "steel spoon", "category": "cutlery"}))

        self.assertEqual(add_product.status_code, 201)

    def test_api_can_get_all_products(self):
        # tests if the api can get all the products
        res = self.client().post(ProductTestCase.product_url, data=self.product)
        self.assertEqual(res.status_code, 201)
        res = self.client().get(ProductTestCase.product_url)
        self.assertEqual(res.status_code, 200)
        self.assertIn('Mahogany wood dining chair', str(res.data))

    def test_api_return_right_response_if_no_product_found(self):
        result = self.client().get(ProductTestCase.product_url)
        self.assertEqual(result.status_code, 400)
        self.assertIn("product does not exist", str(result.data))

    def test_api_can_get_product_by_id(self):
        self.addProduct()
        res = self.client().post(ProductTestCase.product_url, data=self.testProduct)

        self.assertEqual(res.status_code, 201)
        # convert response to json
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))

        # make get request and add the id
        get_request = self.client().get(ProductTestCase.product_id_url.format(result_in_json['id']))

        # assert the request status
        self.assertIn("Mahogany wood dining table", str(get_request.data))

    def test_api_can_edit_product(self):
        result = self.client().post('api/v1/products',
                                    data=json.dumps(dict(name="Spoon", description="steel spoon", category="cutlery")),
                                    content_type='application/json')
        self.assertEqual(result.status_code, 201)
        # get the json with the product
        results = json.loads(result.data.decode())
        result = self.client().put(
            '/api/v1/products/{}'.format(results['id']),
            data=json.dumps(dict(name="Plate", description="steel plate", category="cutlery")),
            content_type='application/json')
        self.assertEqual(result.status_code, 200)
        results = self.client().get(
            '/api/v1/products{}'.format(results['id']))
        self.assertIn('steel plate', str(results.data))

    def test_api_deletes_product(self):
        # test if api can delete a product
        res = self.client().post(ProductTestCase.product_url, data=self.product)

        self.assertEqual(res.status_code, 201)
        # convert response into json so as to get the id
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))

        # delete and pass in the id
        result = self.client().delete(ProductTestCase.product_id_url.format(result_in_json['id']))

        # self.assertEqual(result.status_code,200)
        # try to run get request for deleted product
        deleted_prod = self.client().get(ProductTestCase.product_id_url.format(result_in_json['id']))

        # should return 404
        self.assertEqual(deleted_prod.status_code, 404)

    def test_api_cannot_register_without_all_fields(self):
        res = self.client().post(ProductTestCase.product_url, data={"name": "dining table", "category": "furniture"})
        self.assertEqual(res.status_code, 400)

    def test_api_cannot_get_nonexistent_by_id(self):
        self.addProduct()
        result = self.client().get('/api/v1/products/10')
        self.assertEqual(result.status_code, 404)

    def test_api_cannot_delete_nonexistent_product(self):
        self.addProduct()

        # try to edit first product
        put_request = self.client().put('/api/v1/products/1',
                                        data={"name": "dining table", "description": "Mahogany wood dining table",
                                              "category": "furniture"})

        self.assertEqual(put_request.status_code, 200)
        self.assertIn("Mahogany wood dining table", str(put_request.data))

        # try to edit non existent product
        put_request = self.client().put('/api/v1/products/10',
                                        data={"name": "dining table", "description": "Mahogany wood dining table",
                                              "category": "furniture"})

        self.assertEqual(put_request.status_code, 404)

    def test_api_cannot_create_product_if_name_exists(self):
        self.addProduct()
        result = self.client().post(ProductTestCase.product_url,
                                    data={"name": "Dining chair", "description": "Mahogany wood dining chair",
                                          "category": "furniture"}
                                    )
        self.assertEqual(result.status_code, 400)

    def test_api_can_get_product_by_name(self):
        res = self.client().post(ProductTestCase.product_url, data=self.product)
        res.test = self.client().post(ProductTestCase.product_url, data=self.testProduct)

        self.assertEqual(res.status_code, 201)
        # convert response to json
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))

        # make get request and add the id
        get_request = self.client().get(ProductTestCase.product_id_url.format(result_in_json['name']))

        # assert the request status
        self.assertEqual(get_request.status_code, 200)

    def test_api_gives_error_if_name_missing(self):
        res = self.client().post(ProductTestCase.product_url, data=self.product_name_missing)
        self.assertEqual(res.status_code, 400)
        self.assertIn('name is missing', str(res.data))

    def test_api_gives_error_if_description_missing(self):
        res = self.client().post(ProductTestCase.product_url, data=self.product_description_missing)
        self.assertEqual(res.status_code, 400)
        self.assertIn('description missing', str(res.data))

    def test_api_gives_error_if_category_missing(self):
        res = self.client().post(ProductTestCase.product_url, data=self.product_category_missing)
        self.assertEqual(res.status_code, 400)
        self.assertIn('category is missing', str(res.data))

    def test_api_cannot_register_duplicate_names(self):
        self.addProduct()
        res = self.client().post(ProductTestCase.product_url,
                                 data=json.dumps(dict(name="Dining chair", description="Mahogany wood dining chair",
                                                      category="furniture")), content_type='application/json')
        self.assertEqual(res.status_code, 400)

    def test_api_cannot_register_product_with_empty_name(self):
        res = self.client().post(ProductTestCase.product_url,
                                 data={"name": "", "description": "Mahogany wood dining table",
                                       "category": "furniture"})
        self.assertEqual(res.status_code, 400)
        self.assertIn("name is missing", str(res.data))

    def test_api_cannot_register_product_with_empty_descr(self):
        res = self.client().post(ProductTestCase.product_url,
                                 data={"name": "dining table", "description": "",
                                       "category": "furniture"})
        self.assertEqual(res.status_code, 400)
        self.assertIn("description missing", str(res.data))

    def test_api_cannot_register_product_empty_category(self):
        res = self.client().post(ProductTestCase.product_url,
                                 data={"name": "dining table", "description": "Mahogany wood dining table",
                                       "category": ""})
        self.assertEqual(res.status_code, 400)
        self.assertIn("category is missing", str(res.data))

    def tearDown(self):
        """Runs after test and makes the product list empty"""
        Product.prod_list = []


if __name__ == "__main__":
        unittest.main()


