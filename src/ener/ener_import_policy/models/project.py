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


class ProjectTask(models.Model):
    _inherit = 'project.task'

    # ---------------------------- ENTITY FIELDS ------------------------------

    policy_id = fields.Many2one(
        string='Policy',
        comodel_name='policy.policy',
    )

    name_policy = fields.Char(
        string='Policy',
        related='policy_id.name',
    )

    partner = fields.Char(
        string='Partner',
        related='policy_id.partner',
    )

    address = fields.Char(
        string='Address',
        related='policy_id.address',
    )

    user = fields.Char(
        string='Person in charge',
        related='policy_id.user',
    )

    price = fields.Char(
        string='Price',
        related='policy_id.price',
    )

    policy_date_start = fields.Date(
        string='Date start',
        related='policy_id.policy_date_start',
    )

    policy_date_end = fields.Date(
        string='Date end',
        related='policy_id.policy_date_end',
    )

    cups = fields.Char(
        string='CUPS',
        related='policy_id.cups',
    )

    technology = fields.Char(
        string='Technology',
        related='policy_id.technology',
    )

    type_point_messure = fields.Integer(
        string='Type point messure',
        related='policy_id.type_point_messure',
    )

    type_installation = fields.Char(
        string='Type installation',
        related='policy_id.type_installation',
    )

    type_read = fields.Char(
        string='Type read',
        related='policy_id.type_read',
    )

    brand = fields.Char(
        string='Brand',
        related='policy_id.brand',
    )

    model = fields.Char(
        string="Model",
        related='policy_id.model',
    )

    serial_number = fields.Char(
        string='Serial Number',
        related='policy_id.serial_number',
    )

    rules = fields.Char(
        string='Rules',
        related='policy_id.rules',
    )

    name_description = fields.Char(
        string='Name description',
        related='policy_id.name_description',
    )

    voltage = fields.Integer(
        string='Voltage',
        related='policy_id.voltage',
    )

    namect = fields.Char(
        string='NameCT',
        related='policy_id.namect',
    )

    id5 = fields.Char(
        string='ID5',
        related='policy_id.id5',
    )

    pcp1 = fields.Float(
        string='PCP1',
        related='policy_id.pcp1',
    )

    pcp2 = fields.Float(
        string='PCP2',
        related='policy_id.pcp2',
    )

    pcp3 = fields.Float(
        string='PCP3',
        related='policy_id.pcp3',
    )

    pcp4 = fields.Float(
        string='PCP4',
        related='policy_id.pcp3',
    )

    pcp5 = fields.Float(
        string='PCP5',
        related='policy_id.pcp5',
    )

    pcp6 = fields.Float(
        string='PCP6',
        related='policy_id.pcp6',
    )
