
from openerp import models, fields, api
from openerp.tools.translate import _

class IrModel(models.Model):
    _inherit = 'ir.model'

    @api.multi
    def show_tree_view(self):
        self.ensure_one()
        return {
            'name': _('Export Data (%s)' % self.model),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': self.model,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'context': self.env.context,
        }