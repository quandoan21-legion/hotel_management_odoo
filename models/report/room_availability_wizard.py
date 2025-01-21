from odoo import models, fields, api
from datetime import date


class RoomAvailabilityWizard(models.TransientModel):
    _name = 'room.availability.wizard'
    _description = 'Room Availability Wizard'

    start_date = fields.Date(string='Start Date', required=True, default=fields.Date.context_today)
    end_date = fields.Date(string='End Date', required=True, default=fields.Date.context_today)

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date > record.end_date:
                raise models.ValidationError('Start Date cannot be greater than End Date')

    def get_available_rooms(self):
        domain = [('room_status', '=', 'available')]
        rooms = self.env['hotels.room'].search(domain)

        available_rooms = []
        for room in rooms:
            overlapping_orders = self.env['hotels.room.order'].search([
                ('room_id', '=', room.id),
                ('order_status', '!=', 'completed'),
                ('check_in_date', '<=', self.end_date),
                ('check_out_date', '>=', self.start_date),
            ])
            if not overlapping_orders:
                available_rooms.append(room)

        return available_rooms

    def action_view_report(self):
        available_rooms = self.get_available_rooms()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Available Rooms',
            'view_mode': 'list,form',
            'res_model': 'hotels.room',
            'domain': [('id', 'in', [room.id for room in available_rooms])],
            'target': 'current',
        }

    def action_print_report(self):
        available_rooms = self.get_available_rooms()
        return self.env.ref('hotel_management.action_room_availability_report').report_action(self, data={
            'rooms': available_rooms})