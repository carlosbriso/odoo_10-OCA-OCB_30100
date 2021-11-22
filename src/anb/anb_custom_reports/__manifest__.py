# -*- coding: utf-8 -*-
##############################################################################
#
#    Mandate module for openERP
#    Copyright (C) 2016 Anubía, soluciones en la nube,SL (http://www.anubia.es)
#    @author: Jesús Cacabelos <jcr@anubia.es>,
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

{
    'name': 'Custom Reports',
    'author': 'Anubia, soluciones en la nube SL <anubia@anubia.es>',
    'version': '8.0.1.0',
    'summary': 'It adds several options on: '
               'Company > Report Configuration',
    'category': 'Tools',
    'complexity': 'easy',
    'contributors': [
        'Jesús Cacabelos <jcr@anubia.es>',
        'Juan Formoso <jfv@anubia.es>',
    ],
    'website': 'www.anubia.es',
    'data': [
        'report/external_layout_header.xml',
        'views/res_company.xml',
    ],
    'depends': [
        'base',
        'account',
        'report',
        'sale',
        'stock',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
