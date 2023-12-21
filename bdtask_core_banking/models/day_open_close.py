from odoo import api, fields, models, _
from datetime import timedelta, datetime, date
from odoo.exceptions import ValidationError

class DayOpenClose(models.Model):
    _name = 'day.open.close'
    _order = "id"
    _description = "Day Open Close"
    
    # Fields definition for the Day Open Close model
    date = fields.Date(string='Date')
    company_id = fields.Many2one('res.company', string="Organization")
    branch_id = fields.Many2one('cbs.branch', string="Branch")
    is_visible = fields.Boolean(string="Is Visible")

    # Method to open a date
    def custom_create_date(self):
        # Set visibility to True
        self.is_visible = True
        
        # Fetch calendar setup for the current branch and company
        calendar_setup_obj = self.env['cbs.calendar.setup'].search([('branch_id', '=', self.branch_id.id), ('company_id', '=', self.company_id.id)])
        
        # Fetch calendar setup lines excluding weekends
        calendar_setup_line_obj = self.env['calendar.setup.line'].search([('calendar_setup_line_id', '=', calendar_setup_obj.id), ('is_weekend', '=', False)])
        
        # Filter calendar setup lines for non-holiday and no day status
        expected_obj1 = calendar_setup_line_obj.filtered(lambda x: x.is_holiday == False)
        expected_obj2 = expected_obj1.filtered(lambda x: not x.day_status)
        
        # Check if no matching records found
        if not expected_obj2:
            # If the date is set, raise a validation error
            if self.date:
                raise ValidationError(_('Limit reached for this year.'))
            
            # Set the day status to 'open' for the first matching record
            expected_obj1[0].day_status = 'open'
            self.date = expected_obj1[0].date 
        else:
            # Set the day status to 'open' for the first matching record
            expected_obj2[0].day_status = 'open'
            self.date = expected_obj2[0].date 

    # Method to close a date
    def custom_close_date(self):
        # Set visibility to False
        self.is_visible = False
        
        # Define search domain to find open dates for the current branch and company
        domain = [
            ('branch_id', '=', self.branch_id.id),
            ('company_id', '=', self.company_id.id),
            ('day_status', '=', 'open'),
        ]
        
        # Search for open dates
        calendar_setup_line = self.env['calendar.setup.line'].search(domain)
        
        # Set day status to 'close' for each open date
        for rec in calendar_setup_line:
            rec.day_status = 'close'
