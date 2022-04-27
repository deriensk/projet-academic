# -*- coding: utf-8 -*-
from odoo import http

# class SalesAquaExt(http.Controller):
#     @http.route('/sales_aqua_ext/sales_aqua_ext/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sales_aqua_ext/sales_aqua_ext/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sales_aqua_ext.listing', {
#             'root': '/sales_aqua_ext/sales_aqua_ext',
#             'objects': http.request.env['sales_aqua_ext.sales_aqua_ext'].search([]),
#         })

#     @http.route('/sales_aqua_ext/sales_aqua_ext/objects/<model("sales_aqua_ext.sales_aqua_ext"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sales_aqua_ext.object', {
#             'object': obj
#         })