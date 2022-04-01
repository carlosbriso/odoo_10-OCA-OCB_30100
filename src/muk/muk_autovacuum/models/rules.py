# -*- coding: utf-8 -*-

###################################################################################
# 
#    Copyright (C) 2018 MuK IT GmbH
#
#    Odoo Proprietary License v1.0
#    
#    This software and associated files (the "Software") may only be used 
#    (executed, modified, executed after modifications) if you have
#    purchased a valid license from the authors, typically via Odoo Apps,
#    or if you have received a written agreement from the authors of the
#    Software (see the COPYRIGHT file).
#    
#    You may develop Odoo modules that use the Software as a library 
#    (typically by depending on it, importing it and using its resources),
#    but without copying any source code or material from the Software.
#    You may distribute those modules under the license of your choice,
#    provided that this license is compatible with the terms of the Odoo
#    Proprietary License (For example: LGPL, MIT, or proprietary licenses
#    similar to this one).
#    
#    It is forbidden to publish, distribute, sublicense, or sell copies of
#    the Software or modified copies of the Software.
#    
#    The above copyright notice and this permission notice must be included
#    in all copies or substantial portions of the Software.
#    
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#    OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#    DEALINGS IN THE SOFTWARE.
#
###################################################################################

import logging

from odoo import _
from odoo import models, api, fields

_logger = logging.getLogger(__name__)

class AutoVacuumRules(models.Model):
    
    _name = 'muk_autovacuum.rules'
    _description = "Auto Vacuum Rules"
    
    #----------------------------------------------------------
    # Defaults
    #----------------------------------------------------------

    def _default_sequence(self):
        record = self.sudo().search([], order='sequence desc', limit=1)
        if record:
            return record.sequence + 1
        else:
            return 1

    #----------------------------------------------------------
    # Database
    #----------------------------------------------------------

    sequence = fields.Integer(
        string='Sequence',
        default=_default_sequence,
        required=True)
    
    model = fields.Many2one(
        'ir.model',
        string="Model",
        required=True,
        ondelete='cascade',
        help="Model on which the rule is applied.")
    
    time_type = fields.Selection([
        ('minutes', 'Minutes'),
        ('hours', 'Hours'),
        ('days', 'Days'),
        ('weeks', 'Weeks'),
        ('months', 'Months'),
        ('years', 'Years')],
        string='Time Unit', 
        default='months',
        required=True)
    
    time = fields.Integer(
        string='Time', 
        default=1, 
        help="Delete older data than x.")
    
    protect_starred = fields.Boolean(
        string='Protect Starred', 
        default=True, 
        help="Do not delete starred records.")
    
    only_inactive = fields.Boolean(
        string='Only Archived', 
        default=False, 
        help="Only delete archived records.")
    
    only_attachments = fields.Boolean(
        string='Only Attachments', 
        default=False, 
        help="Only delete record attachments.")