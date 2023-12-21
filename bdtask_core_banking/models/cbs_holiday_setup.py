from odoo import api, fields, models, _
from datetime import timedelta, datetime, date
from odoo.exceptions import ValidationError

class CBSHolidaySetup(models.Model):
    _name = 'cbs.holiday.setup'
    _order = "id"
    _description = "CBS Holiday Setup"
    
    # Fields definition for the CBS Calendar Setup model
    company_id = fields.Many2one('res.company', string="Organization")
    branch_id = fields.Many2one('cbs.branch', string="Branch")
    holiday = fields.Char(string='Holiday')
    holiday_reason = fields.Text("Holiday Reason")
    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    holiday_id = fields.One2many('holiday.setup.line', 'holiday_line_id', string="Holiday Line")
    is_visible = fields.Boolean(string="Is Visible")
    is_holiday = fields.Boolean(string="Is Holiday")
    
 # Create function for holidays 
    def custom_create(self):
        self.is_visible = True
        if self.from_date and self.to_date :
            holiday_line_obj = self.env['holiday.setup.line']
            for i in range((self.to_date - self.from_date).days + 1):
                current_date = self.from_date + timedelta(days=i)
                day_name = current_date.strftime('%A')
                holiday_setup_line_vals = {
                    'date': current_date,
                    'holiday_line_id': self.id,
                    'name': day_name,
                    'is_holiday': True,
                }
                holiday_line_obj.create(holiday_setup_line_vals)
        else:
            raise ValidationError(_("From Date and To Date must be selected!!"))
    
    def custom_apply(self):
        '''' This method is used to apply holiday in calendar setup '''
        self.is_holiday = True
        current_date = date.today()
        calender_obj = self.env['cbs.calendar.setup'].search([('branch_id', '=', self.branch_id.id), ('company_id', '=', self.company_id.id)])
        date_list = []
        for holiday in self.holiday_id:
            date_list.append(holiday.date)
        if calender_obj:
            for calender in calender_obj.calendar_setup_id:
                if calender.date >= current_date:
                    if calender.date in date_list:
                        calender.is_holiday = True
                    else:
                        calender.is_holiday = False
        else:
            raise ValidationError(_("Please Create Calendar First for this Branch!!"))

class HolidaySetupLine(models.Model):
    _name = 'holiday.setup.line'
    _order = "id"
    _description = "Holiday Setup Line"
    
    # Fields definition for the Holiday Setup Line model
    date = fields.Date(string='Date')
    name = fields.Char(string='Day Name',  compute='_compute_day', store=True)
    is_holiday = fields.Boolean(string="Is Holiday", store = True)
    holiday_line_id = fields.Many2one('cbs.holiday.setup', string="Holiday Setup Line")

    @api.depends('date')
    def _compute_day(self):
        for rec in self:
            if rec.date:
                rec.name = rec.date.strftime('%A')
            else:
                rec.name = False