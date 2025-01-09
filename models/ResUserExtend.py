from odoo import models, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def create(self, vals):
        # Create the user first
        user = super(ResUsers, self).create(vals)
        # Automatically create an employee linked to this user
        if user:
            self.env['hr.employee'].create({
                'name': user.name,  # Use the user's name for the employee
                'user_id': user.id,  # Link the employee to the user
                'work_email': user.email,  # Optional: Use the user's email
            })
        return user
