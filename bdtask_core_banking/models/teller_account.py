from odoo import api, fields, models, _


class TellerAccount(models.Model):
    _name = 'teller.account'
    _order = "name"
    _description = "Teller Account"

    # Fields definition for the Teller Account model
    branch_id = fields.Many2one('cbs.branch', string="Branch")
    name = fields.Char(string="Teller Account Code")
    link_account_id = fields.Many2one('link.account', string="Internal Account")
    is_head_cashier = fields.Boolean(string="Is Head Cashier", store = True)
    is_vault = fields.Boolean(string="Is Vault", store = True)
    is_active = fields.Boolean(string="Is Active", store = True)
    user_id = fields.Many2one('res.users', string="User")
   