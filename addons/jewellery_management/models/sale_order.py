from odoo import models, fields, api
from odoo.addons import decimal_precision as dp
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_compare, float_round

class SaleOrder(models.Model):    
    
    _inherit = 'sale.order'

    total_weight = fields.Float("Total Weight", digits= dp.get_precision('Stock Weight'))
    
    


class SaleOrderLine(models.Model):    
    
    _inherit = 'sale.order.line'

    @api.depends('nilairiil', 'product_uom_qty', 'tarif')
    def _compute_nilaimurni(self):
        for record in self:
            record.nilaimurni = (record.nilairiil * record.tarif) * record.product_uom_qty

    @api.depends('nilaimurni', 'currency_id')
    def _compute_nilaikonversi(self):
        if not self.currency_id:
            self.currency_id = self.order_id.currency_id

        for record in self:
            record.nilaikonversi = record.nilaimurni * record.order_id.currency_id.tarifjualharga
            record.price_unit = record.nilaikonversi
            record.sub_total = record.nilaikonversi

    #weight = fields.Float("Weight", digits= dp.get_precision('Stock Weight'))
    tarif = fields.Float("Tarif", digits= dp.get_precision('Stock Weight'))
    nilairiil = fields.Float("Nilai Riil", digits= dp.get_precision('Stock Weight'))
    nilaimurni= fields.Float("Nilai Murni", digits= dp.get_precision('Stock Weight'),  compute=_compute_nilaimurni, store=True)
    nilaikonversi=fields.Float("Nilai Konversi", digits= dp.get_precision('Stock Weight'), compute= _compute_nilaikonversi, store=True)
    #tarif = field.Fields()

    def _prepare_invoice_line(self):
        self.ensure_one()
        res = super(SaleOrderLine, self)._prepare_invoice_line()
        res['nilairiil']= self.nilairiil
        res['tarif']= self.tarif
        res['nilaimurni']= self.nilaimurni
        res['nilaikonversi']= self.nilaikonversi
        return res

    def _prepare_procurement_values(self, group_id=False):
        values = super(SaleOrderLine,self)._prepare_procurement_values(group_id)
        values['nilairiil']  = self.nilairiil
        return values

    def _get_qty_procurement(self, previous_product_uom_qty=False):
        self.ensure_one()
        super(SaleOrderLine, self)._get_qty_procurement()
        qty = 0.0
        nilairiil = 0.0
        outgoing_moves, incoming_moves = self._get_outgoing_incoming_moves()
        for move in outgoing_moves:
            nilairiil += move.nilairiil

        for move in incoming_moves:
            nilairiil -= move.nilairiil
        return qty, nilairiil

    # def _action_launch_stock_rule(self, previous_product_uom_qty=False):
    #     """
    #     Launch procurement group run method with required/custom fields genrated by a
    #     sale order line. procurement group will launch '_run_pull', '_run_buy' or '_run_manufacture'
    #     depending on the sale order line product rule.
    #     """
    #     vals = super(SaleOrderLine, self)._action_launch_stock_rule(previous_product_uom_qty)
    #     precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
    #     procurements = []
    #     for line in self:
    #         if line.state != 'sale' or not line.product_id.type in ('consu','product'):
    #             continue
    #         qty, nilairiil = line._get_qty_procurement(previous_product_uom_qty)
    #
    #         group_id = line._get_procurement_group()
    #         if not group_id:
    #             group_id = self.env['procurement.group'].create(line._prepare_procurement_group_vals())
    #             line.order_id.procurement_group_id = group_id
    #         else:
    #             # In case the procurement group is already created and the order was
    #             # cancelled, we need to update certain values of the group.
    #             updated_vals = {}
    #             if group_id.partner_id != line.order_id.partner_shipping_id:
    #                 updated_vals.update({'partner_id': line.order_id.partner_shipping_id.id})
    #             if group_id.move_type != line.order_id.picking_policy:
    #                 updated_vals.update({'move_type': line.order_id.picking_policy})
    #             if updated_vals:
    #                 group_id.write(updated_vals)
    #
    #         values = line._prepare_procurement_values(group_id=group_id)
    #         product_qty = line.product_uom_qty - qty
    #         product_nilairiil = line.nilairiil - nilairiil
    #
    #         line_uom = line.product_uom
    #         quant_uom = line.product_id.uom_id
    #         product_qty, procurement_uom = line_uom._adjust_uom_quantities(product_qty, quant_uom)
    #         procurements.append(self.env['procurement.group'].Procurement(
    #             line.product_id, product_qty, procurement_uom,
    #             line.order_id.partner_shipping_id.property_stock_customer,
    #             line.name, line.order_id.name, line.order_id.company_id, values, product_nilairiil))
    #     if procurements:
    #         self.env['procurement.group'].run(procurements)
    #
    #     return True

    # @api.onchange('product_template_id')
    # def _onchange_product_template_id(self):
    #
    #     for line in self:
    #         currency_rate =  line.order_id.pricelist_id.currency_id.rate
    #         line.weight = line.product_template_id.weight
    #         price = line.weight * currency_rate
    #         line.product_template_id.update({
    #             'list_price': price
    #         })
    #         line.write({
    #             'price_unit':price
    #         })
    #
    #
    #
    #
    #

