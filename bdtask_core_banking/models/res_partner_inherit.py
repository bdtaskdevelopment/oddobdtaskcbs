from odoo import api, fields, models, _


class ResPartner(models.Model):
    # Inherited res.partner model
    _inherit = 'res.partner'

    # SQL constraints to enforce uniqueness on phone and email fields
    _sql_constraints = [
        ('phone_uniq', 'unique (phone)', 'The phone must be unique !'),
        ('email_uniq', 'unique (email)', 'The email must be unique !')
    ]