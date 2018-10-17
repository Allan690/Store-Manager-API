import unittest
import json
from app.api.v1.models import Sale
from app.api.v1 import create_app


class SalesTestCase(unittest.TestCase):
    sales_url = '/api/v1/sales'
    sales_id_url = '/api/v1/sales/{}'

    def setUp(self):
        # initialize our app
        self.app = create_app()
        # get the app test client
        self.client = self.app.test_client
        # data to use as test payload
        self.Sale = {"name": "Dining chair", "description": "Mahogany wood dining chair", "quantity": "50",
                     "total": "10000"}
        self.testSale = {"name": "Dining table", "description": "Mahogany wood dining table", "quantity": "50",
                         "total": "10000"}

    def addSales(self) -> object:
        """this method adds a sale to the data structure"""
        return self.client().post(SalesTestCase.sales_url, data=self.Sale)

    def test_sale_creation(self):
        # tests if the api can create a sale
        add_sale = self.client().post('/api/v1/sales',
                                      data=dict(name="Dining chair", description="Mahogany wood dining chair",
                                                quantity="50", total="10000"))

        self.assertEqual(add_sale.status_code, 201)

    def test_api_can_get_all_sales(self):
        # tests if the api can get all the sales
        res = self.client().post(SalesTestCase.sales_url, data=self.Sale)
        self.assertEqual(res.status_code, 201)
        res = self.client().get(SalesTestCase.sales_url)
        self.assertEqual(res.status_code, 200)
        self.assertIn('Mahogany wood dining chair', str(res.data))

    def test_api_return_right_response_if_no_sale_found(self):
        result = self.client().get(SalesTestCase.sales_url)
        self.assertEqual(result.status_code, 400)
        self.assertIn("sale does not exist", str(result.data))

    def test_api_can_get_sale_by_id(self):
        self.addSales()
        res = self.client().post(SalesTestCase.sales_url, data=self.testSale)

        self.assertEqual(res.status_code, 201)
        # convert response to json
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))

        # make get request and add the id
        get_request = self.client().get(SalesTestCase.sales_id_url.format(result_in_json['id']))

        # assert the request status
        self.assertIn("Mahogany wood dining table", str(get_request.data))

    def test_api_can_edit_sale(self):
        # tests if a the api can get a sale and edit it
        res = self.client().post(SalesTestCase.sales_url, data=self.Sale)

        self.assertEqual(res.status_code, 201)
        # convert response into json so as to get the id
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))

        # make a put request
        # this edits the current sale
        put_request = self.client().put(SalesTestCase.sales_id_url.format(result_in_json['id']),
                                        data={"name": "Dining chair", "description": "Mahogany wood dining chair",
                                              "quantity": "50",
                                              "total": "10000"})

        self.assertIn("Mahogany wood dining chair", str(put_request.data))

    def test_api_deletes_sale(self):
        # test if api can delete a sale
        res = self.client().post(SalesTestCase.sales_url, data=self.Sale)

        self.assertEqual(res.status_code, 201)
        # convert response into json so as to get the id
        result_in_json = json.loads(res.data.decode('utf-8').replace("'", "\""))

        # delete and pass in the id
        result = self.client().delete(SalesTestCase.sales_id_url.format(result_in_json['id']))

        # self.assertEqual(result.status_code,200)
        # try to run get request for deleted sale
        deleted_sale = self.client().get(SalesTestCase.sales_id_url.format(result_in_json['id']))

        # should return 404
        self.assertEqual(deleted_sale.status_code, 404)

    def test_api_cannot_register_without_all_fields(self):
        res = self.client().post(SalesTestCase.sales_id_url,
                                 data=dict(name="Dining chair", description="", quantity="50", total="10000"))
        self.assertEqual(res.status_code, 400)

    def test_api_cannot_get_nonexistent_by_id(self):
        self.addSales()
        result = self.client().get('/api/v1/sales/10')
        self.assertEqual(result.status_code, 404)

    def test_api_cannot_delete_nonexistent_sale(self):
        self.addSales()
        # try to edit first sale
        put_request = self.client().put('/api/v1/sales/1',
                                        data={"name": "dining table", "description": "Mahogany wood dining table",
                                              "category": "furniture"})

        self.assertEqual(put_request.status_code, 200)
        self.assertIn("Mahogany wood dining table", str(put_request.data))

        # try to edit non existent sale
        put_request = self.client().put('/api/v1/sales/10',
                                        data={"name": "dining table", "description": "Mahogany wood dining table",
                                              "category": "furniture"})

        self.assertEqual(put_request.status_code, 404)

    def test_api_cannot_create_sale_if_name_exists(self):
        self.addSales()
        result = self.client().post(SalesTestCase.sales_url,
                                    data={"name": "Dining chair", "description": "Mahogany wood dining chair",
                                          "quantity": "50",
                                          "total": "10000"}
                                    )
        self.assertEqual(result.status_code, 400)

    def tearDown(self):
        """Runs after test and makes the sales list empty"""
        Sale.sales_list = []


if __name__ == "__main__":
    unittest.main()
