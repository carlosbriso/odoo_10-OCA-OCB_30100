# -*- coding: utf-8 -*-
###############################################################################
#
#    Odoo, Open Source Management Solution
#
#    Copyright (c) All rights reserved:
#        (c) 2019 Anubía Soluciones en la Nube, S.L.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses
#
###############################################################################
{
    'name': 'Custom Reports for Enermol',
    'summary': 'Custom Reports for Enermol',
    'version': '10.0.1.0',
    'description': """Description in HTML file.""",
    'author': 'Anubía Soluciones en la Nube, S.L.',
    'website': "http://www.anubia.es",
    'maintainer': 'Anubía Soluciones en la Nube, S.L.',
    'contributors': [
        'Jesús Cacabelos Reyes <jcr@anubia.es>'
    ],
    'license': 'AGPL-3',
    'category': 'Purchase',
    'depends': [
        'anb_custom_reports',
    ],
    'external_dependencies': {},
    'data': [
        'report/account_invoice.xml',
        'report/external_layout.xml'
    ],
    'demo': [],
    'js': [],
    'css': [],
    'qweb': [],
    'images': [],
    'test': [],
    'installable': True,
}
