from odoo import api, fields, models, _


class CBSBranch(models.Model):
    _name = 'cbs.branch'
    _order = "name"
    _description = "Branch"

    # Fields definition for the Branch model
    company_id = fields.Many2one('res.company', string="Organization")
    name = fields.Char(string="Branch Name")
    code = fields.Char(string="Branch Code")
    date = fields.Date(string="Software Starting Date")
    office_type = fields.Selection ([ 
        ('head', 'Head Office'),
        ('child', 'Child Office'),

    ])
    b_short_name = fields.Char(string="Branch Short Name")
    is_active = fields.Boolean(string="Is Active", store = True)
   