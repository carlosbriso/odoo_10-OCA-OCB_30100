# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)

###############################################################################
#   account.invoice.confirm                                                   #
###############################################################################


class AccountInvoiceConfirmWizard(models.TransientModel):
    _name = 'account.invoice.confirm.wizard'

    # ---------------------------- ENTITY FIELDS ------------------------------

    msg_inv_validate = fields.Char(
        default=lambda s: _("Do you want validate this invoice?"),
        translated=True,
    )

    # ------------------------------ METHODS ---------------------------------

    @api.multi
    def validate(self):
        ai = self.env['account.invoice'].browse(
            self._context.get('active_id', False))
        if ai is False:
            raise Warning(
                _("Error validation: Invoice ID is False")
            )
        return ai.action_invoice_open()

###############################################################################
#   account.move                                                              #
###############################################################################


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    # ------------------------------ METHODS ---------------------------------

    @api.multi
    def check_year(self):
        self.ensure_one()
        current_year = datetime.today().year
        invoice_date = datetime.strptime(self.date_invoice, "%Y-%m-%d")
        if invoice_date.year == current_year:
            return self.action_invoice_open()
        else:
            return {
                'name': _('Are you sure?'),
                'type': 'ir.actions.act_window',
                'res_model': 'account.invoice.confirm.wizard',
                'view_mode': 'form',
                'view_type': 'form',
                'target': 'new',
            }

    # -------------------------- METHODS OVERRIDE -----------------------------
