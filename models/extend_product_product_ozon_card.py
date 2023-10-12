from odoo import models, fields, api
from odoo.exceptions import UserError
from . import ozon_api
import json



class ProductOzonTemplate(models.Model):
    _description = 'Extension to product with Ozon template fields'
    _inherit = 'product.product'

    ozon_category_tree = fields.Many2one('ozon.category', string="Ozon Category", ondelete='cascade',
                                          domain=[('child_id', '=', False)])
    category_readonly = fields.Boolean(compute='_read_only_tree')
    #ozon_attribute_id = fields.Many2one('ozon.attribute', string="Ozon Attribute", ondelete='cascade')
    #ozon_attribute_line = fields.One2many('ozon.attribute', 'product_many_ids', string="Ozon Attribute Line")
    #ozon_attribute_line = fields.One2many('ozon.attribute', 'product_id', string="Ozon Attribute Line")
    ozon_attribute_line = fields.Many2many('ozon.attribute', string="Ozon Attribute Line")

    ozon_product_name = fields.Char(string='Имя на Ozon')
    ozon_offer_id = fields.Char(string='Артикул Товара')
    ozon_barcode = fields.Char(string='Штрихкод')
    ozon_price = fields.Char(string='Цена на Ozon')
    ozon_price_currency = fields.Char(string='Валюта', default='RUB')
    ozon_primary_image = fields.Char(string='Основное изображение')
    ozon_images = fields.Text(string='Дополнительные изображения')
    ozon_dimension_units = fields.Char(string='Единицы измерения', default='mm')
    ozon_height = fields.Char(string='Высота в мм')
    ozon_width = fields.Char(string='Ширина в мм')
    ozon_depth = fields.Char(string='Глубина в мм')
    ozon_weight_units = fields.Char(string='Единицы измерения веса', default='g')
    ozon_weight = fields.Char(string='Вес в граммах')
    ozon_vat = fields.Selection(string='НДС', selection=[('0.2', '20%'), ('0.1', '10%'), ('0', '0%')], default='0.2')
    ozon_last_upload_task_id = fields.Char(string='ID последней загрузки')

    #Display message
    def update_category_tree(self):
        self.env['ozon.category'].get_ozon_catalog_tree()


    # Make 'ozon_category_tree' readonly if the product is new to prevent an Error 
    # when category is selected anf onchange method is called
    @api.onchange('name')
    def _read_only_tree(self):
        if str(self.id).startswith('NewId'):
            self.category_readonly = True  # Make the field readonly
        else:
            self.category_readonly = False

    # Fill the fields with the values from the product
    def fill_the_fields(self):
        self.ozon_product_name = self.name
        self.ozon_offer_id = self.default_code
        self.ozon_barcode = self.barcode
        self.ozon_price = self.lst_price
        self.ozon_weight = int(float(self.weight * 1000))

    # Make images URL in the format required by Ozon API
    def process_ozon_images(self):
        ozon_images = self.ozon_images
        if ozon_images:
            print(f'--------ozon_images: {ozon_images}')
            ozon_images = ozon_images.replace(" ", "")
            ozon_images = ozon_images.replace("\n", "")
            image_list = ozon_images.split(',')
        else:
            image_list = []
        return image_list

    # Upload product to Ozon
    def upload_product_to_ozon(self):
        url = "https://api-seller.ozon.ru/v2/product/import"
        attributes_list = []
        for attribute in self.ozon_attribute_line:
            attribute_item = {
                "complex_id": 0,
                "id": int(attribute.attribute_id),
                "values": [{"dictionary_value_id": int(attribute.value_ids.ozon_value_id), "value": attribute.value_ids.name}]
                }
            attributes_list.append(attribute_item)
        for item in attribute_item['values']:
            if item['dictionary_value_id'] == False:
                item.pop('dictionary_value_id')
        data = {
            "items": [
                {
                    "barcode": self.ozon_barcode,
                    "category_id": int(self.ozon_category_tree.category_id),
                    "complex_attributes": [],
                    "currency_code": self.ozon_price_currency,
                    "depth": int(self.ozon_depth),
                    "dimension_unit": self.ozon_dimension_units,
                    "height": int(self.ozon_height),
                    "images": self.process_ozon_images(),
                    "name": self.ozon_product_name,
                    "offer_id": self. ozon_offer_id,
                    "price": self.ozon_price,
                    "primary_image": "",
                    "vat": self.ozon_vat,
                    "weight": int(self.ozon_weight),
                    "weight_unit": self.ozon_weight_units,
                    "width": int(self.ozon_width),

                    "attributes": attributes_list
                }
            ]
        }
        try:
            res = ozon_api.ozon_api_request_template(self=self, url=url, data=data)
            self.message_post(body="Карточка товара загружена на Ozon")
            if res["result"]["task_id"]:
                self.ozon_last_upload_task_id = res["result"]["task_id"]
            return res["result"]
        except:
            raise UserError('Ошибка загрузки карточки товара на Ozon')
        

    # Get the status of the last upload task and post a message
    def get_task_info(self):
        url = "https://api-seller.ozon.ru/v1/product/import/info"
        data = {"task_id": self.ozon_last_upload_task_id}
        try:
            res = ozon_api.ozon_api_request_template(self=self, url=url, data=data)
            if res['result']['items'][0]['status'] == 'imported' and res['result']['items'][0]['errors'] == []:
                self.message_post(body="Карточка товара загружена на Ozon")
                reply = f"Товар был успешно загружен на Ozon: \n - product_id:\
                      {res['result']['items'][0]['product_id']}"\
                      f"\n - task_id: {self.ozon_last_upload_task_id}"
                self.message_post(body=reply)
        except:
            raise UserError('Ошибка загрузки карточки товара на Ozon')


    def ozon_get_category_tree(self):
        pass

    # Update the Attribute records and Attribute Value records from Ozon API
    # Populate the One2many field 'ozon_attribute_line' with the attributes recieved
    @api.onchange('ozon_category_tree')
    def ozon_get_attributes(self):
        try:
            print(f'***********Category ID ONCHANGE {self.ozon_category_tree.category_id}')

            if self.ozon_category_tree.category_id == False :
                empty_list = {}
                print(f'---EMPTY LIST')
                return empty_list
            
            get_attributes = self.env['ozon.category'].ozon_get_attributes(self.ozon_category_tree.category_id)

            # Populate the One2many field 'ozon_attribute_line' with the attributes in a 'lines' list

            # First check if there are any records already in 'ozon.attribute' model 
            # with the same Ozon category ID user selected in the 'ozon_category_tree' field
            category_record = self.env['ozon.category'].search([('category_id', '=', self.ozon_category_tree.category_id)])

            # Get the list of Ids already existing records in the 'ozon.attribute' model
            attribute_values_ids = self.env['ozon.attribute'].search([('category_id', '=', category_record.id)]).ids
            #print(f'***********Attribute Values found: {attribute_values_ids}')

            #Iterate through the list of attributes and add them to the 'lines' list
            if attribute_values_ids:
                print("***********Existing attributes found****************")
                lines = [(5, 0, 0)]
                for category_id in attribute_values_ids:
                    #print(f'***********Existing category found: {category_id}')
                    lines.append((4, category_id, 0))
                    attribute_line = self.env['ozon.attribute'].browse(category_id)

                    #### Populate product_many_ids
                    # The list with Ids of all the products associated with this attribute record
                    products_ids_to_add = attribute_line.product_many_ids.ids
                    # Convert the list to a set to eliminate duplicates
                    products_ids_set = set(products_ids_to_add)
                    # Add the new ID to the set
                    products_ids_set.add(self._origin.id)
                    # Convert the set back to a list
                    products_ids_to_add = list(products_ids_set)
                    attribute_line.write({'product_many_ids': [(6, 0, products_ids_to_add)]})
                    # Now the 'lines' list contains the Ids of the existing records 
                    # in the 'ozon.attribute' model
                    
            # If there are no attributes in the One2many field, create a new list of attributes
            else:
                print("***********No existing attributes found****************")
                lines = [(5, 0, 0)]
                for attribute in get_attributes:
                    vals = {"product_id": self._origin.id, 
                            "attribute_id": attribute['id'],
                            "name": attribute['name'], 
                            "is_required": attribute['is_required'], 
                            "is_collection": attribute['is_collection'], 
                            "type": attribute['type'], 
                            "description": attribute['description'], 
                            "group_id": attribute['group_id'], 
                            "group_name": attribute['group_name'], 
                            "dictionary_id": attribute['dictionary_id'], 
                            "is_aspect": attribute['is_aspect'], 
                            "category_id": self.ozon_category_tree.id,
                            }

                    ##### Create a attribute records 
                    attribute_line = self.env['ozon.attribute'].create(vals)
                    #### Append lines with this records
                    lines.append((4, attribute_line.id, 0))

                    #### Create ozon.attribute.values for each attribute
                    ### Get attribute.values by Ozon API
                    #Check if attribute 'dictionary_id' is not 0
                    if attribute['dictionary_id'] != 0:
                        attribute_values = self.env['ozon.category'].ozon_get_attributes_value(
                                                                                self.ozon_category_tree.category_id, 
                                                                                attribute['id']
                                                                                )
                        print(f'-----attribute_values: {attribute_values}')
                        for value in attribute_values:

                            self.env['ozon.attribute.value'].create(
                                {'attribute_id': [attribute_line.id], 
                                'name': value['value'],
                                'ozon_value_id': value['id'],}
                                )
            # Inser records into Many2many field
            self.ozon_attribute_line = lines
        except Exception as e:
            raise UserError('Ошибка получения атрибутов с Ozon')