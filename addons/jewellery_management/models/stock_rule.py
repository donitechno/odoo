from odoo import api, fields, models, registry, SUPERUSER_ID, _
from collections import namedtuple

import logging
_logger = logging.getLogger(__name__)

class StockRule(models.Model):
    _inherit = 'stock.rule'
    _description = "Stock Rule"


    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, company_id, values):

        move_values=  super(StockRule, self)._get_stock_move_values(product_id, product_qty, product_uom, location_id, name, origin, company_id, values)
        #move_values['nilairiil'] = values.nilairiil

        return move_values


class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'
    _description = "procurement group inherit"
