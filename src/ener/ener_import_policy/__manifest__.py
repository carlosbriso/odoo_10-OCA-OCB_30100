# -*- coding: utf-8 -*-
###############################################################################
#
#    Odoo, Open Source Management Solution
#
#    Copyright (c) All rights reserved:
#        (c) 2015
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
    'name': 'Importación de Pólizas para Enermol',
    'summary': 'Importar pólizas para Enermol',
    'version': '10.0.1.0',
    'description': """Description in HTML file.""",
    'author': 'Anubia, Soluciones en la Nube, SL',
    'website': "http://www.anubia.es",
    'maintainer': 'Anubia, soluciones en la nube, SL',
    'contributors': [
        'Pablo González González <pgg@anubia.es>'
    ],
    'license': 'AGPL-3',
    'category': 'Project',
    'depends': [
        'project',
    ],
    'external_dependencies': {},
    'data': [
        'security/request_security.xml',
        'views/policy.xml',
        'views/project.xml',
        'wizard/import_policy.xml',
    ],
    'demo': [],
    'js': [],
    'css': [],
    'qweb': [],
    'images': [],
    'test': [],
    'installable': True,
}
