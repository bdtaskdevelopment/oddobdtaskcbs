from odoo import api, fields, models, _
from datetime import date, datetime, timedelta
from odoo.exceptions import ValidationError

class CBSWeekendSetup(models.Model):
    _name = 'cbs.weekend.setup'
    _order = "id"
    _description = "CBS Weekend Setup"
    
    # Fields definition for the CBS Weekend Setup model
    company_id = fields.Many2one('res.company', string="Organization")
    branch_id = fields.Many2one('cbs.branch', string="Branch")
    cbs_week_id = fields.One2many('cbs.week', 'cbs_weekend_setup_ids')
    is_visible = fields.Boolean(string="Is Visible")

    _sql_constraints = [
        ('branch_uniq', 'unique (branch_id)', 'Record already exists for this branch.')
    ]

    # Method to create all the days in a week
    def custom_create_day(self):
        self.is_visible = True
        days = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        
        for day in days:
            existing_record = self.env['cbs.week'].search([
                ('name', '=', day),
                ('cbs_weekend_setup_ids', '=', self.id)
            ])
            if not existing_record:
                self.env['cbs.week'].create({
                    'name': day,
                    'cbs_weekend_setup_ids': self.id
                })
    
    # This method is used to apply weekend in calendar setup 
    def custom_apply(self):
        '''' This method is used to apply weekend in calendar setup '''
        weekends = []
        current_date = date.today()
        calendar_setup_obj = self.env['cbs.calendar.setup']
        for rec in self.cbs_week_id:
            if rec.is_weekend:
                weekends.append(rec.name)

        calendar_setup = calendar_setup_obj.search([('branch_id', '=', self.branch_id.id), ('company_id', '=', self.company_id.id)])
        if calendar_setup:
            for rec in calendar_setup.calendar_setup_id:
                if rec.date >= current_date:
                    if rec.day_name in weekends:
                        rec.write({'is_weekend': True})
                    else:
                        rec.write({'is_weekend': False})


class CBSWeek(models.Model):
    _name = 'cbs.week'
    _order = "id"
    _description = "CBS Week"
    
    # Fields definition for the CBS Week model
    name = fields.Char(string='Days')
    cbs_weekend_setup_ids = fields.Many2one('cbs.weekend.setup')
    is_weekend = fields.Boolean(string="Is Weekend")
