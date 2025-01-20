from datetime import date

from odoo import fields, models, api


class BookingPaymentWizard(models.TransientModel):
    _name = 'hotels.room.payment.wizard'
    _description = 'Room Payment Wizard'

    room_id = fields.Integer(string="Room", required=True, readonly=True)
    room_name = fields.Char(string="Room Name", compute="_compute_room_name", readonly=True)
    payment_date = fields.Date(string="Payment Date", default=lambda self: date.today(), required=True)
    paid_amount = fields.Float(string="Paid Amount", required=True)

    @api.depends('room_id')
    def _compute_room_name(self):
        # Fetch the room name using the room_id
        for record in self:
            room = self.env['hotels.room'].browse(record.room_id)
            record.room_name = room.name if room else ''


    def confirm_payment(self):
        self.room_order_id.write({
            'is_paid': 'paid',
            'paid_date': self.payment_date,
            'paid_amount': self.paid_amount,
        })
        return {'type': 'ir.actions.act_window_close'}
