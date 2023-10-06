from odoo import models, fields, api
import logging
import requests
import json

_logger = logging.getLogger(__name__)

class OzonCategory(models.Model):
    _description = 'Ozon Category Tree'
    _name = 'ozon.category'

    category_id = fields.Char()
    title = fields.Char()
    name = fields.Char(string='Name', related='title', store=True)
    product_id = fields.Many2one('product.product', string='Product', index=True, ondelete='cascade')
    parent_id = fields.Many2one('ozon.category', string='Parent Category', index=True, ondelete='cascade')
    child_id = fields.One2many('ozon.category', 'parent_id', string='Child Categories')



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
                self.category_tree_recursion_create(item['children'], category.id)



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
                self.env['ozon.category'].category_tree_recursion_create(res['result'])
                #print(res['result'])
                # Process the JSON content if it can be parsed
            except Exception as e:
                _logger.warning(
                    u'Failed to parse the JSON response: {}'.format(e))
                return 0
        else:
            # Handle the case where the request was not successful (status code is not 200)
            raise Warning('Request failed with status code: {}'.format(
                response.status_code))



class SomeCategory(models.Model):
    _description = 'Some tree'
    _name = 'ozon.category.some'

    name = fields.Char()
    title = fields.Char()
    product_id = fields.Many2one('product.product', string='Product', index=True, ondelete='cascade')
    category_id = fields.Many2one('ozon.category', string='Category', index=True, ondelete='cascade')

