from odoo import api, exceptions, fields, models
import logging
import requests
import pprint
import json


_logger = logging.getLogger(__name__)


class ProductSelect(models.Model):
    _name = "product.ozonwb.select"
    _description = "Select products to create on Ozon and Wildberries"

    state = fields.Selection([('draft', 'Draft'), ('done', 'Done'),
                             ('connected', 'Connected')], string='State', default='draft')
    task_id = fields.Char(string='Task ID')
    product_ids = fields.Many2many('product.product', string='Product')
    message = fields.Text('Message')

    @api.model
    def default_get(self, field_names):
        try:
            defaults_dict = super().default_get(field_names)
            # Add values to the defaults_dict here
           # print(f'----INFO[default_dicts: {defaults_dict}')

            product_ids = self.env.context["active_ids"]
            # print(f'----INFO[checkout_ids: {product_ids}')

            defaults_dict["product_ids"] = [(6, 0, product_ids)]
            return defaults_dict
        except Exception as e:
            raise exceptions.UserError("Error in default_get: {}".format(e))


    def get_products_from_ozon(self):
        url = "https://api-seller.ozon.ru/v2/product/list"
        data = {
            "filter": {
                "visibility": "ALL"
            },
            "last_id": "",
            "limit": 3
        }
        company = self.env.company
        print(f'======company1: {company.read(["name"])}')
        print(f'======company2: {company.client_id_ozon}')
        headers = {
            'Host': 'api-seller.ozon.ru',
            'Client-Id': company.client_id_ozon,
            'Api-Key': company.apikey_ozon,
            'Content-Type': 'application/json'
        }

        data_json = json.dumps(data)
        response = requests.post(url, headers=headers, data=data_json)
        if response.status_code == 200:
            response_content = response.text  # Use .text or .content to access the content
            print(f'***********Response Content: {response_content}')
            try:
                res = response.json()
                # Process the JSON content if it can be parsed
            except Exception as e:
                _logger.warning(
                    u'Failed to parse the JSON response: {}'.format(e))
                return 0
        else:
            # Handle the case where the request was not successful (status code is not 200)
            raise Warning('Request failed with status code: {}'.format(
                response.status_code))

    def upload_product_to_ozon(self):
        url = "https://api-seller.ozon.ru/v2/product/import"
        data = {
            "items": [
                {
                    "attributes": [
                        {
                            "complex_id": 0,
                            "id": 85,
                            "values": [{"value": "Нет бренда"}]
                        },
                        {
                            "complex_id": 0,
                            "id": 9048,
                            "values": [
                                {
                                    "value": "Тестовый товар"
                                }
                            ]
                        },
                        {
                            "complex_id": 0,
                            "id": 8229,
                            "values": [
                                {
                                    "dictionary_value_id": 92917,
                                    "value": "Набор для опытов"
                                }
                            ]
                        },

                    ],
                    "barcode": "",
                    "category_id": 17035533,
                    "complex_attributes": [],
                    "currency_code": "RUB",
                    "depth": 10,
                    "dimension_unit": "mm",
                    "height": 250,
                    "images": [],
                    "name": "Тестовый товар 3",
                    "offer_id": "AMP-TEST-3",
                    "price": "1000",
                    "primary_image": "",
                    "vat": "0.20",
                    "weight": 100,
                    "weight_unit": "g",
                    "width": 150
                }
            ]
        }
        company = self.env.company
        print(f'======company1: {company.read(["name"])}')
        print(f'======company2: {company.client_id_ozon}')
        headers = {
            'Host': 'api-seller.ozon.ru',
            'Client-Id': company.client_id_ozon,
            'Api-Key': company.apikey_ozon,
            'Content-Type': 'application/json'
        }

        data_json = json.dumps(data)
        response = requests.post(url, headers=headers, data=data_json)
        if response.status_code == 200:
            response_content = response.text  # Use .text or .content to access the content
            print(f'***********Response Content: {response_content}')
            try:
                res = response.json()
                # Process the JSON content if it can be parsed
            except Exception as e:
                _logger.warning(
                    u'Failed to parse the JSON response: {}'.format(e))
                return 0
        else:
            # Handle the case where the request was not successful (status code is not 200)
            raise Warning('Request failed with status code: {}'.format(
                response.status_code))

################################################
    def get_product_info(self):
        url = "https://api-seller.ozon.ru/v2/product/info"
        data = {
            # "offer_id": "",
            "product_id": 231734359,
            # "sku": 0
        }
        company = self.env.company
        print(f'======company1: {company.read(["name"])}')
        print(f'======company2: {company.client_id_ozon}')
        headers = {
            'Host': 'api-seller.ozon.ru',
            'Client-Id': company.client_id_ozon,
            'Api-Key': company.apikey_ozon,
            'Content-Type': 'application/json'
        }

        data_json = json.dumps(data)
        response = requests.post(url, headers=headers, data=data_json)
        if response.status_code == 200:
            response_content = response.text  # Use .text or .content to access the content
            print(f'***********Response Content: {response_content}')
            try:
                res = response.json()
                # Process the JSON content if it can be parsed
            except Exception as e:
                _logger.warning(
                    u'Failed to parse the JSON response: {}'.format(e))
                return 0
        else:
            # Handle the case where the request was not successful (status code is not 200)
            raise Warning('Request failed with status code: {}'.format(
                response.status_code))

################################################
    def get_task_info(self):
        url = "https://api-seller.ozon.ru/v1/product/import/info"
        data = {"task_id": self.task_id}
        company = self.env.company
        print(f'======company1: {company.read(["name"])}')
        print(f'======company2: {company.client_id_ozon}')
        headers = {
            'Host': 'api-seller.ozon.ru',
            'Client-Id': company.client_id_ozon,
            'Api-Key': company.apikey_ozon,
            'Content-Type': 'application/json'
        }

        data_json = json.dumps(data)
        response = requests.post(url, headers=headers, data=data_json)
        if response.status_code == 200:
            response_content = response.text  # Use .text or .content to access the content
            print(f'***********Response Content: {response_content}')
            try:
                res = response.json()
                # Process the JSON content if it can be parsed
            except Exception as e:
                _logger.warning(
                    u'Failed to parse the JSON response: {}'.format(e))
                return 0
        else:
            # Handle the case where the request was not successful (status code is not 200)
            raise Warning('Request failed with status code: {}'.format(
                response.status_code))

################################################

