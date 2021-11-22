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


class AccountAssetAsset(models.Model):
    _inherit = 'account.asset.asset'

    trace_id = fields.Many2one(
        comodel_name='account.asset.asset.trace',
        string='Trace',
    )
    length = fields.Float(
        string='Length (m)',
        digits=dp.get_precision('Product Unit of Measure'),
    )
    line_type = fields.Selection(
        selection=[
            ('aerial', 'Aerial'),
            ('underground', 'Underground'),
            ('building', 'Building'),
        ],
        string='Line type',
    )
