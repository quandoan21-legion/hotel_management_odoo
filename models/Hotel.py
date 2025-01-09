from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Hotel(models.Model):
    _name = 'hotels.hotel'
    _description = 'Hotel Description'

    name = fields.Char(string='Name', required=True)
    address = fields.Char(string='Address', required=True)
    floors = fields.Integer(string='Floors', required=True)
    rooms = fields.Integer(string='Rooms', required=True)

    manager_id = fields.Many2one(
        'hr.employee',
        string="Manager",
        required=True,
        help="Assign a manager from the 'Manager' group"
    )

    assigned_users = fields.Many2many(
        "res.users",
        string="Assigned Users",
        help="Employees that assigned to work in this hotel."
    )

    @api.constrains('manager_id')
    def _check_manager_group(self):
        """Ensure the selected manager belongs to the specific group."""
        for record in self:
            if record.manager_id:
                # Ensure the employee is linked to a user
                user = record.manager_id.user_id
                if user:
                    # Check if the user belongs to the "Manager" group
                    group = self.env.ref('hotel.group_manager')
                    if group not in user.groups_id:
                        raise ValidationError(
                            f"The selected employee ({record.manager_id.name}) is not in the 'Manager' group."
                        )
                else:
                    raise ValidationError(
                        f"The selected employee ({record.manager_id.name}) does not have an associated user."
                    )
