# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import Warning
import odoo.addons.decimal_precision as dp
import logging

_logger = logging.getLogger(__name__)


class ResCountryParish(models.Model):
    _name = 'res.country.parish'

    name = fields.Char(
        string='Name',
        required=True,
    )
    state_id = fields.Many2one(
        string='State',
        required=True,
    )


class ResCountryNucleus(models.Model):
    _name = 'res.country.nucleus'

    name = fields.Char(
        string='Name',
        required=True,
    )
    state_id = fields.Many2one(
        string='State',
        required=True,
    )


class AccountAssetAssetTraceZone(models.Model):
    _name = 'account.asset.asset.trace.zone'

    name = fields.Char(
        string='Name',
        required=True,
    )


class AccountAssetAssetTraceCT(models.Model):
    _name = 'account.asset.asset.trace.ct'

    name = fields.Char(
        string='Name',
        required=True,
    )
    ct_type = fields.Selection(
        selection=[
            ('stand', 'Stand'),
            ('interior', 'Interior'),
            ('on_support', 'On Support'),
            ('on_portico', 'On Portico'),
        ],
        string='Ownership',
    )


class AccountAssetAssetTraceOriginLine(models.Model):
    _name = 'account.asset.asset.trace.origin.line'

    name = fields.Char(
        string='Name',
        required=True,
    )


class AccountAssetAssetTrace(models.Model):
    _name = 'account.asset.asset.trace'

    name = fields.Char(
        string='Name',
        required=True,
    )
    code = fields.Char(
        string='Code',
    )
    identificator = fields.Char(
        string='Identificator',
    )
    investment_plan = fields.Char(
        string='Investment Plan ID',
    )
    ownership = fields.Selection(
        selection=[
            ('own', 'Own'),
            ('assigned', 'Assigned'),
        ],
        string='Ownership',
    )
    financing_perc = fields.Float(
        digits=dp.get_precision('Discount'),
        string='Financing (%)',
        default=0.00,
    )
    assignment_date = fields.Date(
        string='Assignment Date',
    )
    city = fields.Char(
        string='City',
    )
    parish_id = fields.Many2one(
        comodel_name='res.country.parish',
        string='Parish',
    )
    urban_nucleus_id = fields.Many2one(
        comodel_name='res.country.core',
        string='Urban Nucleus',
    )
    state_id = fields.Many2one(
        comodel_name='res.country.state',
        string='State',
    )
    zone_id = fields.Many2one(
        comodel_name='account.asset.asset.trace.zone',
        string='Zone',
    )
    ct_id = fields.Many2one(
        comodel_name='account.asset.asset.trace.ct',
        string='CT Name',
    )
    ct_type = fields.Selection(
        related='ct_id.ct_type',
        string='CT Type',
    )
    particular = fields.Selection(
        selection=[
            ('yes', 'Yes'),
            ('no', 'No'),
        ],
        string='Particular',
    )
    low_voltage = fields.Char(
        string='Low Voltage',
    )
    input_voltage = fields.Char(
        string='Input Voltage (V)',
    )
    voltage = fields.Char(
        string='Voltage',
    )
    exp_name = fields.Char(
        string='Exp. Name',
    )
    transformers_number = fields.Integer(
        string='Transformers Number',
    )
    transformation_pot = fields.Integer(
        string='Transformation Pot. (KVA)',
    )
    line_type = fields.Selection(
        selection=[
            ('main', 'Main Line'),
            ('derivation', 'Derivation'),
            ('subderivation', 'Subderivation'),
        ],
        string='Ownership',
    )
    origin_line = fields.Many2one(
        comodel_name='account.asset.asset.trace.origin.line',
        string='Origin Line',
    )
    origin_type = fields.Selection(
        selection=[
            ('transformation_centre', 'Transformation Centre'),
            ('support', 'Support'),
            ('junction', 'Junction'),
            ('substation', 'Substation'),
        ],
        string='Ownership',
    )
    output_sockets_number = fields.Integer(
        string='Output Sockets Number',
    )
    trace_class = fields.Selection(
        selection=[
            ('transformation_manoeuvre', 'Transformation Manoeuvre'),
            ('transformation', 'Transformation'),
            ('manoeuvre', 'Manoeuvre'),
        ],
        string='Ownership',
    )
    length = fields.Float(
        string='Length (m)',
        digits=dp.get_precision('Product Unit of Measure'),
    )
    # product_uom = fields.Many2one(
    #     comodel_name='product.uom',
    #     string='Unit of Measure',
    #     domain=lambda self: [
    #         ('category_id', '=', self.env.ref('product.uom_categ_length').id),
    #     ],
    #     default=lambda self: self.env.ref('product.product_uom_meter'),
    # )
