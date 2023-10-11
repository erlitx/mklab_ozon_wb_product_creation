import json
import requests
import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

# Template method to make any OZON API request
def ozon_api_request_template(self, url, data):
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
    print(f'***********data_json: {data_json}')
    response = requests.post(url, headers=headers, data=data_json)
    if response.status_code == 200:
        try:
            res = response.json()
            print(f'~~~~~~~~~~~~~~~res: {res}')
            return res
        except Exception as e:
            _logger.warning(
                u'Failed to parse the JSON response: {}'.format(e))
            return 0
    else:
        # Handle the case where the request was not successful (status code is not 200)
        raise Warning('Request failed with status code: {}'.format(
            response.status_code))