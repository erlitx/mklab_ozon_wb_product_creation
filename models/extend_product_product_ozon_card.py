from odoo import models, fields, api


class ProductOzonTemplate(models.Model):
    _description = 'Extension to product with Ozon template fields'
    _inherit = 'product.product'

    ozon_required_attributes = fields.Char()
    selection_field = fields.Char(string='Choose category')
    ozon_category_tree = fields.Many2one('ozon.category', string="Ozon Category", ondelete='cascade', domain=[('child_id', '=', False)])
    ozon_attribute_id = fields.Many2one('ozon.attribute', string="Ozon Attribute", ondelete='cascade')
    ozon_attribute_line = fields.One2many('ozon.attribute.value', 'product_id', string="Ozon Attribute Line")


    @api.onchange('ozon_category_tree')
    def _onchange_category_tree(self):
        lines = [(5, 0, 0)]
        vals = {'product_id': self.id, "name": "some name"}
        lines.append((0, 0, vals))
        self.ozon_attribute_line = lines



    def ozon_get_category_tree(self):
        # records_to_delete = self.env['ozon.category'].search([])
        # if records_to_delete:
        #     records_to_delete.unlink()
        # get_tree = self.env['ozon.category'].get_ozon_catalog_tree()
        pass


    def ozon_get_attributes(self):
        get_attributes = self.env['ozon.category'].ozon_get_attributes(self.ozon_category_tree.category_id)
        print(f'***********Attributes found: {get_attributes}')
        lines = [(5, 0, 0)]
        for attribute in get_attributes:
            vals = {'product_id': self.id, "name": attribute['name']}
            lines.append((0, 0, vals))
        self.ozon_attribute_line = lines


# {'id': 85, 'name': 'Бренд', 'description': 'Укажите наименование бренда, под которым произведен товар. Если товар не имеет бренда, используйте значение "Нет бренда".',
#     'type': 'String', 'is_collection': False, 'is_required': True, 'group_id': 0, 'group_name': '', 'dictionary_id': 28732849, 'is_aspect': False, 'category_dependent': True}
