from datetime import timedelta
from datetime import date

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Room(models.Model):
    _name = 'hotels.room'
    _inherit = ['mail.thread']  # Inherit to enable chatter
    _description = 'Hotel Room Details'

    name = fields.Char(string='Room Name', track_visibility='onchange')
    hotel_id = fields.Many2one('hotels.hotel', string='Hotel', required=True, ondelete='cascade')
    hotel_address = fields.Char(related='hotel_id.address', string='Hotel Address')
    bed_type = fields.Selection([("single", "Single"), ("double", "Double")], string='Bed Type', required=True)
    room_price = fields.Float(string='Room Price', required=True)
    room_status = fields.Selection([("available", "Available"), ("occupied", "Occupied")], string='Room Status',
                                   required=True)

    order_ids = fields.One2many("hotels.room.order", 'room_id')
    weekend_rate = fields.Integer(string="Weekend rate(%)", required=True)
    room_description = fields.Many2many('hotels.room.description', string='Room Descriptions')
    last_rent_date = fields.Date(string="Last Rent Date")

    # Method to check the last rent date for all rooms
    def check_rooms_not_rented_7_days(self):
        """This method checks for rooms that haven't been rented for over 7 days."""
        today = fields.Date.today()
        # Find rooms that haven't been rented for the last 7 days
        rooms = self.search([
            ('last_rent_date', '<', today - timedelta(days=7))
        ])

        # Log room and hotel details
        for room in rooms:
            print(f"Room: {room.name}, Hotel: {room.hotel_id.name}, Last Rented Date: {room.last_rent_date}")

    @api.depends('order_ids.check_in_date', 'order_ids.check_out_date')
    def _check_availability(self):
        today = date.today()
        for record in self:
            overlapping_bookings = self.env['hotels.room.order'].search([
                ('room_id', '=', record.id),
                ('check_in_date', '<=', today),
                ('check_out_date', '>=', today),
            ])

            if overlapping_bookings:
                record.room_status = 'occupied'
            else:
                record.room_status = 'available'

    @api.constrains('weekend_rate')
    def check_weekend_rate_is_valid(self):
        for record in self:
            if record.weekend_rate < 0:
                raise ValidationError("The weekend rate value must be a positive number")
