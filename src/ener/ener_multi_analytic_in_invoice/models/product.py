# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import Warning
import logging
import pprint

_logger = logging.getLogger(__name__)

###############################################################################
#   product.product                                                           #
###############################################################################

class ProductProduct(models.Model):

    _inherit = "product.product"

    # ------------------------ METHODS  OVERWRITTEN ---------------------------

    @api.model
    def _convert_prepared_anglosaxon_line(self, line, partner):
        return {
            'invl_id': line.get('invl_id', False),
            'date_maturity': line.get('date_maturity', False),
            'partner_id': partner,
            'name': line['name'],
            'debit': line['price'] > 0 and line['price'],
            'credit': line['price'] < 0 and -line['price'],
            'account_id': line['account_id'],
            'analytic_line_ids': line.get('analytic_line_ids', []),
            'amount_currency': line['price'] > 0 and abs(
                line.get('amount_currency', False)) or \
                -abs(line.get('amount_currency', False)),
            'currency_id': line.get('currency_id', False),
            'quantity': line.get('quantity', 1.00),
            'product_id': line.get('product_id', False),
            'product_uom_id': line.get('uom_id', False),
            'analytic_account_id': line.get('account_analytic_id', False),
            'analytic_account_ids': line.get('account_analytic_ids', False),
            'invoice_id': line.get('invoice_id', False),
            'tax_ids': line.get('tax_ids', False),
            'tax_line_id': line.get('tax_line_id', False),
            'analytic_tag_ids': line.get('analytic_tag_ids', False),
        }
