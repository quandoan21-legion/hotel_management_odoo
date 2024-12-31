from odoo import models, fields

class Hotel(models.Model):
    _name = 'hotels.hotel'
    _description = 'Hotel description'

    name = fields.Char(string='Name', required=True)
    address = fields.Char(string='Address', required=True)
    floors = fields.Integer(string='Floor', required=True)
    rooms = fields.Integer(string='Rooms', required=True)



