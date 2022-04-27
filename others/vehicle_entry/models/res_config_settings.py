# -*-coding: utf-8-*-
# Part of BI Solutions. See lICENSE

from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    link_with_accounting = fields.Boolean(string="Link with Accounting")