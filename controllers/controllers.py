# -*- coding: utf-8 -*-

import logging
import random

from odoo import http

# from odoo.http import request

logger = logging.getLogger(__name__)


class RealEstate(http.Controller):
    @http.route("/estate/property/statistics", type="json", website=True, auth="public")
    def get_statistics(self, **kwargs):
        return http.request.env["estate.property"].get_statistics()
        
        # count = PropertyModel.search_count([])
        # sold_properties = PropertyModel.search([("state", "=", "sold")])
        # avg_price = sold_properties.read_group(
        #     [("state", "=", "sold")], ["selling_price:avg(selling_price)"], []
        # )
        # return {
        #     "count": count,
        #     "avg_price": avg_price[0]["selling_price"] if avg_price else 0.0,
        # }
