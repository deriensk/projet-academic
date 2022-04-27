# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

from datetime import datetime, timedelta

from odoo.exceptions import ValidationError

class vehicle_entry(models.Model):
    _inherit = 'mail.thread'
    _name = 'vehicle_entry.vehicle_entry'
    _order = 'id desc'
    _rec_name = 'sequence_id'

    sequence_id = fields.Char(
        'Sequence ID', copy=False, readonly=True, default=lambda x: _('New'))

    check_in = fields.Datetime("Check In", readonly=True)#, default=fields.Datetime.now)
    check_out = fields.Datetime("Check Out", readonly=True)# default=fields.Datetime.now
    state = fields.Selection([
        ('checkin', 'Check In'),
        ('waiting', 'Waiting'),
        ('offload', 'Offload'),
        ('filling', 'Filling'),
        ('load', 'Loading'),
        ('checkout', 'Check Out'),
    ], string='Status', index=True, readonly=True, copy=False, default='checkin',
        help="""* When the vehicle check in the status is \'Check In\'
                \n* If the vehicle is under verification, the status is \'Waiting\'.
                \n* If the vehicle is offloaded then status is set to \'Offload\'.
                \n* If jar is on process then status is set to \'Filling\'.
                \n* If the vehicle is loaded then status is set to \'Loading\'.
                \n* If the vehicle leave then status is set to \'Check Out\'.""")
    
    '''@api.model
    def _getVehicle(self):
        vehicle_list = []
        vehicle_objs = self.env['vehicle_entry.vehicle_entry'].search([('state', '!=', 'checkout')])
        for vehicle_obj in vehicle_objs:
            if vehicle_obj.vehicle_no.vehicle_number not in vehicle_list:
                vehicle_list.append(vehicle_obj.vehicle_no.vehicle_number)
        vehicle_domain = [('vehicle_number', 'not in', vehicle_list)]
        return vehicle_domain'''

    '''@api.model
    def _getVehicle(self):
        vehicle_list = []
        vehicle_objs = self.env['vehicle_entry.vehicle_entry'].search([('state', '!=', 'checkout')])
        for vehicle_obj in vehicle_objs:
            if vehicle_obj.vehicle_no not in vehicle_list:
                vehicle_list.append(vehicle_obj.vehicle_no)
        vehicle_domain = [('id', 'not in', vehicle_list)]
        return vehicle_domain'''

 
    vehicle_no = fields.Many2one('vehicle.info', string='Vehicle No', required=True)# domain="_getVehicle")
    customer = fields.Many2one('res.partner', string="Customer", related="vehicle_no.customer")
    vehicle_type = fields.Many2one(string="Vehicle Model", readonly=True, related="vehicle_no.vehicle_type")                         
   
    item_ids = fields.One2many('jar.data.line', 'order_line_ids', string='Item Id.')

    driver_name = fields.Many2one('res.partner', string='Driver Name')
    driver_id = fields.Char('Driver Liscence No.', compute="_get_licence_number", readonly=True)

    # @api.model
    # def entry_checkin(self):
    #     v_search = self.env['vehicle.info'].search([('vehicle_number', '=', self.vehicle_no)])
    #     if v_search == True:
    #         raise ValidationError('Yes the vehicle exists.')


   
    # For seamless printing
    is_printed = fields.Boolean('Printed?', default = False)
    print_request = fields.Boolean('Print Request', default = False)
    print_requested_by = fields.Integer('Request by')
    bool_field = fields.Boolean('Vehicle Out', default=False)

    # @api.onchange("driver_name")
    # @api.multi
    def driver_self(self):
        if self.driver_name == None:
            self.driver_name = self.customer
    

    @api.multi
    def action_print_request(self):
        # Any validation checks
        if self.is_printed == True:
            raise ValidationError(
                "Print Error")
            return 1
            self.print_request = True
            self.print_requested_by = self._uid

    @api.multi
    def auto_date_check_in(self):
        Date = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        raise Date.context_today(self)


    @api.multi
    def auto_date_check_out(self):
        Date = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        raise Date.context_today(self)

    @api.multi
    def _auto_date_time_in(self):
        for order in self:
            order.check_in = fields.Datetime.now()


    @api.multi
    def _auto_date_time_out(self):
        for order in self:
            order.check_out = fields.Datetime.now()

    # Create unique id of every entry record
    @api.model
    def create(self, vals):
        if vals.get('sequence_id', _('New')) == _('New'):
            vals['sequence_id'] = self.env['ir.sequence'].next_by_code('vehicle_entry.vehicle_entry') or _('New')
        return super(vehicle_entry, self).create(vals)


    # Workflow
    @api.multi
    def concept_checkin(self):
        self.ensure_one()
        self.write({'state': 'checkin', })

    @api.multi
    def concept_waiting(self):
        self.ensure_one()
        
        # Print checks
        if self.action_print_request():
            return 1
        self.write({'state': 'waiting', })
        self._auto_date_time_in()
        # return self.env.ref('vehicle_entry.action_print_token_report').report_action(self)
        # return self.env['web'].get_action(self, 'vehicle_entry.vehicle_entry_token_print_template') # deprecated


    @api.multi
    def concept_offload(self):
        self.ensure_one()
        self.write({'state': 'offload', })

    @api.multi
    def concept_filling(self):
        # self.ensure_one()
        for rec in self.item_ids:
            if rec.empty_jar > 0:
                self.write({'state': 'filling', })
            else:
                raise ValidationError("Total quantity must be entered.")    

    @api.multi
    def concept_loading(self):
        self.ensure_one()
        self.write({'state': 'load', })

    @api.multi
    def concept_out(self):
        self.ensure_one()
        self.write({'state': 'checkout'})
        self._auto_date_time_out()
        return {
                'type': 'ir.actions.client',
                'tag': 'vehicle_entry_enter'
                }
