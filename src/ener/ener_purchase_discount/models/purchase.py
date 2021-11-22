# -*- coding: utf-8 -*-
# Copyright 2019 Anubía Solciones en la Nube, S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import odoo.addons.decimal_precision as dp

import logging
_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.depends('order_line.price_total')
    def _amount_all(self):
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                # FORWARDPORT UP TO 10.0
                if order.company_id.\
                   tax_calculation_rounding_method == 'round_globally':
                    if line.discount:
                        price_unit = (
                            line.price_unit * (100 - line.discount) / 100)
                    else:
                        price_unit = line.price_unit
                    taxes = line.taxes_id.compute_all(
                        price_unit, line.order_id.currency_id,
                        line.product_qty, product=line.product_id,
                        partner=line.order_id.partner_id)
                    amount_tax += sum(t.get('amount', 0.0) for t in taxes.get(
                        'taxes', []))
                else:
                    amount_tax += line.price_tax
            order.update({
                'amount_untaxed': order.currency_id.round(amount_untaxed),
                'amount_tax': order.currency_id.round(amount_tax),
                'amount_total': amount_untaxed + amount_tax,
            })


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.depends('product_qty', 'price_unit', 'taxes_id', 'discount')
    def _compute_amount(self):
        for line in self:
            if line.discount:
                price_unit_disc = line.price_unit * (100 - line.discount) / 100
            else:
                price_unit_disc = line.price_unit
            taxes = line.taxes_id.compute_all(
                price_unit_disc, line.order_id.currency_id, line.product_qty,
                product=line.product_id, partner=line.order_id.partner_id)
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })

    discount = fields.Float(
        string='Discount (%)',
        digits=dp.get_precision('Discount'),
    )

    @api.multi
    @api.constrains('discount')
    def _check_discount(self):
        for line in self:
            if line.discount < 0 or line.discount > 100:
                raise ValidationError(
                    _('Discounts in line must be a float among 0 and 100.')
                )
