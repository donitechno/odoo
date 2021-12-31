# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp

class StockPicking(models.Model):    
    _description = 'Stock Picking'
    _inherit = 'stock.picking'

    nilairiil = fields.Float("Nilai Riil", digits= dp.get_precision('Stock Weight'))
