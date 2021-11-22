# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    previous_move_id = fields.Many2one(
        string='Journal Entry',
        comodel_name='account.move',
    )

    @api.model
    def force_paid_state_action(self, ids):
        invoices = self.env['account.invoice'].search([
            ('id', 'in', ids)
        ])
        for invoice in invoices:
            move = invoice.move_id
            invoice.write({'move_id': False, 'state': 'paid', 'previous_move_id': move.id})
            invoice.write({'residual': 0.0})
