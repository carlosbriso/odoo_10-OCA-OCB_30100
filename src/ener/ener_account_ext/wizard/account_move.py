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
#   account.move.confirm.wizard                                               #
###############################################################################

class AccountMoveConfirm(models.TransientModel):
    _name = 'account.move.confirm'

   # ---------------------------- ENTITY FIELDS ------------------------------

    msg_validate = fields.Char(
        default=lambda s: _("Do you want validate this accounting entry?"),
        translated=True,
    )

    # ------------------------------ METHODS ---------------------------------

    @api.multi
    def validate(self):
        am = self.env['account.move'].browse(
            self._context.get('active_id', False))
        if am is False:
            raise Warning(
                _("Error validation: Account move ID is False")
            )
        return am.post()

###############################################################################
#   account.move                                                              #
###############################################################################

class AccountMove(models.Model):
    _inherit = 'account.move'

    # ------------------------------ METHODS ---------------------------------

    @api.multi
    def check_year(self):
        self.ensure_one()
        current_year = datetime.today().year
        move_date = datetime.strptime(self.date, "%Y-%m-%d")
        if move_date.year == current_year:
            return self.post()
        else:
            return {
                'name': _('Are you sure?'),
                'type': 'ir.actions.act_window',
                'res_model': 'account.move.confirm',
                'view_mode': 'form',
                'view_type': 'form',
                'target': 'new',
            }

    # -------------------------- METHODS OVERRIDE -----------------------------

    @api.multi
    def post(self):
        invoice = self._context.get('invoice', False)
        res = super(AccountMove, self).post()
        for move in self:
            year_move_date = move.date.split("-")[0]
            year_name = move.name.split("/")[1]
            journal = move.journal_id
            if year_move_date != year_name:
                if journal.sequence_id:
                    # If invoice is actually refund and journal has a refund_sequence then use that one or use the regular one
                    sequence = journal.sequence_id
                    if invoice and invoice.type in ['out_refund', 'in_refund'] and journal.refund_sequence:
                        if not journal.refund_sequence_id:
                            raise UserError(_('Please define a sequence for the refunds'))
                        sequence = journal.refund_sequence_id
                    move.name = sequence.with_context(ir_sequence_date=move.date).next_by_id()
                else:
                    raise UserError(_('Please define a sequence on the journal.'))
        return res
