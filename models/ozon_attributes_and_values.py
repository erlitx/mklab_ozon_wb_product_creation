from odoo import models, fields, api
import logging
import requests
import json

_logger = logging.getLogger(__name__)

class OzonAttributes(models.Model):
    _description = 'ozon.attribute'
    _name = 'ozon.attribute'

    name = fields.Char()
    title = fields.Char()
    attribute_id = fields.Char(string="Attribute ID")
    description = fields.Char(string="Description")
    type = fields.Char(string="Attribute Type")
    is_collection = fields.Boolean(string="Is Collection")
    is_required = fields.Boolean(string="Is Required")
    group_id = fields.Char(string="Group ID")
    group_name = fields.Char(string="Group Name")
    dictionary_id = fields.Char(string="Dictionary ID")
    is_aspect = fields.Boolean(string="Is Aspect")
    category_depended = fields.Boolean(string="Category Depended")
    category_id = fields.Many2one('ozon.category', string='Category Id', index=True,)
    product_id = fields.Many2one('product.product', string='Product', )
    product_many_ids = fields.Many2many(
            comodel_name='product.product',  # Name of the related model
            relation='product_product_to_many_attributes',  # Name of the intermediary table
            column1='attribute_id_comodel',  # Name of the column for the current model's IDs in the intermediary table
            column2='product_product_comodel',  # Name of the column for the related model's IDs in the intermediary table
            string='Product IDs',  # Label for the field in forms and views
            help='Help text for the field',  # Help text displayed with the field
            )

    value_ids = fields.Many2one('ozon.attribute.value', string='Value_ids',
                                domain="[('attribute_id', 'in', id)]")
    #value_ids = fields.One2many('ozon.attribute.value', 'attribute_id', string='Attribute Values',)


    @api.onchange('category_id')
    def _onchange_category_id(self):
        print(f'***********Category ID ONCHANGE')
        # Clear existing values in the Many2many field
        #self.value_ids = [(5, 0, 0)]
        #values = self.env['ozon.attribute.value'].search([('name', '=', 'Бренд')])
        #print(f'***********Values found: {values}')
        #self.value_ids = values

        # # Add values from the related category's attribute values
        # if self.category_id:
        #     category_values = self.category_id.value_ids.filtered(lambda v: v.attribute_id == self)
        #     self.value_ids = [(4, value.id) for value in category_values]

    def write(self, vals):
      #  print(f'***********Write1: {vals}')
        new_rec = super().write(vals)
       # print(f'***********Write2: {vals}')

    def create(self, vals):
    #    print(f'***********Create1: {vals}')
        # for val in vals:
        #     val['product_many_ids'] = [(6, 0, [18])]
        #print(f'***********Create2: {vals}')
        try:
            new_rec = super().create(vals)
           # print(f'***********Create2: {vals}')
           # print(f'***********NEW REC: {new_rec}')
            return new_rec
        except Exception as e:
            print(f'***********Create3: {vals}')
    
    def unlink(self):
        print(f'***********Unlink1: {self}')
        res = super().unlink()
        print(f'***********Unlink2: {self}')
        return res


class OzonAttributesValues(models.Model):
    _description = 'Some tree'
    _name = 'ozon.attribute.value'

    ozon_value_id = fields.Char(String="Ozon Value ID")
    name = fields.Char()
    title = fields.Char()
    value = fields.Char(string="Value")
    info = fields.Char(string="Info")
    picture = fields.Char(string="Picture")
    #attribute_id = fields.Many2one('ozon.attribute', string='Attributes Values', index=True)
    attribute_id = fields.Many2many('ozon.attribute', string='Attributes Values', index=True)
    #attribute_id = fields.One2many('ozon.attribute', 'value_ids', string='Attributes Values', index=True)
    #product_id = fields.Many2one('product.product', string='Product', index=True, ondelete='cascade')


    def create(self, vals):
        print(f'***********Create1(values): {vals}')
        # for val in vals:
        #     val['product_many_ids'] = [(6, 0, [18])]
        #print(f'***********Create2: {vals}')
        try:
            new_rec = super().create(vals)
           # print(f'***********Create2: {vals}')
           # print(f'***********NEW REC: {new_rec}')
            return new_rec
        except Exception as e:
            print(f'***********Create3: {vals}')
