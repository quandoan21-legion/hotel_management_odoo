from odoo import models, fields


class Room(models.Model):
    _name = 'hotels.room'
    _description = 'Room description'

    hotel_id = fields.Many2one('hotels.hotel', string='Hotel', required=True)
    hotel_address = fields.Char(related='hotel_id.address', string='Hotel Address')
    bed_type = fields.Selection([("single", "Single"), ("double", "Double")], string='Bed Type',
                                required=True)
    room_price = fields.Float(string='Room Price', required=True)
    room_status = fields.Selection([("available", "Available"), ("occupied", "Occupied")], string='Room Status',
                                   required=True)
    room_description = fields.Many2many('hotels.room.description', string='Room Descriptions')

