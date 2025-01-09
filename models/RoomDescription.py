from odoo import models, fields, api

class RoomDescription(models.Model):
    _name = 'hotels.room.description'
    _description = 'Room\'s Description Detail'

    view = fields.Char(string='View', required=True)
    name = fields.Char(string='Description', compute='_compute_name', store=True)

    @api.depends('view')
    def _compute_name(self):
        for record in self:
            record.name = record.view.capitalize() if record.view else ''

    # You can also add record rules programmatically here if needed
