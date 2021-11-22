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
#   account.analytic.line                                                     #
###############################################################################

class AccountAnalyticLine(models.Model):

    _inherit = 'account.analytic.line'

    # ------------------------ METHODS  OVERWRITTEN ---------------------------

    @api.model
    def create(self, values):
        result = super(AccountAnalyticLine, self).create(values)
        return result

    @api.multi
    def write(self, values):
        result = super(AccountAnalyticLine, self).write(values)
        return result

###############################################################################
#   account.invoice                                                           #
###############################################################################

class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    # ------------------------ METHODS  OVERWRITTEN ---------------------------

    @api.model
    def invoice_line_move_line_get(self):
        res = []
        for line in self.invoice_line_ids:
            if line.quantity==0:
                continue
            tax_ids = []
            for tax in line.invoice_line_tax_ids:
                tax_ids.append((4, tax.id, None))
                for child in tax.children_tax_ids:
                    if child.type_tax_use != 'none':
                        tax_ids.append((4, child.id, None))
            analytic_tag_ids = [(4, analytic_tag.id, None) for analytic_tag \
                in line.analytic_tag_ids]
            move_line_dict = {
                'invl_id': line.id,
                'type': 'src',
                'name': line.name.split('\n')[0][:64],
                'price_unit': line.price_unit,
                'quantity': line.quantity,
                'price': line.price_subtotal,
                'account_id': line.account_id.id,
                'product_id': line.product_id.id,
                'uom_id': line.uom_id.id,
                'account_analytic_id': line.account_analytic_id.id,
                'account_analytic_ids': line.account_analytic_ids,
                'tax_ids': tax_ids,
                'invoice_id': self.id,
                'analytic_tag_ids': analytic_tag_ids
            }
            res.append(move_line_dict)
        return res

    def inv_line_characteristic_hashcode(self, invoice_line):
        return "%s-%s-%s-%s-%s-%s-%s" % (
            invoice_line['account_id'],
            invoice_line.get('invl_id', 'False'),
            invoice_line.get('tax_ids', 'False'),
            invoice_line.get('tax_line_id', 'False'),
            invoice_line.get('product_id', 'False'),
            invoice_line.get('analytic_account_id', 'False'),
            invoice_line.get('analytic_account_ids', 'False'),
            invoice_line.get('date_maturity', 'False'),
            invoice_line.get('analytic_tag_ids', 'False'),
        )

###############################################################################
#   account.invoice.line                                                      #
###############################################################################

class AccountInvoiceLine(models.Model):

    _inherit = 'account.invoice.line'

    # --------------------------- ENTITY  FIELDS ------------------------------

    account_analytic_ids = fields.Many2many(
        comodel_name='account.analytic.account',
        relation='account_invoice_line_account_analytic_rel',
        column1='invoice_line_id',
        column2='analytic_account_id',
        string='Analytic accounts',
    )

    analytic_ids = fields.One2many(
        comodel_name='account.invoice.line.analytic',
        inverse_name='account_invoice_line_id',
        string='Analytics',
    )

    # ----------------------------- NEW METHODS -------------------------------

    @api.multi
    def act_invoice_line_2_analytic(self):
        view_tree = self.env.ref(
            'ener_multi_analytic_in_invoice.invoice_line_analytic_tree', False)
        return {
            'name': _('Analytics'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.invoice.line.analytic',
            'views': [
                (view_tree.id, 'tree'),
            ],
            'view_id': view_tree.id,
            'domain': [(
                'account_invoice_line_id', '=', self.id,
            )],
            'context': {
                'default_account_invoice_line_id': self.id,
            },
            'groups_id': '[(4, ref("base.group_user"))]',
            'target': 'current',
            'flags': {
                'action_buttons': True,
            },
        }

###############################################################################
#   account.invoice.line.analytic                                             #
###############################################################################

class AccountInvoiceLineAnalytic(models.Model):

    _name = 'account.invoice.line.analytic'

    # ----------------------- AUXILIARY FIELD METHODS -------------------------

    @api.multi
    @api.depends('analytic_percent')
    def _compute_amount_result(self):
        for record in self:
            price_subtotal = \
                record.account_invoice_line_id.price_subtotal
            record.analytic_result = price_subtotal * \
                (record.analytic_percent / 100)

    # --------------------------- ENTITY  FIELDS ------------------------------

    account_analytic_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Analytic account',
        required=True,
    )

    analytic_percent = fields.Float(
        string='Analytic percent',
        required=True,
        default=100.0,
    )

    analytic_result = fields.Float(
        compute='_compute_amount_result',
        string='Analytic result',
    )

    account_invoice_line_id = fields.Many2one(
        comodel_name='account.invoice.line',
        string='Invoice line',
    )

    # ------------------------ METHODS  OVERWRITTEN ---------------------------

    @api.model
    def create(self, values):
        result = super(AccountInvoiceLineAnalytic, self).create(values)
        invoice_line = self.env['account.invoice.line'].search([
            ('id', '=', values['account_invoice_line_id'])
        ])
        invoice_line.write({
            'account_analytic_ids': [(4, values['account_analytic_id'])],
        })
        return result

    @api.multi
    def write(self, values):
        result = super(AccountInvoiceLineAnalytic, self).write(values)
        return result

    @api.multi
    def unlink(self):
        for record in self:
            invoice_line = self.env['account.invoice.line'].search([
                ('id', '=', record.account_invoice_line_id.id)
            ])
            if len(invoice_line.account_analytic_ids) > 0:
                aa_id = record.account_analytic_id.id
                invoice_line.write({
                    'account_analytic_ids': [(3, aa_id)],
                })
        result = super(AccountInvoiceLineAnalytic, self).unlink()
        return result

    @api.model
    def default_get(self, fields):
        rec = super(AccountInvoiceLineAnalytic, self).default_get(fields)
        active_ids = self.env.context.get('active_ids', False)
        invoice_lines = self.env['account.invoice.line'].search([
            ('id', 'in', active_ids),
        ])
        restant_percent = 100.0
        if len(invoice_lines) > 0:
            invoice_line = invoice_lines[0]
            for analytic in invoice_line.analytic_ids:
                restant_percent -= analytic.analytic_percent
        rec.update({
            'analytic_percent': restant_percent,
        })
        return rec

