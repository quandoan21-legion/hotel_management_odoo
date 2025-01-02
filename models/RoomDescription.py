from odoo import models, fields, api

class RoomDescription(models.Model):
    _name = 'hotels.room.description'
    _description = 'Room Description'

    view = fields.Char(string='View', required=True)  # Changed to Char field
    name = fields.Char(string='Description', compute='_compute_name', store=True)

    @api.depends('view')
    def _compute_name(self):
        for record in self:
            # Capitalize the first letter of the view and set it as the name
            record.name = record.view.capitalize() if record.view else ''
