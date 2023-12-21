from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

class LinkAccount(models.Model):
    _name = 'link.account'
    _order = "name"
    _description = "Link Account"
    
    # Fields definition for the Link Account model
    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    chart_of_accounts_id = fields.Many2one('account.account', string="Chart of Accounts", company_dependent=True)
    
    # SQL constraints to enforce uniqueness on name field
    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Name already exists !')
    ]
