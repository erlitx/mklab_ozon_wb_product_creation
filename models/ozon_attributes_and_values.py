from odoo import models, fields, api
import logging
import requests
import json

_logger = logging.getLogger(__name__)

class OzonAttributes(models.Model):
    _description = 'Some tree'
    _name = 'ozon.attribute'

    name = fields.Char()
    title = fields.Char()
    attribute_id = fields.Char(string="Attribute ID")
    description = fields.Char(string="Description")
    attribute_type = fields.Char(string="Attribute Type")
    is_collection = fields.Boolean(string="Is Collection")
    is_required = fields.Boolean(string="Is Required")
    group_id = fields.Char(string="Group ID")
    group_name = fields.Char(string="Group Name")
    dictionary_id = fields.Char(string="Dictionary ID")
    is_aspect = fields.Boolean(string="Is Aspect")
    category_depended = fields.Boolean(string="Category Depended")
    category_id = fields.Many2one('ozon.category', string='Category', index=True, ondelete='cascade')



class OzonAttributesValues(models.Model):
    _description = 'Some tree'
    _name = 'ozon.attribute.value'

    name = fields.Char()
    value = fields.Char(string="Value")
    info = fields.Char(string="Info")
    picture = fields.Char(string="Picture")
    attribute_id = fields.Many2one('ozon.attribute', string='Attributes Values', index=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', index=True, ondelete='cascade')



