from odoo import models, fields, api


class ProductOzonTemplate(models.Model):
    _description = 'Extension to product with Ozon template fields'
    _inherit = 'product.product'



    def _selection_tree(self):
        category_id = self.selection_field
        print(f'category_id: {category_id:=^30}')
        selection_list = [('1111', '6'), ('222', '7'), ('333', '8')]
        return  selection_list

    ozon_product_category = fields.Char()
    ozon_required_attributes = fields.Char()
    selection_field = fields.Char(string='Choose category')
    #ozon_category_tree = fields.Many2one('ozon.category', string="Ozon Category", ondelete='cascade')
    #ozon_category_tree = fields.One2many(comodel_name='ozon.category', inverse_name='product_id', 
                                         # string="Ozon Category")
    ozon_category_tree = fields.One2many('ozon.category.some', 'product_id', index=True, copy=True, auto_join=True, string="Ozon Category")
    #sale_order = fields.One2many('sale.order', 'order_id', string="Sale" )


    def ozon_get_category_tree(self):
        # records_to_delete = self.env['ozon.category'].search([])
        # if records_to_delete:
        #     records_to_delete.unlink()
        #get_tree = self.env['ozon.category'].get_ozon_catalog_tree()
        pass
