from odoo import api, fields, models, _

class ProductService(models.Model):
    _name = 'product.service'
    _order = "id"
    _description = "Product Service"
    
    # Fields definition for the Product Service model
    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    link_account_id = fields.Many2one('link.account', string="Link Account")
    product_type_id = fields.Many2one('product.type', string="Product Type")

    # SQL constraints to enforce uniqueness on name and code fields
    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The product name must be unique !'),
        ('code_uniq', 'unique (code)', 'The product code must be unique !')
    ]
