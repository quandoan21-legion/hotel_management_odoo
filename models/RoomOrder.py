from odoo import models, fields

class RoomOrder(models.Model):
    _name = 'hotels.room.order'
    _description = 'Room Order'

    customer_name = fields.Char(string='Customer Name', required=True)
    check_in_date = fields.Date(string='Check In Date', required=True)
    check_out_date = fields.Date(string='Check Out Date', required=True)
    room_id = fields.Many2one('hotels.room', string='Room', required=True)
    order_status = fields.Selection([('confirmed', 'Confirmed'), ('new', 'New')], string='Order Status',
                                    required=True)
    room_prize = fields.Float(related='room_id.room_prize', string='Room Prize')