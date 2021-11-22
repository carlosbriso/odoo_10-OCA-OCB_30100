# -*- coding: utf-8 -*-
# Copyright 2019 Anubía Solciones en la Nube, S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models

import logging
_logger = logging.getLogger(__name__)


class FleetVehicleLogServices(models.Model):
    _inherit = 'fleet.vehicle.log.services'

    cost_ids = fields.One2many(
        comodel_name='fleet.vehicle.cost',
        inverse_name='parent_id',
        copy=True,
    )
