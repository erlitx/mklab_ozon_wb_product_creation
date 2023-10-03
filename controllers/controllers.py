# -*- coding: utf-8 -*-
# from odoo import http


# class MklabOzonwbProductCreation(http.Controller):
#     @http.route('/mklab_ozonwb_product_creation/mklab_ozonwb_product_creation', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mklab_ozonwb_product_creation/mklab_ozonwb_product_creation/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mklab_ozonwb_product_creation.listing', {
#             'root': '/mklab_ozonwb_product_creation/mklab_ozonwb_product_creation',
#             'objects': http.request.env['mklab_ozonwb_product_creation.mklab_ozonwb_product_creation'].search([]),
#         })

#     @http.route('/mklab_ozonwb_product_creation/mklab_ozonwb_product_creation/objects/<model("mklab_ozonwb_product_creation.mklab_ozonwb_product_creation"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mklab_ozonwb_product_creation.object', {
#             'object': obj
#         })
