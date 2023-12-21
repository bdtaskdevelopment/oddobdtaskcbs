from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import UserError, ValidationError

class CBSTransaction(models.Model):
    _name = 'cbs.transaction'
    _order = "id"
    _description = "CBS Transaction"
    
    # Fields definition for the CBS Transaction model
    name = fields.Char(string="Transaction Number", compute="_compute_transaction_number", store=True)
    cbs_bank_account_id = fields.Many2one('cbs.bank.account', string="Bank Account Number")
    partner_id = fields.Many2one('res.partner', string="Account Name")
    product_id = fields.Many2one('product.service', string="Product Name")
    product_type_id = fields.Many2one('product.type', string="Product Type")
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    remarks = fields.Text("Remarks")
    # transaction_date = fields.Date(string='Transaction Date', default=fields.Date.today)
    transaction_status = fields.Selection([
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw')
    ], string='Transaction Status')
    cbs_transaction_line_id = fields.One2many('cbs.transaction.line', 'transaction_id', string="CBS Transaction Line")
    journal_id = fields.Many2one('account.journal', string="Journal Items")
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env['res.company']._company_default_get('bdtask_core_banking'))
    calendar_setup_line_id = fields.Many2one('calendar.setup.line', string="Calendar Child", default=lambda self: self.env['calendar.setup.line'].search([('company_id', '=', self.env.user.company_id.id), ('branch_id', '=', self.env.user.branch_id.id), ('day_status', '=', 'open')]))
    transaction_date = fields.Date(related='calendar_setup_line_id.date', string='Transaction Date')
    is_visible = fields.Boolean(string="Is Visible")


    # Constraints to check if total debit and total credit in transaction lines are equal
    @api.constrains('cbs_transaction_line_id')
    def check_email_phone(self):
        total_debit = 0
        total_credit = 0
        for rec in self.cbs_transaction_line_id:
            total_debit += rec.debit_amount
            total_credit += rec.credit_amount
        if total_debit != total_credit:
            raise ValidationError(_('Total debit and total credit are not the same.'))

    # Onchange method to update fields based on the selected CBS Bank Account
    @api.onchange('cbs_bank_account_id')
    def onchange_cbs_bank_account_id(self):
        for rec in self:
            rec.name = rec.id
            rec.partner_id = rec.cbs_bank_account_id.partner_id
            rec.product_id = rec.cbs_bank_account_id.product_id
            rec.product_type_id = rec.cbs_bank_account_id.product_type_id
            rec.phone = rec.cbs_bank_account_id.phone
            rec.email = rec.cbs_bank_account_id.email

    # Computation method to generate the transaction number based on the transaction ID
    @api.depends('product_id')
    def _compute_transaction_number(self):
        for rec in self:
            rec.name = rec.id
    
    def create_journal_entries(self):
        ''' This method is used to create journal entries '''
        self.is_visible = True
        for rec in self:
            move_vals = {
                # 'name': rec.partner_id,
                'journal_id': rec.journal_id.id,
                'date': rec.transaction_date,
                'ref': rec.name,
            }
            line_ids = []
            for line in rec.cbs_transaction_line_id:
                debit = line.debit_amount
                credit = line.credit_amount

                if debit or credit: 
                    line_ids += [(0, 0, {
                        'name': rec.partner_id.name,
                        'debit': debit,
                        'credit': credit,
                        'account_id': line.account_id.id,
                        'partner_id': rec.partner_id.id
                    })]

            if line_ids:
                move_vals.update({'line_ids': line_ids})
                move = self.env['account.move'].create(move_vals)
                # move.action_post()
                # rec.write({'state': 'progress', 'move_id': move.id})

        return True