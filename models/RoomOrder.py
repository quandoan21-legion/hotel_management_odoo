from datetime import date
from odoo import models, fields, api


class RoomOrder(models.Model):
    _name = 'hotels.room.order'
    _description = 'Hotel Room Order Details'

    customer_name = fields.Char(string='Customer Name', required=True)
    check_in_date = fields.Date(string='Check In Date', required=True, default=lambda self: date.today())
    check_out_date = fields.Date(string='Check Out Date', required=True)
    room_id = fields.Many2one('hotels.room', string='Room', required=True, ondelete='restrict', )
    order_status = fields.Selection([
        ('requested', 'Requested'),
        ('new', 'New'),
        ('approved', 'Approved'),
        ('completed', 'Completed')
    ], string='Order Status', required=True, default='new')
    room_price = fields.Float(related='room_id.room_price', string='Room Price')

    def action_approve(self):
        for order in self:
            order.write({'order_status': 'approved'})


    @api.model
    def create(self, vals):
        record = super(RoomOrder, self).create(vals)
        if record.room_id:
            # Update last_rent_date for the associated room
            record.room_id.last_rent_date = date.today()
        return record

    def write(self, vals):
        result = super(RoomOrder, self).write(vals)
        for record in self:
            if record.room_id:
                # Update last_rent_date for the associated room
                record.room_id.last_rent_date = date.today()
        return result

    @api.constrains('check_in_date', 'check_out_date')
    def _check_dates(self):
        for record in self:
            if record.id and record.check_out_date < record.check_in_date:
                raise models.ValidationError("The Check Out Date must not be earlier than the Check In Date.")
            else:
                continue

            # Ensure the check_in_date is not before today
            if record.check_in_date and record.check_in_date < date.today():
                raise models.ValidationError("The Check In Date must not be earlier than today.")

            # Ensure check_out_date is not earlier than check_in_date
            if record.check_in_date and record.check_out_date and record.check_out_date < record.check_in_date:
                raise models.ValidationError("The Check Out Date must not be earlier than the Check In Date.")
