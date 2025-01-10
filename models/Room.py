from datetime import timedelta

from odoo import models, fields

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
