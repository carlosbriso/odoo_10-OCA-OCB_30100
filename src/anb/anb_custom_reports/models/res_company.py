# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016-CURRENTLY Anubía SOluciones en la Nube, S.L.
#                  (<http://www.anubies.es>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api
from odoo.exceptions import Warning
from odoo import _
import re
import logging
_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = 'res.company'

    logo_height = fields.Integer(
        string='Logo height (px)',
        required=True,
        default=100,
        help='This is the height of the header logo in the reports. '
             'The range should be [50, 200]'
    )

    @api.multi
    def write(self, values):
        """ El problema de esta funcion es que si hay varias
            empresas cogería solo los cambios que se hagan en la ultima
            Los valores por defecto son:
                max-height: 100px;
                padding-top: 30px;
        """
        logo_height = values.get('logo_height', False)
        if logo_height:
            if logo_height < 50 or logo_height > 200:
                raise Warning(_('Logo height out of range (50, 200)'))

            layout_header = self.env['ir.ui.view'].search(
                [('name', '=', 'custom_external_layout_header')]
            )
            if layout_header:
                template = layout_header[0].arch
                replaced = re.sub(
                    'height: [0-9]+px;',
                    'height: %spx;' % str(logo_height),
                    template
                )
                layout_header[0].write({'arch': replaced})

            page_style = self.env['ir.ui.view'].search(
                [('name', '=', 'report_vat_view_style')]
            )
            if page_style:
                template = page_style[0].arch
                replaced = re.sub(
                    'padding-top: [0-9]+px;',
                    'padding-top: %spx;' % str(logo_height - 45),
                    template
                )
                page_style[0].write({'arch': replaced})

            if not page_style or not layout_header:
                raise Warning(_(
                    'Report templates not found: '
                    'report_vat_view_style or custom_external_layout_header'
                ))

        return super(ResCompany, self).write(values)
