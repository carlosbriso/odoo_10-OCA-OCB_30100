# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import Warning
import logging

_logger = logging.getLogger(__name__)


###############################################################################
#   product.product                                                           #
###############################################################################

class Product(models.Model):
    _inherit = 'product.product'

    # ------------------------ METHODS  OVERWRITTEN ---------------------------

    @api.model
    def create(self, values):
        result = super(Product, self).create(values)
        if 'default_code' in values:
            products = self.env['product.product'].search([
                ('default_code', '=', values['default_code'])
            ])
            if len(products) > 1:
                raise Warning(_('Product default code must be unique.'))
        return result

    @api.multi
    def write(self, values):
        result = super(Product, self).write(values)
        if 'default_code' in values:
            products = self.env['product.product'].search([
                ('default_code', '=', values['default_code'])
            ])
            if len(products) > 1:
                raise Warning(_('Product default code must be unique.'))
        return result
