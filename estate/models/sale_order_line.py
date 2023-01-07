from odoo import fields, models, Command

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    training_date_start = fields.Datetime(string="Training starting date")
    training_date_end = fields.Datetime(string="Training ending date")
    employee_id = fields.Many2one('hr.employee', string="Employee")