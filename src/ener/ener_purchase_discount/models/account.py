# -*- coding: utf-8 -*-
# Copyright 2019 Anubía Solciones en la Nube, S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models

import logging
_logger = logging.getLogger(__name__)


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    def _set_additional_fields(self, invoice):
        if self.purchase_line_id:
            self.discount = self.purchase_line_id.discount
        super(AccountInvoiceLine, self)._set_additional_fields(invoice)
