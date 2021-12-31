# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta
from functools import partial
from itertools import groupby

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.misc import formatLang, get_lang
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare



from werkzeug.urls import url_encode
from odoo.addons import decimal_precision as dp

class MutasiStock(models.Model):
    _name = "mutasi.stock"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = " Mutasi Stock "
    _order = 'tanggal_diterima desc, id desc'

    def _default_currency_id(self):
        company_id = self.env.context.get('force_company') or self.env.context.get('company_id') or self.env.company.id
        return self.env['res.company'].browse(company_id).currency_id

    @api.depends('nilairiil', 'tarif')
    def _compute_nilaimurni(self):
        for record in self:
            record.nilaimurni = (record.nilairiil * record.tarif)
    @api.depends('nilaimurni', 'currency_id')
    def _compute_nilaikonversi(self):
        if not self.currency_id:
            self.currency_id = self.order_id._default_currency_id()

    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    reference = fields.Char(string='No Ref.', copy=False,
        help='The payment communication of this sale order.')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Bayar'),
        ('validate', 'Validasi'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, default='draft')
    tanggal_diterima = fields.Datetime(string='Order Date', required=True, readonly=False, index=True,  copy=False, default=fields.Datetime.now, help="Creation date of draft/sent orders,\nConfirmation date of confirmed orders.")

    user_id = fields.Many2one(
        'res.users', string='Salesperson', index=True, tracking=2, default=lambda self: self.env.user,
        domain=lambda self: [('groups_id', 'in', self.env.ref('sales_team.group_sale_salesman').id)])
    penerima_id = fields.Many2one(
        'res.partner', string='Customer', readonly=False,

        required=False, change_default=True, index=True, tracking=1,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",)

    currency_id = fields.Many2one("res.currency", string="Currency",  required=False, default=_default_currency_id,)

    note = fields.Text(' Keterangan ', )

    nominal = fields.Monetary(string='Jumlah', store=True, readonly=False,)
    currency_rate = fields.Float("Currency Rate", compute='_compute_currency_rate', compute_sudo=True, store=True, digits=(12, 6), readonly=True, help='The rate of the currency to the currency of rate 1 applicable at the date of the order')

    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company)
    account_penerima_id = fields.Many2one('account.account', string='Account Penerima', required=False,

                                 domain="[('company_id', '=', company_id)]",
                                 )
    account_sumber_id = fields.Many2one('account.account', string='Account Sumber', required=True,

                                          domain="[('company_id', '=', company_id)]",
                                          )

    journal_id = fields.Many2one('account.journal', string='Journal', required=True, readonly=False,

                                 domain="[('company_id', '=', company_id)]",
                                 )

    tarif = fields.Float("Tarif", digits=dp.get_precision('Stock Weight'))
    nilairiil = fields.Float("Nilai Riil", digits=dp.get_precision('Stock Weight'), required=True)
    nilaimurni = fields.Float("Nilai Murni", digits=dp.get_precision('Stock Weight'), compute=_compute_nilaimurni,
                              store=True)
    nilaikonversi = fields.Float("Nilai Konversi", digits=dp.get_precision('Stock Weight'),
                                 compute=_compute_nilaikonversi, store=True)

    account_line = fields.One2many('mutasi.stock.detail', 'account_id', string='Account Sumber', copy=True,
                                   auto_join=True)


class MutasiStockDetail(models.Model):
    _name = "mutasi.stock.detail"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = " stock detail"

    name = fields.Char(string='Order Reference', required=False, copy=False, readonly=True,  index=True, default=lambda self: _('New'))
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Bayar'),
        ('validate', 'Validasi'),
        ('done', 'Locked'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, default='draft')

    note = fields.Text(' Keterangan ', )

    account_sumber_id = fields.Many2one('account.account', string='Account Sumber', required=True,)

    account_id = fields.Many2one('mutasi.stock', string='detail', required=True, ondelete='cascade',
                               index=True, copy=False)

    tarif = fields.Float("Tarif", digits=dp.get_precision('Stock Weight'))
    nilairiil = fields.Float("Nominal", digits=dp.get_precision('Stock Weight'), required=True)
    nilaimurni = fields.Float("Nilai Murni", digits=dp.get_precision('Stock Weight'),
                              store=True)
    nilaikonversi = fields.Float("Nilai Konversi", digits=dp.get_precision('Stock Weight'),
                                 store=True)
    #product_id = fields.Many2one(
        #'product.product', string='Product')



