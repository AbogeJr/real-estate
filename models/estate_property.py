from odoo import models, fields, api, exceptions, tools


class ReasEstatePropertyModel(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Char()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.today())
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (Sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (Sqm)")
    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
        string="Status",
    )
    property_type_id = fields.Many2one("estate.property.type", required=True)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Integer(
        compute="_compute_total_area", readonly=True, store=True
    )
    best_price = fields.Float(
        compute="_compute_best_price", string="Best Offer", readonly=True, store=True
    )
    offer_count = fields.Integer(compute="_compute_offer_count", store=True)

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def set_sold(self):
        # print("Hello World!")
        for record in self:
            if record.state == "offer_accepted":
                if record.state == "cancelled":
                    raise exceptions.UserError("You cannot sell cancelled property")
                else:
                    record.state = "sold"
            elif record.state == "new":
                raise exceptions.UserError("An offer has to be received")
            else:
                raise exceptions.UserError("An offer has to be accepted before selling")

    def set_cancelled(self):
        for record in self:
            record.state = "cancelled"

    @api.constrains("selling_price", "offer_ids")
    def _check_selling_price(self):
        for record in self:
            if record.expected_price and record.selling_price:
                if not tools.float_utils.float_is_zero(
                    record.expected_price, precision_rounding=2
                ):
                    if (
                        tools.float_utils.float_compare(
                            record.selling_price,
                            record.expected_price * 0.9,
                            precision_rounding=2,
                        )
                        == -1
                    ):
                        raise exceptions.ValidationError(
                            "Offer price cannot be lower than 90% of expected price."
                        )

    @api.model
    def ondelete(self, vals):
        for record in vals:
            if record.state != "new" or record.state != "cancelled":
                raise exceptions.UserError("You cannot delete sold property")
            else:
                return super().ondelete(vals)

    @api.model
    def get_statistics(self):
        property_by_type = self.read_group(
            [("state", "!=", "cancelled")],
            [],
            ["property_type_id"],
        )
        print(property_by_type)

        property_by_type_stats = {
            g["property_type_id"][0]: g["property_type_id_count"]
            for g in property_by_type
        }

        property_by_type_stats_with_name = {
            self.env["estate.property.type"].browse(property_type_id).name: count
            for property_type_id, count in property_by_type_stats.items()
            if property_type_id
        }

        avg_price = self.search([("state", "=", "sold")]).read_group(
            [("state", "=", "sold")], ["selling_price:avg(selling_price)"], []
        )[0]["selling_price"]

        return {
            "count": self.search_count([]),
            "avg_price": "{:.2f}".format(avg_price) if avg_price else 0.0,
            "property_by_type": property_by_type_stats_with_name,
        }
