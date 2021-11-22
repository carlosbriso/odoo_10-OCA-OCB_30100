# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import Warning
from datetime import datetime, date, timedelta
import logging

_logger = logging.getLogger(__name__)


###############################################################################
#   project.task                                                              #
###############################################################################

class ProjectTask(models.Model):
    _inherit = 'project.task'

    # ----------------------- AUXILIARY FIELD METHODS -------------------------

    @api.multi
    @api.depends('date_start', 'date_deadline', 'set_close')
    def _compute_tstate(self):
        for record in self:
            today = fields.Date.context_today(self)
            date_start = datetime.strptime(
                record.date_start, '%Y-%m-%d %H:%M:%S'
            ).date().strftime('%Y-%m-%d')
            if not record.set_close and today < date_start:
                record.tstate = 'open'
            elif not record.set_close and today >= date_start and \
                    today <= record.date_deadline:
                record.tstate = 'process'
            elif not record.set_close and today > record.date_deadline:
                record.tstate = 'out'
            elif record.set_close:
                record.tstate = 'closed'
            else:
                record.tstate = 'closed'

    # --------------------------- ENTITY  FIELDS ------------------------------

    code = fields.Char(
        string='Sequence',
        readonly=True,
    )

    set_close = fields.Boolean(
        string='Set close',
        default=False,
    )

    tstate = fields.Selection(
        selection=[
            ('open', 'Open'),
            ('process', 'In progress'),
            ('out', 'Out of time'),
            ('closed', 'Closed'),
        ],
        string='Status',
        compute='_compute_tstate',
        store=True,
    )

    # ---------------------------- NEW METHODS --------------------------------

    @api.model
    def cron_sync_task_state(self):
        tasks = self.env['project.task'].search([])
        for task in tasks:
            task._compute_tstate()

    @api.multi
    def task_set_open(self):
        for task in self:
            if task.create_uid.id != self.env.uid:
                raise Warning(
                    _('You cannot set this task to open.')
                )
            else:
                task.write({
                    'date_end': False,
                    'set_close': False
                })
                self._compute_tstate()
        return True

    @api.multi
    def task_set_closed(self):
        for task in self:
            if task.create_uid.id != self.env.uid:
                raise Warning(
                    _('You cannot set this task to closed.')
                )
            else:
                today = fields.datetime.now()
                task.write({
                    'tstate': 'closed',
                    'date_end': today,
                    'set_close': True
                })
        return True

    @api.multi
    def action_send_mail_assigned_task(self, user_id):
        template = self.env.ref('ener_project_ext.assigned_task')
        if user_id:
            template_values = {
                'email_to': user_id.partner_id.email,
                'email_cc': False,
                'auto_delete': True,
                'partner_to': False,
                'scheduled_date': False,
            }
            template.write(template_values)
            for record in self:
                if record.user_id:
                    messages = self.env['mail.message']
                    new_message = messages.create({
                        'subject': 'Assigned task',
                        'body': _('''<p>Assigned task "%s"</p>
<p>%s</p>''') % (
                            record.name,
                            record.description,
                        ),
                        'message_type': 'comment',
                        'subtype_id': self.env.ref('mail.mt_comment').id,
                        'author_id': self.env.ref('base.partner_root').id,
                        'partner_ids': [(6, 0, [
                            record.user_id.partner_id.id
                        ])],
                        'date': fields.datetime.now(),
                        'model': 'project.task',
                        'res_id': record.id,
                    })
                    if new_message:
                        notifications = self.env['mail.notification']
                        notifications.create({
                            'mail_message_id': new_message.id,
                            'res_partner_id': record.user_id.partner_id.id,
                            'email_status': False,
                        })
                    if record.user_id.email:
                        template.with_context(
                            lang=record.user_id.lang,
                            user_name=record.user_id.name,
                            user_email=record.user_id.partner_id.email,
                            task_id=record.id,
                            task_name=record.name,
                            project_name=record.project_id.name,
                        ).send_mail(
                            record.id,
                            force_send=True,
                            raise_exception=True
                        )
                        _logger.info(
                            "Assigned task for user <%s>, <%s>",
                            record.user_id.name,
                            record.user_id.login
                        )

    # ------------------------ METHODS OVERWRITTEN ----------------------------

    @api.model
    def create(self, values):
        values.update({
            'code': self.env['ir.sequence'].next_by_code(
                'project.task.code') or '',
        })
        result = super(ProjectTask, self).create(values)
        if 'user_id' in values:
            result.action_send_mail_assigned_task(result.user_id)
        if 'active' in values:
            if not values['active']:
                pass
        return result

    @api.multi
    def write(self, values):
        result = super(ProjectTask, self).write(values)
        if 'user_id' in values:
            for record in self:
                record.action_send_mail_assigned_task(record.user_id)
        return result
