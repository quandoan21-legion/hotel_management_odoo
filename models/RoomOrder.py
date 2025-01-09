from datetime import date
from odoo import models, fields, api


class RoomOrder(models.Model):
    _name = 'hotels.room.order'
    _description = 'Hotel Room Order Details'

    customer_name = fields.Char(string='Customer Name', required=True)
    check_in_date = fields.Date(string='Check In Date', required=True, default=lambda self: date.today())
    check_out_date = fields.Date(string='Check Out Date', required=True)
    room_id = fields.Many2one('hotels.room', string='Room', required=True, ondelete='restrict',)
    order_status = fields.Selection([
        ('requested', 'Requested'),
        ('approved', 'Approved'),
        ('completed', 'Completed')
    ], string='Order Status', required=True, default='requested')
    room_price = fields.Float(related='room_id.room_price', string='Room Price')

    def action_approve(self):
        for record in self:
            record.state = 'approved'

    def action_complete(self):
        for record in self:
            record.state = 'completed'

    @api.constrains('check_in_date', 'check_out_date')
    def _check_dates(self):
        for record in self:
            # Ensure the check_in_date is not before today
            if record.check_in_date and record.check_in_date < date.today():
                raise models.ValidationError("The Check In Date must not be earlier than today.")

            # Ensure check_out_date is not earlier than check_in_date
            if record.check_in_date and record.check_out_date and record.check_out_date < record.check_in_date:
                raise models.ValidationError("The Check Out Date must not be earlier than the Check In Date.")
