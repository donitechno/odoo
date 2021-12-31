# Copyright (C) 2013 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# Copyright (C) 2015 Akretion (<http://www.akretion.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class PembayaranWizard(models.TransientModel):
    _name = "jewellery_management.pembayaran.wizard"
    _description = "pembayaran"

    def _default_currency_id(self):
        company_id = self.env.context.get('force_company') or self.env.context.get('company_id') or self.env.company.id
        return self.env['res.company'].browse(company_id).currency_id

    journal_id = fields.Many2one("account.journal", string="Type Pembayaran")
    amount_total = fields.Monetary(string='Jumlah', readonly=True)
    jumlah_diterima = fields.Monetary(string='Jumlah yang diterima',)
    sisa_kembalian = fields.Monetary(string='Kembalian', readonly=True, store=True, compute='_sisa_kembalian',)
    currency_id = fields.Many2one('res.currency', 'Currency', required=True, default=_default_currency_id)

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        if not fields:
            return res
        context = self.env.context
        return res

    def validate(self):
        for record in self.env['order.pembelian'].browse(self._context.get('active_ids', [])):
            # here you can access target table fields using *record* variable
            record.write({'state':'validate'})
        return True

    @api.depends('jumlah_diterima')
    def _sisa_kembalian(self):
        for model in self:
            model.sisa_kembalian = model.jumlah_diterima - model.amount_total

