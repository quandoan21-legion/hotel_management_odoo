from odoo import models, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    def write(self, vals):
        if 'groups_id' in vals:
            # Get the "User Types" category
            user_type_category = self.env.ref('base.module_category_user_type')
            for user in self:
                # Check if the groups being written include a user type
                new_groups = self.env['res.groups'].browse(vals['groups_id'][0][2]) if vals['groups_id'] else self.env['res.groups']
                if any(group.category_id == user_type_category for group in new_groups):
                    # Remove the current user type
                    user.groups_id -= user.groups_id.filtered(lambda g: g.category_id == user_type_category)
        return super(ResUsers, self).write(vals)
