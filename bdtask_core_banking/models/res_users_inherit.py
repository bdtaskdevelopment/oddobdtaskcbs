from odoo import api, fields, models, _


class ResUser(models.Model):
    _inherit = 'res.users'

    # Branch Ids and Branch id releted with CBS Branch Model
    branch_ids = fields.Many2many('cbs.branch', string="Allowed Branches")
    branch_id = fields.Many2one('cbs.branch', string="Default Branch")