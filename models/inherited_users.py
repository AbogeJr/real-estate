from odoo import fields, models


class InheritedUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        comodel_name="estate.property",
        inverse_name="salesperson_id",
        string="Properties Listed",
    )
