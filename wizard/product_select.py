from odoo import api, exceptions, fields, models
import logging
import requests
import pprint


_logger = logging.getLogger(__name__)

class ProductSelect(models.TransientModel):
    _name = "product.ozonwb.select"
    _description = "Select products to create on Ozon and Wildberries"

    state = fields.Selection([('draft', 'Draft'), ('done', 'Done'), ('connected', 'Connected')], string='State', default='draft')
    product_ids = fields.Many2many('product.product', string='Product')


    @api.model
    def default_get(self, field_names):
        try:
            defaults_dict = super().default_get(field_names)
            # Add values to the defaults_dict here
            print(f'----INFO[default_dicts: {defaults_dict}')
            
            product_ids = self.env.context["active_ids"]
            print(f'----INFO[checkout_ids: {product_ids}')
            
            defaults_dict["product_ids"] = [(6, 0, product_ids)]
            return defaults_dict
        except Exception as e:
            raise exceptions.UserError("Error in default_get: {}".format(e))

    def upload_to_ozon(self):
        print(f'-----self.product_ids: {self.product_ids}')
        for product_id in self.product_ids:
            print(f'-----product_id: {product_id.name}')
            product = self.env['product.product'].search([('id', '=', product_id.id)])
            pprint.pprint(f"-----product: {self.env['product.product'].browse(product_id.id).read()}")





    # def default_get(self, field_names):
    #     defaults = super(TelegramAuth, self).default_get(field_names)
    #     app_id=self.env.context['active_id'] 
    #     telegram_client = self.env['telegram.client'].search([ ('id', '=', app_id)])
    #     defaults['phone_number'] = telegram_client.phone_number
    #     defaults['api_id'] = telegram_client.api_id
    #     defaults['api_hash'] = telegram_client.api_hash
    #     defaults['session_name'] = telegram_client.session_name
    #     defaults['server_url'] = telegram_client.server_url
    #     return defaults


    # THIS METHOD ALLOW TO REMAIN WIZARD FORM STAY CLOSED AFTER BUTTON CLICK
    # return self._reopen_form() should be used in a method of the button
    # def _reopen_form(self):
    #     self.ensure_one()        
    #     print(f'************************************')
    #     return {
    #     'name': "Paste an SMS or PUSH notification code you've recieved",
    #     'type': 'ir.actions.act_window',
    #     'view_type': 'form',
    #     'view_mode': 'form',
    #     'res_model': self._name,
    #     'target': 'new',
    #     'res_id': self.id,
    #     'context': self.env.context,
    # }

    # def get_code(self):
    #     try:
    #         self.ensure_one()
    #         self.state = 'done'
    #         url = self.server_url + 'sms_code_request' #URL for POST request
    #         # Sending all Telegram keys in the body of POST request
    #         params = {
    #             "session_name": self.session_name,
    #             "api_id": self.api_id,
    #             "api_hash": self.api_hash,
    #             "phone_number": self.phone_number,
                
    #         }
    #         print(f'----INFO[get_code(self)]: {url}------{params}')
    #         headers = {"Content-Type": "application/json"}
    #         response = requests.post(url, params=params, headers=headers)
    #         data = response.json()
    #         print(f'----INFO[get_code(self)]: {data}')
    #         self.phone_hash = data.get('phone_hash', '')
    #     except:
    #         print(f'MORE THEN ONE RECORD SELECTED')
    #     return self._reopen_form()