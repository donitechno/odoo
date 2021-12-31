# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class AccountMove(models.Model):    
    _description = 'Stock Move'
    _inherit = 'account.move'

    #weight = fields.Float("Weight", digits= dp.get_precision('Stock Weight'))
    

class StockMoveLine(models.Model):
    _inherit ='account.move.line'

    @api.depends('nilairiil')
    def _compute_nilaimurni(self):
        tarif = 103
        for record in self:
            record.nilaimurni= (record.nilairiil * record.currency_id.tarifbeliharga) * record.quantity

    @api.depends('nilaimurni')
    def _compute_nilaikonversi(self):
        tarifRp = 800000
        for record in self:
            record.nilaikonversi = record.nilaimurni * tarifRp
            record.price_unit = record.nilaikonversi
            record.sub_total = record.nilaikonversi

    #weight = fields.Float("Weight", digits= dp.get_precision('Stock Weight'))
    tarif = fields.Float("Tarif", digits= dp.get_precision('Stock Weight'))
    nilairiil = fields.Float("Nilai Riil", digits= dp.get_precision('Stock Weight'))
    nilaimurni= fields.Float("Nilai Murni", digits= dp.get_precision('Stock Weight'), store=True)
    nilaikonversi= fields.Float("Nilai Konversi", digits= dp.get_precision('Stock Weight'), store=True)
    debitkonversi = fields.Float("Debit Konversi", digits=dp.get_precision('Stock Weight'), store=True)
    creditkonversi = fields.Float("Kredit Konversi", digits=dp.get_precision('Stock Weight'), store=True)

    #tarif = field.Fields()
    @api.onchange('debitkonversi')
    def _onchange_debit(self):
        if self.debitkonversi:
            self.creditkonversi = 0.0
        self._onchange_balance()

    @api.onchange('creditkonversi')
    def _onchange_credit(self):
        if self.creditkonversi:
            self.debitkonversi = 0.0
        self._onchange_balance()

    @api.onchange('nilairiil')
    def _onchange_nilaimurni(self):
        for line in self:
            if not line.move_id.is_invoice(include_receipts=True):
                continue

            line.update(line._get_price_total_and_subtotal())
            line.update(line._get_fields_onchange_subtotal())

    @api.model
    def _get_fields_onchange_subtotal_model(self, price_subtotal, move_type, currency, company, date):
        vals = super(StockMoveLine, self)._get_fields_onchange_subtotal_model(price_subtotal,move_type, currency, company, date)

        if move_type in self.move_id.get_outbound_types():
            sign = 1
        elif move_type in self.move_id.get_inbound_types():
            sign = -1
        else:
            sign = 1
        price_subtotal *= sign

        if currency and currency != company.currency_id:
            # Multi-currencies.
            #balance = currency._convert(self.nilaikonversi, company.currency_id, company, date)
            vals['amount_currency'] = self.price_unit
            vals['debit'] = self.price_unit > 0.0 and self.price_unit or 0.0
            vals['credit'] = self.price_unit < 0.0 and -self.price_unit or 0.0

            vals['debitkonversi'] = self.nilaimurni > 0.0 and self.nilaimurni or 0.0
            vals['creditkonversi'] = self.nilaimurni < 0.0 and -self.nilaimurni or 0.0

        else:

            # Single-currency.
            vals['amount_currency'] = 0.0
            vals['debit'] = self.price_unit > 0.0 and self.price_unit or 0.0
            vals['credit'] = self.price_unit < 0.0 and -self.price_unit or 0.0

            vals['creditkonversi'] = self.nilairiil < 0.0 and -self.nilairiil or 0.0
            vals['debitkonversi'] = self.nilairiil > 0.0 and self.nilairiil or 0.0



        return vals


