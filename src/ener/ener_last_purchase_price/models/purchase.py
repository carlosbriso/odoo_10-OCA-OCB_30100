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
#   purchase.order                                                            #
###############################################################################

class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    # ------------------------ METHODS  OVERWRITTEN ---------------------------

    @api.multi
    def button_confirm(self):
        result = super(PurchaseOrder, self).button_confirm()
        for purchase in self:
            for line in purchase.order_line:
                if line.product_id:
                    line.product_id.write({
                        'standard_price': line.price_unit
                    })
        return result
