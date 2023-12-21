from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta

class CBSCalendarSetup(models.Model):
    _name = 'cbs.calendar.setup'
    _order = "id"
    _description = "CBS Calendar Setup"
    
    # Fields definition for the CBS Calendar Setup model
    company_id = fields.Many2one('res.company', string="Organization")
    branch_id = fields.Many2one('cbs.branch', string="Branch")
    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    add_more_date = fields.Date(string='Add More Date')
    calendar_setup_id = fields.One2many('calendar.setup.line','calendar_setup_line_id', string= "CBS Calendar Setup")

    # SQL constraint to ensure uniqueness of records for each branch
    _sql_constraints = [
        ('branch_uniq', 'unique (branch_id)', 'Record already exists for this branch.')
    ]

    # Method to create calendar setup lines based on the from_date and to_date range
    def custom_create_date(self):
        # Fetch weekend setup records for the current branch and company
        weekend_obj = self.env['cbs.weekend.setup'].search([('branch_id', '=', self.branch_id.id), ('company_id', '=', self.company_id.id)])
        holiday_obj = self.env['cbs.holiday.setup'].search([('branch_id', '=', self.branch_id.id), ('company_id', '=', self.company_id.id)])
        
        # Check if both from_date and to_date are provided
        if self.from_date and self.to_date:
            # Loop through the date range and create records for each date
            for i in range((self.to_date - self.from_date).days + 1):
                date = self.from_date + timedelta(days=i)
                day_name = date.strftime("%A")
                
                # Check if a record already exists for the current date and calendar setup
                existing_record = self.env['calendar.setup.line'].search([
                    ('date', '=', date),
                    ('calendar_setup_line_id', '=', self.id)
                ])
                
                # If no existing record, create a new record for the date and day_name
                if not existing_record:
                    self.env['calendar.setup.line'].create({
                        'date': date,
                        'day_name': day_name,
                        'calendar_setup_line_id': self.id
                    })
                    
                    # If weekend setup exists, call the custom_apply method
                    if weekend_obj:
                        func_call = weekend_obj.custom_apply()
                    if holiday_obj :
                        for i in holiday_obj:
                            func_call2 = holiday_obj.custom_apply()
        else:
            raise UserError(_("Please Select From Date and To Date"))


class CalendarSetupLine(models.Model):
    _name = 'calendar.setup.line'
    _order = "id"
    _description = "Calendar Setup Line"

    # Fields for Calendar Setup Line model
    date = fields.Date(string= "Date")
    day_name = fields.Char(string="Day Name")
    is_weekend = fields.Boolean(string="Weekend")
    is_holiday = fields.Boolean(string="Holiday")
    day_status = fields.Selection([
        ('open', 'Open'),
        ('close', 'Close')
    ], string='Day Status')
    
    calendar_setup_line_id = fields.Many2one('cbs.calendar.setup', string='Calendar Setup Line')
    company_id = fields.Many2one(related='calendar_setup_line_id.company_id', string="Organization")
    branch_id = fields.Many2one(related='calendar_setup_line_id.branch_id', string="Branch")
