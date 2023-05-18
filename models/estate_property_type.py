from odoo import fields, models, api


class EstatePropertyTypeModel(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer("Sequence", default=1)
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    property_count = fields.Integer(compute="_compute_property_count")
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends("property_ids")
    def _compute_property_count(self):
        for record in self:
            record.property_count = len(record.property_ids)

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
