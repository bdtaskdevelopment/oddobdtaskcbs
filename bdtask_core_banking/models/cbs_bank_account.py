from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class CBSBankAccount(models.Model):
    _name = 'cbs.bank.account'
    _order = "id"
    _description = "CBS Bank Account"
    
    # Fields definition for the CBS Bank Account model
    name = fields.Char(string="Account Number", compute="_compute_account_number", store=True)
    partner_id = fields.Many2one('res.partner', string="Account Name")
    address = fields.Text("Address")
    product_id = fields.Many2one('product.service', string="Product Name")
    product_type_id = fields.Many2one('product.type', string="Product Type")
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')

    # Onchange method to update email and phone based on partner selection
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for rec in self:
            rec.email = self.partner_id.email
            rec.phone = self.partner_id.phone

    # Constraints to check if email and phone are set for the partner
    @api.constrains('partner_id')
    def check_email_phone(self):
        '''This method will check email and phone are set or not'''
        for rec in self:
            if not rec.email:
                raise ValidationError(_('Please set an email for this partner.'))
            if not rec.phone:
                raise ValidationError(_('Please set a phone number for this partner.'))
    
    # Computation method to generate the account number based on product ID, and current record ID
    @api.depends('product_id', 'partner_id')
    def _compute_account_number(self):
        product_prefix = ''
        account_prefix = ''
        for rec in self:
            if rec.product_id.code:
                product_prefix += rec.product_id.code
            current_id = rec.id
            if len(str(current_id)) < 6:
                diff = 6 - len(str(current_id))
                zeroes = "0" * diff
                account_prefix += zeroes + str(current_id)
            else:
                account_prefix = str(current_id)
            rec.name = product_prefix + "-" + account_prefix
            if not rec.product_id.id or not rec.id:
                rec.name = None
            break
