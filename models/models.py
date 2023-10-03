# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class mklab_ozonwb_product_creation(models.Model):
#     _name = 'mklab_ozonwb_product_creation.mklab_ozonwb_product_creation'
#     _description = 'mklab_ozonwb_product_creation.mklab_ozonwb_product_creation'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
