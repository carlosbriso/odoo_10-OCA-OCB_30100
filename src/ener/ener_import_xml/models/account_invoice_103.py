# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.exceptions import Warning
from datetime import datetime
import logging
import pprint

_logger = logging.getLogger(__name__)


###############################################################################
#   account.invoice.103                                                       #
###############################################################################

class AccountInvoice103(models.Model):
    _name = 'account.invoice.103'
    _rec_name = 'name'

    # --------------------------- ENTITY  FIELDS ------------------------------

    code = fields.Char(
        string='Code',
        required=True,
    )

    name = fields.Text(
        string='Name',
        required=True,
    )
