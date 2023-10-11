from odoo import models, fields, api
import logging
import requests
import json

_logger = logging.getLogger(__name__)


class OzonCategory(models.Model):
    _description = 'Ozon Category Tree'
    _name = 'ozon.category'

    category_id = fields.Char()
    name = fields.Char(string='Name', compute="_get_name", stored=True, index=True)
    title = fields.Char()
    #product_id = fields.Many2one('product.product', string='Product', index=True, ondelete='cascade')
    product_id = fields.Many2many('product.product', string='Product', index=True, ondelete='cascade')
    parent_id = fields.Many2one('ozon.category', string='Parent Category', index=True, ondelete='cascade')
    child_id = fields.One2many('ozon.category', 'parent_id', string='Child Categories')


    @api.depends('category_id', 'title')
    def _get_name(self):
        for record in self:
            display_name = f"{record.category_id} - {record.title}"
            record.name = display_name


    # A recursion method to get and save all the categories from the Ozon API
    def category_tree_recursion_create(self, json_data, parent_id=None):
        for item in json_data:
            values = {
                'category_id': item['category_id'],
                'title': item['title'],
                'parent_id': parent_id,
            }
            category = self.create(values)
            print(f'***********Category found: {values}')

            if item['children']:
                self.category_tree_recursion_create(
                    item['children'], category.id)


    # Template method to make any OZON API request
    def ozon_api_request_template(self, url, data):
        print(f'***********data: {data}********* {url}')
        if data['category_id'] == [False]:
            print(f'--------- RETURNED 0')
            return 0
        url = url
        data = data
        company = self.env.company
        headers = {
            'Host': 'api-seller.ozon.ru',
            'Client-Id': company.client_id_ozon,
            'Api-Key': company.apikey_ozon,
            'Content-Type': 'application/json'
        }
        data_json = json.dumps(data)
        #print(f'***********data_json: {data_json}')
        response = requests.post(url, headers=headers, data=data_json)
        if response.status_code == 200:
            try:
                res = response.json()
                return res
            except Exception as e:
                _logger.warning(
                    u'Failed to parse the JSON response: {}'.format(e))
                return 0
        else:
            # Handle the case where the request was not successful (status code is not 200)
            raise Warning('Request failed with status code: {}'.format(
                response.status_code))


    # Get the CATEGORIES from the Ozon API
    def get_ozon_catalog_tree(self):
        url = "https://api-seller.ozon.ru/v2/category/tree"
        data = {"language": "DEFAULT"}
        company = self.env.company
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
            try:
                res = response.json()
                self.env['ozon.category'].category_tree_recursion_create(
                    res['result'])
                # print(res['result'])
                # Process the JSON content if it can be parsed
            except Exception as e:
                _logger.warning(
                    u'Failed to parse the JSON response: {}'.format(e))
                return 0
        else:
            # Handle the case where the request was not successful (status code is not 200)
            raise Warning('Request failed with status code: {}'.format(
                response.status_code))


    # Get the ATTRIBUTES from the Ozon API
    def ozon_get_attributes(self, category_id):
        
        url = "https://api-seller.ozon.ru/v3/category/attribute"
        data = {
            "attribute_type": "REQUIRED",
            "category_id": [category_id],
            "language": "DEFAULT"
        }
        res = self.ozon_api_request_template(url, data)
        for attr in res["result"][0]["attributes"]:
            print(f'=========={attr}')

        attributes = res["result"][0]["attributes"]
        return attributes


    # Get the ATTRIBUTE VALUES from the Ozon API
    def ozon_get_attributes_value(self, category_id, attribute_id):
        url = "https://api-seller.ozon.ru/v2/category/attribute/values"
        data = {
                "attribute_id": attribute_id,
                "category_id": int(category_id),
                "language": "DEFAULT",
                "last_value_id": 0,
                "limit": 100
        }
        res = self.ozon_api_request_template(url, data)
        if attribute_id == 85:
            print(f'=====LENGHT====={len(res["result"])}')

        return res["result"]