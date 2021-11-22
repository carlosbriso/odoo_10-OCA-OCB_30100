# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


###############################################################################
#   trial.balance.report.wizard                                               #
###############################################################################

class TrialBalanceReportWizard(models.TransientModel):
    _inherit = 'trial.balance.report.wizard'

    # ----------------------- AUXILIARY FIELD METHODS -------------------------

    @api.onchange('acc_from')
    def _onchange_acc_from(self):
        if self.acc_from and self.acc_to:
            account_ids = self.env['account.account'].search([
                ('code_number', '>=', self.acc_from),
                ('code_number', '<=', self.acc_to)
            ])
            self.account_ids = [(6, 0, account_ids.mapped('id'))]
        elif self.acc_from:
            account_ids = self.env['account.account'].search([
                ('code_number', '>=', self.acc_from)
            ])
            self.account_ids = [(6, 0, account_ids.mapped('id'))]

    @api.onchange('acc_to')
    def _onchange_acc_to(self):
        if self.acc_from and self.acc_to:
            account_ids = self.env['account.account'].search([
                ('code_number', '>=', self.acc_from),
                ('code_number', '<=', self.acc_to)
            ])
            self.account_ids = [(6, 0, account_ids.mapped('id'))]
        elif self.acc_to:
            account_ids = self.env['account.account'].search([
                ('code_number', '<=', self.acc_to)
            ])
            self.account_ids = [(6, 0, account_ids.mapped('id'))]

    # ---------------------------- ENTITY FIELDS ------------------------------

    acc_from = fields.Integer(
        string='From'
    )

    acc_to = fields.Integer(
        string='To'
    )
