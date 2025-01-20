from datetime import date
from odoo import models, fields, api

class RoomOrder(models.Model):
    _name = 'hotels.room.order'
    _description = 'Hotel Room Order Details'

    customer_name = fields.Many2one('res.partner', required=True)
    check_in_date = fields.Date(string='Check In Date', required=True, default=lambda self: date.today())
    check_out_date = fields.Date(string='Check Out Date', required=True)
    room_id = fields.Many2one('hotels.room', string='Room', required=True, ondelete='restrict')
    order_status = fields.Selection([
        ('requested', 'Requested'),
        ('new', 'New'),
        ('approved', 'Approved'),
        ('completed', 'Completed')
    ], string='Order Status', required=True, default='new')
    room_price = fields.Float(related='room_id.room_price', string='Room Price')
    total_room_price = fields.Float(string='Booking Total Price(Not Include Amenities)', readonly=True, compute="_calculate_total_room_price")
    is_paid = fields.Selection([
        ('paid', "Paid"),
        ('not_paid', "Not Paid"),
    ], String='Customer has paid for the order or not', default='not_paid')
    product_id = fields.Many2many('product.product')
    paid_date = fields.Date(string='Paid Date')
    paid_amount = fields.Float(string='Total Order')

    def action_approve(self):
        for order in self:
            order.write({'order_status': 'approved'})

    @api.onchange('check_in_date', 'check_out_date')
    def _calculate_total_room_price(self):
        for record in self:
            if record.check_in_date and record.check_out_date:
                check_in = fields.Date.from_string(record.check_in_date)
                check_out = fields.Date.from_string(record.check_out_date)
                day_difference = (check_out - check_in).days
                if day_difference > 0:
                    record.total_room_price = day_difference * record.room_price
                else:
                    record.total_room_price = 0
                    raise models.ValidationError("The Check Out Date must be later than the Check In Date.")
            else:
                record.total_room_price = 0

    @api.model
    def create(self, vals):
        record = super(RoomOrder, self).create(vals)
        if record.room_id:
            record.room_id.last_rent_date = date.today()
            record.room_id._check_availability()
        return record

    @api.model
    def write(self, vals):
        result = super(RoomOrder, self).write(vals)
        for record in self:
            if record.room_id:
                record.room_id.last_rent_date = date.today()
                record.room_id._check_availability()
        return result

    @api.model
    def paid_order(self, vals):
        return {
            'name': 'Payment',
            'type': 'ir.actions.act_window',
            'res_model': 'hotels.room.payment.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_room_order_id': self.env.context.get('default_order_id'),
                'default_room_id': self.env.context.get('default_room_id')
            }
        }

    @api.constrains('check_in_date', 'check_out_date')
    def _check_dates(self):
        for record in self:
            if record.check_in_date and record.check_out_date:
                # Ensure the check_in_date is not before today
                if record.check_in_date < date.today():
                    raise models.ValidationError("The Check In Date must not be earlier than today.")

                # Ensure check_out_date is not earlier than check_in_date
                if record.check_out_date < record.check_in_date:
                    raise models.ValidationError("The Check Out Date must not be earlier than the Check In Date.")
