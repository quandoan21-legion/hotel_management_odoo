from odoo import models, fields

class RoomDescription(models.Model):
    _name = 'hotels.room.description'
    _description = 'Room Description'

    view = fields.Selection([('sea', 'Sea View'), ('city', 'City View'), ('garden', 'Garden View')], string='View')
