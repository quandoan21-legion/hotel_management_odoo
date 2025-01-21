from odoo import models, fields

class HotelRoomPortal(models.Model):
    _name = 'hotels.room.portal'
    _inherit = ['portal.mixin']
    _description = 'Hotel Room Portal'

    def get_portal_menu(self):
        return [{
            'name': 'Available Rooms',
            'url': '/hotel/rooms',
            'sequence': 10,
            'access_key': 'view_available_rooms',
        }]