# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ContactExt(models.Model):
    
    _inherit = 'res.partner'
    
    driver_license = fields.Char('Driving Licence No.')
    # key_person = fields.Char('Key Person')
    vehicle_list = fields.One2many('vehicle.info', 'customer', 'Vehicle List')
    is_a_driver = fields.Boolean(string='Is a Driver')


    @api.multi
    def name_get(self):
        res = []
        for record in self:
            name = record.name
            name = "%(name)s" % {
                'name': name
            }
            res.append((record.id, name))
        return res

   
class VehicleList(models.Model):
    
    _inherit = 'vehicle.info'

    # vehicle = fields.Char("Vehicle")
    # vehicle_list_id = fields.Many2one('res.partner')







# class contact_ext_aqua(models.Model):
#     _name = 'contact_ext_aqua.contact_ext_aqua'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
