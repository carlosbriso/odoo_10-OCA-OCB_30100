# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


##############################################################################
#  policy.policy                                                             #
##############################################################################


class PolicyPolicy(models.Model):
    _name = 'policy.policy'

    # ---------------------------- ENTITY FIELDS ------------------------------

    task_ids = fields.One2many(
        string='Tasks',
        comodel_name='project.task',
        inverse_name='policy_id',
    )

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

    # ----------------------------- CONSTRAINTS -------------------------------

    sql_constraints = [
        ('policy_unique', 'UNIQUE (name)',
            'You can not have two policies with the same number')
    ]
