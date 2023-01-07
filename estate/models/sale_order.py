from odoo import api, models, fields
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def create_calendar_events(self):
        for orderLine in self.order_line:
            if orderLine.training_date_start and orderLine.training_date_end and orderLine.employee_id:
                #checks for an existing event to fix a duplicate issue due to create_calendar_events() being called twice, and I dread removing either of them
                existing_event = self.env['calendar.event'].search([
                    ('name', '=', orderLine.name),
                    ('start', '=', orderLine.training_date_start),
                    ('stop', '=', orderLine.training_date_end),
                    ('partner_ids', '=', self.partner_id.id),
                    ('employee_ids', '=', orderLine.employee_id.id)
                ])
                # if an event with the same attributes does not exist, create a new event
                if not existing_event:
                    #name: description set in the quotation order line
                    #start: starting training date
                    #stop: ending training date
                    #partner_ids: partners
                    #employee_ids: employees selected in the "Employee" field in the order line
                    vals = {
                        'name': orderLine.name,
                        'start': orderLine.training_date_start,
                        'stop': orderLine.training_date_end,
                        #6 indicates that the operation is 'replace' (the available opeorations are add, delete, remove and replace)
                        #4 should also work instead of 6, but for reasons unknown it breaks the code so 6 is being used instead
                        #0 means that it is done for every ID in the M2M field, if a specific ID is desired then it should replace the 0
                        'partner_ids': [(6, 0, [self.partner_id.id])],
                        'employee_ids': [(6, 0, [orderLine.employee_id.id])],
                    }
                    self.env['calendar.event'].create(vals)

    #overrides the create method
    @api.model
    def create(self, vals):
        sale_order = super(SaleOrder, self).create(vals)
        sale_order.create_calendar_events()
        return sale_order

    #overrides the write method
    @api.model
    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        self.create_calendar_events()
        return res

    #necessary to get the employee id
class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    employee_ids = fields.Many2many('hr.employee', string='Employees')