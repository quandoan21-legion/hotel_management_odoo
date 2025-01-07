from datetime import date
from email.policy import default

from odoo import models, fields, api

class RoomOrder(models.Model):
    _name = 'hotels.room.order'
    _description = 'Room Order'

    customer_name = fields.Char(string='Customer Name', required=True)
    check_in_date = fields.Date(string='Check In Date', required=True, default=lambda self: date.today())
    check_out_date = fields.Date(string='Check Out Date', required=True)
    room_id = fields.Many2one('hotels.room', string='Room', required=True)
    order_status = fields.Selection(
        [('confirmed', 'Confirmed'), ('new', 'New')], string='Order Status', required=True, default='new')
    room_price = fields.Float(related='room_id.room_price', string='Room Price')


    @api.depends('room_id')
    def _compute_room_feature(self):
        for order in self:
            if order.room_id:
                order.room_name= order.room_id.room_name

    @api.constrains('check_out_date', 'check_in_date')
    def _check_dates(self):
        for record in self:
            if record.check_out_date and record.check_out_date <= date.today():
                raise models.ValidationError("The Check Out Date must be later than today.")
            if record.check_in_date and record.check_out_date and record.check_out_date < record.check_in_date:
                raise models.ValidationError("The Check Out Date must not be earlier than the Check In Date.")

    @api.onchange('check_in_date', 'check_out_date', 'customer_name', 'room_id')
    def _onchange_order_status(self):
        if self.order_status == 'new':
            self.order_status = 'confirmed'