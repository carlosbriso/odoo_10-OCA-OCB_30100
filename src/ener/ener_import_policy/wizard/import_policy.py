# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import Warning
import logging

_logger = logging.getLogger(__name__)


###############################################################################
# import.policy                                                               #
###############################################################################

class ImportPolicy(models.TransientModel):
    _name = 'import.policy'

    # --------------------------- ENTITY  FIELDS ------------------------------

    name = fields.Char(
        string='Policy',
    )

    partner = fields.Char(
        string='Partner',
    )

    address = fields.Char(
        string='Address',
    )

    user = fields.Char(
        string='Person in charge',
    )

    price = fields.Char(
        string='Price',
    )

    policy_date_start = fields.Date(
        string='Date start',
    )

    policy_date_end = fields.Date(
        string='Date end',
    )

    cups = fields.Char(
        string='CUPS',
    )

    technology = fields.Char(
        string='Technology',
    )

    type_point_messure = fields.Integer(
        string='Type point messure',
    )

    type_installation = fields.Char(
        string='Type installation',
    )

    type_read = fields.Char(
        string='Type read',
    )

    brand = fields.Char(
        string='Brand',
    )

    model = fields.Char(
        string="Model",
    )

    serial_number = fields.Char(
        string='Serial Number',
    )

    rules = fields.Char(
        string='Rules',
    )

    name_description = fields.Char(
        string='Name description',
    )

    voltage = fields.Integer(
        string='Voltage',
    )

    namect = fields.Char(
        string='NameCT',
    )

    id5 = fields.Char(
        string='ID5',
    )

    pcp1 = fields.Float(
        string='PCP1',
    )

    pcp2 = fields.Float(
        string='PCP2',
    )

    pcp3 = fields.Float(
        string='PCP3',
    )

    pcp4 = fields.Float(
        string='PCP4',
    )

    pcp5 = fields.Float(
        string='PCP5',
    )

    pcp6 = fields.Float(
        string='PCP6',
    )

    msg = fields.Text(
        string='Result',
        readonly=True,
    )

    strong = fields.Boolean(
        string='Strong',
        readonly=True,
        default=True,
    )

    # ------------------------ METHODS  OVERWRITTEN ---------------------------

    @api.model
    def create(self, vals):
        # Remove all messages
        # self.search([]).unlink()
        self.search([]).write({
            'strong': False,
        })
        wzd = super(ImportPolicy, self).create(vals)
        policy = self.env['policy.policy'].search([('name', '=', wzd.name)])
        if len(policy) == 1:
            policy.write(vals)
            msg = _('The policy {} has been modified.'.format(policy.name))
        elif len(policy) == 0:
            new_policy = self.env['policy.policy'].create(vals)
            msg = _('The policy {} has been generated.'.format(new_policy.name))
        else:
            raise Warning(
                _('More than one policy found with the reference {}. '
                  .format(wzd.name)),
            )
        wzd.write({
            'msg': msg,
        })
        return wzd
