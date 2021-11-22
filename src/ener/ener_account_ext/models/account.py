# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


###############################################################################
#   account.account                                                           #
###############################################################################

class AccountAccount(models.Model):
    _inherit = 'account.account'

    # ----------------------- AUXILIARY FIELD METHODS -------------------------

    @api.multi
    def _compute_code_number(self):
        for record in self:
            record.code_number = int(record.code)

    @api.multi
    @api.depends('move_lines', 'move_lines.credit', 'move_lines.debit',
                 'move_lines.move_id', 'move_lines.move_id.state')
    def _compute_credit_debit(self):
        for account in self:
            if len(account.move_lines) > 0:
                sql_query = """SELECT SUM(aml.credit) AS credit,
                                      SUM(aml.debit) AS debit
                               FROM account_move_line aml
                               JOIN account_move am
                               ON aml.move_id = am.id
                               WHERE am.state = 'posted'
                               AND aml.account_id = %s
                            """
                self.env.cr.execute(sql_query, (tuple([account.id])))
                [results] = self.env.cr.dictfetchall()
                credit = results.get('credit', 0.0) or 0.0
                debit = results.get('debit', 0.0) or 0.0
                account.credit = credit
                account.debit = debit
                account.balance = debit - credit

    # ---------------------------- ENTITY FIELDS ------------------------------

    code_number = fields.Integer(
        string='Code number',
        compute='_compute_code_number',
        store=True
    )

    move_lines = fields.One2many(
        comodel_name='account.move.line',
        inverse_name='account_id',
        string='Move lines',
    )

    debit = fields.Monetary(
        compute='_compute_credit_debit',
        currency_field='currency_id',
    )

    credit = fields.Monetary(
        compute='_compute_credit_debit',
        currency_field='currency_id',
    )

    balance = fields.Monetary(
        compute='_compute_credit_debit',
        # store=True,
        currency_field='currency_id',
    )


###############################################################################
#   account.invoice                                                           #
###############################################################################

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    # ---------------------------- ENTITY FIELDS ------------------------------

    doc = fields.Char(
        string='Doc',
    )
    nref = fields.Char(
        string='N/Ref'
    )
    sref = fields.Char(
        string='S/Ref'
    )

    # ------------------------ METHODS  OVERWRITTEN ---------------------------

    @api.multi
    def action_move_create(self):
        result = super(AccountInvoice, self).action_move_create()
        for invoice in self:
            if invoice.doc and invoice.move_id:
                invoice.move_id.write({
                    'doc': invoice.doc,
                    'description': invoice.name,
                })
        return result

    @api.multi
    def write(self, vals):
        result = super(AccountInvoice, self).write(vals)
        for invoice in self:
            if vals.get('doc') and invoice.move_id:
                invoice.move_id.write({
                    'doc': vals.get('doc'),
                })
        return result


###############################################################################
#   account.move                                                              #
###############################################################################

class AccountMove(models.Model):
    _inherit = 'account.move'

    # ---------------------------- ENTITY FIELDS ------------------------------

    doc = fields.Char(
        string='Doc',
    )

    description = fields.Char(
        string='Description',
        readonly=True,
    )
