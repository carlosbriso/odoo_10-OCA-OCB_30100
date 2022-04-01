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
import datetime

from odoo import _
from odoo import models, api, fields
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT

_logger = logging.getLogger(__name__)

_types = {
    'days': lambda interval: datetime.timedelta(days=interval),
    'years': lambda interval: datetime.timedelta(weeks=interval*52),
    'hours': lambda interval: datetime.timedelta(hours=interval),
    'weeks': lambda interval: datetime.timedelta(weeks=interval),
    'months': lambda interval: datetime.timedelta(days=interval*30),
    'minutes': lambda interval: datetime.timedelta(minutes=interval),
}

class AutoVacuum(models.AbstractModel):
    
    _inherit = 'ir.autovacuum'
    
    @api.model
    def power_on(self, *args, **kwargs):
        super(AutoVacuum, self).power_on(*args, **kwargs)
        rules = self.env['muk_autovacuum.rules'].sudo().search([])
        for rule in rules:
            model = self.env[rule.model.model].sudo()
            timeout_ago = datetime.datetime.utcnow() - _types[rule.time_type](rule.time)
            domain = [('create_date', '<', timeout_ago.strftime(DEFAULT_SERVER_DATETIME_FORMAT))]
            if rule.protect_starred and "starred" in rule.model.field_id.mapped("name"):
                domain.append(('starred', '=', False))
            if rule.only_inactive and "active" in rule.model.field_id.mapped("name"):
                domain.append(('active', '=', False))
            records = model.search(domain)
            if rule.only_attachments:
                attachments = self.env['ir.attachment'].sudo().search([
                    ('res_model', '=', rule.model.model),
                    ('res_id', 'in', records.mapped('id'))])
                count = len(attachments)
                attachments.unlink()
                _logger.info(_("GC'd %s attachments from %s entries") % (count, rule.model.model))
            else:
                count = len(records)
                records.unlink()
                _logger.info(_("GC'd %s %s records") % (count, rule.model.model))
        return True