####################################################
# for the validation to check confirmation of sale
# order before loading the jar
####################################################
    @api.multi
    def concept_sale(self):
        # sale = self.env['sale.order'].search([('state', '=', 'sale'),('token_no', '=', self.sequence_id)])
        # if sale:
        self.concept_loading()
        # else:
            # raise ValidationError("Sales order doesn't confirmed.")


########################################################
#  for validation check in checkout button
#  Only After creating invoice the vehicle can checkout
########################################################
    # @api.multi
    # def concept_out1(self):
    #     sale = self.env['sale.order']
    #     sales = sale.search([('state', '=', 'sale'),('token_no', '=', self.sequence_id)])
    #     if sales:
    #         invoice = self.env['account.invoice'].search([('origin', '=', sale.name)])
    #         if invoice:
    #             self.concept_checkout()
    #         else:
    #             raise ValidationError("Invoice has not been created.")
    #     else:
    #         raise ValidationError("Invoice has not been created yet! Please receive your invoice and select Done.")





    
    #send record to sale order
    # dataflow in vehicle entry
    @api.multi
    def sale_order_send(self):
        self.bool_field = True
        self.write({'state': 'checkout'})
        # self.concept_out()
        ddr_env = self.env['sale.order']
        order_list = []
        for record in self:
            for rec in record.item_ids:
                order_list.append((0, 0, {
                    'product_id': rec.product_id.id,
                    'product_uom_qty': rec.sold_jar,
                    }))               
        for aa in self:
            order_line = ddr_env.create({
                'partner_id': aa.customer.id,
                # 'date_order': aa.check_in,
                'order_line': order_list,
                'token_no':  aa.sequence_id,         
            })
        return order_line

    # def _get_vehicle_type(self):
    #     self.vehicle_type = self.vehicle_no.vehicle_type

    def _get_licence_number(self):
        for rec in self:
            rec.driver_id = rec.driver_name.driver_license  

    @api.multi
    def so_notify(self):
        #self.sale_order_send()
        app = self.env['res.groups'].sudo().search([('category_id.name', '=', 'Sales')])
        for m in app:
            if m.name == 'Manager':
                recipients = []
                for recipient in m.users:
                    recipients.append((4, recipient.partner_id.id))
        sale = self.env['sale.order'].search([('token_no', '=', self.sequence_id)])
        for rec in sale:
            # # Get URL for current record
            record_url = str('/web#id=' + str(rec.id) + '&model=' + str(rec._name))
            # Message body
            body = "Confirm sale order and create invoice: " + str(rec.id) + ": <a href='" + record_url + "'>Please click here to take action.</a>"
            # Send notification message
            post_vars = {'subject': "Confirm Sale Order",
                'body': body,
                'partner_ids': recipients,}
            self.message_post(type="notification", subtype="mt_comment", **post_vars)
        # self.ensure_one()
        # self.write({'state': 'checkout', })
        # self.env.user.notify_info('Confirm Sale order.')



