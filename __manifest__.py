# -*- coding: utf-8 -*-
{
    'name': "mklab_ozonwb_product_creation",

    'summary': """
        Allows to add new products to Ozon and WB from Odoo""",

    'description': """
        Long description of module's purpose
    """,

    'author': "MKLab",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mklab_ozonwb'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/extension_product_product_ozon.xml',
        'views/ozon_category.xml',
        'wizard/wizard_product_select.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
