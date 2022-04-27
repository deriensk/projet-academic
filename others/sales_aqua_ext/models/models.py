# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class sales_aqua_ext(models.Model):
#     _name = 'sales_aqua_ext.sales_aqua_ext'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

class sales_order_extend(models.Model):

    _inherit = "sale.order"

class SaleOrder_Aqua(models.Model):
    
    _inherit = 'sale.order.line'

    # _name = 'jar.data.line'
    
    product_id = fields.Many2one('product.product',string='Product')
    empty_jar = fields.Integer('Empty Jar')
    returned_jar = fields.Integer('Returned Jar')
    damaged_jar = fields.Integer('Damaged Jar')
    filled_jar = fields.Integer('Filled Jar')
    labels_consumed = fields.Integer('Labels Consumed')
    sold_jar = fields.Integer('Sold Jar')
    # order_line_ids = fields.Many2one('vehicle_entry.vehicle_entry')
