from odoo import models, fields, api, exceptions
from dateutil.relativedelta import relativedelta
from datetime import date


class EstateProperyOfferModel(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused"), ("pending", "Pending")],
        default="pending",
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(
        compute="_compute_validity", inverse="_inverse_validity", tracking=True
    )
    date_deadline = fields.Date(string="Deadline", tracking=True)
    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        store=True,
    )

    @api.depends("validity", "date_deadline")
    def _compute_validity(self):
        today = date.today()
        for record in self:
            if record.date_deadline:
                record.validity = (record.date_deadline - today).days
            else:
                record.validity = 1

    def _inverse_validity(self):
        today = date.today()
        for record in self:
            if record.validity:
                record.date_deadline = today + relativedelta(days=record.validity)

    def set_accepted(self):
        for record in self:
            record.status = "accepted"
            record.property_id.state = "offer_accepted"
            record.property_id.buyer_id = record.partner_id.id
            record.property_id.selling_price = record.price

    def set_rejected(self):
        for record in self:
            record.status = "refused"

    @api.model
    def create(self, vals):
        property_id = vals.get("property_id")
        if property_id:
            offers = self.env["estate.property.offer"].search(
                [("property_id", "=", property_id)]
            )
            prices = offers.mapped("price")
            if prices and vals.get("price", 0.0) < max(prices):
                raise exceptions.ValidationError(
                    "The offer must be higher than the best offer"
                )
        record = super().create(vals)
        if record.property_id.state == "new":
            record.property_id.state = "offer_received"
        return record
