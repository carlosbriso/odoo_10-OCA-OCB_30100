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
#   res.partner                                                               #
###############################################################################

class Partner(models.Model):
    _inherit = 'res.partner'

    # ------------------------ METHODS  OVERWRITTEN ---------------------------

    @api.model
    def create(self, values):
        result = super(Partner, self).create(values)
        if 'vat' in values:
            partners = self.env['res.partner'].search([
                ('vat', '=', values['vat']),
                ('parent_id', '=', False)
            ])
            if len(partners) > 1:
                raise Warning(_('Partner VAT must be unique.'))
        return result

    @api.multi
    def write(self, values):
        result = super(Partner, self).write(values)
        if 'vat' in values:
            partners = self.env['res.partner'].search([
                ('vat', '=', values['vat']),
                ('parent_id', '=', False)
            ])
            if len(partners) > 1:
                raise Warning(_('Partner VAT must be unique.'))
        return result
