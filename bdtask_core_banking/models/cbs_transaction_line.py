from odoo import api, fields, models, _

class CBSTransactionLine(models.Model):
    _name = 'cbs.transaction.line'
    _order = "id"
    _description = "CBS Transaction Line"
    
    # Fields definition for the CBS Transaction Line model
    transaction_id = fields.Many2one('cbs.transaction', string="Transaction ID")
    cbs_bank_account_id = fields.Many2one('cbs.bank.account', string="Bank Account Number")
    partner_id = fields.Many2one('res.partner', string="Account Name")
    product_id = fields.Many2one('product.service', string="Product Name")
    product_type_id = fields.Many2one('product.type', string="Product Type")
    link_account_id = fields.Many2one('link.account', string="Internal Account")
    account_id = fields.Many2one('account.account', string="Chart of Accounts", company_dependent=True)
    debit_amount = fields.Float(string='Debit')
    credit_amount = fields.Float(string='Credit')
    transaction_status = fields.Selection(related='transaction_id.transaction_status', string="Transaction Status")
    transaction_date = fields.Date(related='transaction_id.transaction_date', string='Transaction Date')
    
    # Onchange method to update fields based on the selected transaction and product
    @api.onchange('transaction_id', 'product_id')
    def onchange_partner_id(self):
        for rec in self:
            rec.cbs_bank_account_id = rec.transaction_id.cbs_bank_account_id
            rec.link_account_id = rec.product_id.link_account_id
            rec.account_id = rec.product_id.link_account_id.chart_of_accounts_id