class VehicleInfo(models.Model):
    
    _name = "vehicle.info"
    _rec_name = 'vehicle_number'

    vh_zone = fields.Selection(
        [('ME', 'ME'), ('KO', 'KO'), ('SA', 'SA'),
        ('JA', 'JA'), ('BA', 'BA'), ('NA', 'NA'),
        ('GA', 'GA'),('LU', 'LU'),('DH', 'DH'),
        ('RA', 'RA'), ('BHE', 'BHE'), ('KA', 'KA'),
        ('SE', 'SE'), ('MA', 'MA'),], default='BA', string="Zone")

    vh_lot = fields.Integer(string="Lot no.", default=1, required=True)
    vh_category = fields.Selection(
        [('NA', 'NA'), ('KA', 'KA'), ('CHA', 'CHA'),('HA', 'HA'),('KHA', 'KHA'),
        ('PA', 'PA')], default='KHA', string="Vehicle category")
    number = fields.Char(string="Number", required=True, size=4)
    vehicle_number = fields.Char(compute='comp_name', store=True, string='Vehicle no.')
    customer = fields.Many2one('res.partner', string="Customer")
   
    vehicle_type = fields.Many2one('vehicle.model')
    remarks = fields.Text('Remarks')

    @api.depends('vh_zone','vh_lot','vh_category','number')
    @api.one
    def comp_name(self):
        self.vehicle_number = (self.vh_zone)+' '+ str((self.vh_lot or ''))+' '+(self.vh_category or '')+ ' ' +(self.number or '')
 
class VehicleModel(models.Model):
    
    _name = 'vehicle.model'
    _rec_name = 'vh_model'

    vh_model = fields.Char('Vehicle Model')

       
class JarDataLine(models.Model):
    
    _name = 'jar.data.line'

    product_id = fields.Many2one('product.product',string='Product', required=True)
    empty_jar = fields.Integer('Total Quantity')
    returned_jar = fields.Integer('Returned Quantity')
    damaged_jar = fields.Integer('Damaged Quantity')
    filled_jar = fields.Integer('Filled Jar')
    labels_consumed = fields.Integer('Labels Consumed')
    sold_jar = fields.Integer('Ordered Quantity', compute="get_ordered_qty", store=True)
    order_line_ids = fields.Many2one('vehicle_entry.vehicle_entry')

    @api.depends('empty_jar','returned_jar','damaged_jar')
    def get_ordered_qty(self):
        for rec in self:
            if rec.empty_jar < 0:
                rec.empty_jar = 0
            if rec.returned_jar < 0:
                rec.returned_jar = 0
            if rec.damaged_jar < 0:
                rec.damaged_jar = 0
            rec.sold_jar = rec.empty_jar - (rec.returned_jar + rec.damaged_jar)
            if rec.sold_jar < 0:
                raise ValidationError("Please check your entry!")

class vehicle_type(models.Model):
    
    _name = 'vehicle.type'
    _rec_name = 'name'

    name = fields.Many2one('vehicle.info')

class sale_inherit(models.Model):
    _inherit = "sale.order"
    token_no = fields.Char("Token No.")

    
    

# Empty jar : Integer
#  Returned Jar: Integer
#  Damaged Jar: Integer
#  Filled Jar: Integer
#  Labels Consume: Integer
#  Sold Jar: Float


# for printing token

    # @api.multi
    # def print_report(self):
    #     return self.env['report'].get_action(self, 'vehicle_entry.vehicle_entry_token_print_template')

      

    # @api.multi
    # def auto_date_check_in(self):
    #     Date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    #     raise Date.context_today(self)


    # @api.multi
    # def test_server_action(self):
    #     self.env.ref('vehicle_entry.vehicle_entry_action_exit').run

