from datetime import date, timedelta

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

    def calculate_day_different(self, check_in_date, check_out_date):
        return (fields.Date.from_string(check_out_date) - fields.Date.from_string(check_in_date)).days + 1

    def count_weekend_days(self):
        weekend_count = 0
        # Loop through each day in the range
        current_date = self.check_in_date
        while current_date <= self.check_out_date:
            if current_date.weekday() == 5 or current_date.weekday() == 6:
                weekend_count += 1
            current_date += timedelta(days=1)
        return weekend_count

    def calculate_room_price_per_day(self, weekday_count, weekend_count, room_price):
        total_room_price_weekday = weekday_count * room_price
        total_room_price_weekend = weekend_count * (
                room_price + (room_price / 100 * self.room_id.weekend_rate))
        return total_room_price_weekday + total_room_price_weekend

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

    @api.onchange('check_in_date', 'check_out_date')
    def _calculate_total_room_price(self):
        for record in self:
            if record.check_in_date and record.check_out_date:
                day_difference = self.calculate_day_different(check_in_date=record.check_in_date,
                                                              check_out_date=record.check_out_date)
                weekend_count = self.count_weekend_days()
                weekday_count = day_difference - weekend_count
                if day_difference > 0:
                    record.total_room_price = self.calculate_room_price_per_day(weekday_count, weekend_count,
                                                                                record.room_price)
                else:
                    record.total_room_price = 0
                    raise models.ValidationError("The Check Out Date must be later than the Check In Date.")
            else:
                record.total_room_price = 0