###############################################################################
#   account.move.line                                                         #
###############################################################################

class AccountMoveLine(models.Model):

    _inherit = 'account.move.line'

    # --------------------------- ENTITY  FIELDS ------------------------------

    invl_id = fields.Many2one(
        comodel_name='account.invoice.line',
        string='Invoice line',
    )

    analytic_account_ids = fields.Many2many(
        comodel_name='account.analytic.account',
        relation='account_move_line_account_analytic_rel',
        column1='move_line_id',
        column2='analytic_account_id',
        string='Analytic accounts',
    )

    # ------------------------ METHODS  OVERWRITTEN ---------------------------

    @api.model
    def create(self, values):
        result = super(AccountMoveLine, self).create(values)
        if 'analytic_account_ids' in values:
            result['analytic_account_ids'] = values['analytic_account_ids']
        if 'invl_id' in values:
            result['invl_id'] = values['invl_id']
        return result

    @api.multi
    def write(self, values):
        result = super(AccountMoveLine, self).write(values)
        return result

    # ------------------------ METHODS  OVERWRITTEN ---------------------------

    @api.multi
    def create_analytic_lines(self):
        self.mapped('analytic_line_ids').unlink()
        for obj_line in self:
            len_aa = len(obj_line.analytic_account_ids)
            if len_aa > 0:
                for analytic_account_id in obj_line.analytic_account_ids:
                    if len(obj_line.invl_id) > 0:
                        invoice_lines = obj_line.invl_id
                        for analytic in invoice_lines.analytic_ids:
                            if analytic.account_analytic_id.id == \
                                analytic_account_id.id:
                                vals_line = obj_line._prepare_analytic_line(
                                    analytic_account_id.id, \
                                        analytic.analytic_percent)[0]
                                self.env['account.analytic.line'].create(
                                    vals_line)

    @api.one
    def _prepare_analytic_line(self, analytic_account_id=False, percent=100):
        amount = (self.credit or 0.0) - (self.debit or 0.0)
        return {
            'name': self.name,
            'date': self.date,
            'account_id': analytic_account_id,
            'tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'unit_amount': self.quantity,
            'product_id': self.product_id and self.product_id.id or False,
            'product_uom_id': self.product_uom_id and self.product_uom_id.id \
                or False,
            'amount': self.company_currency_id.with_context(date=self.date or \
                fields.Date.context_today(self)).compute(amount,
                self.analytic_account_id.currency_id) * (percent / 100) \
                    if self.analytic_account_id.currency_id else amount * \
                        (percent / 100),
            'general_account_id': self.account_id.id,
            'ref': self.ref,
            'move_id': self.id,
            'user_id': self.invoice_id.user_id.id or self._uid,
        }
