from odoo import api, fields, models, _

class ProductType(models.Model):
    _name = 'product.type'
    _order = "name"
    _description = "Product Type"

    # Fields definition for the Product Type model
    name = fields.Char(string="Product Type")
    product_code = fields.Char(string="Product Code")
    is_bank_account_genarate = fields.Boolean(string="Is Bank Account Genarate")