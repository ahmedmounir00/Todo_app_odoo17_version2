from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Todo(models.Model):
    _name = "todo.management"
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = "New Task"
    _rec_name = "task_name"

    task_name = fields.Char(string="Task Name" , required=True , tracking=True)
    description = fields.Char(string="Description" , tracking=True)
    due_date = fields.Date(string="Due Date" , required=True , tracking=True)
    total_time = fields.Float(string="Total Time", compute='compute_total_time', store=True)
    estimated_time = fields.Integer(string="Estimated Time (hrs)", required=True, tracking=True)
    active = fields.Boolean(default=True)
    status = fields.Selection([
        ('new','New'),
        ('in progress','In Progress'),
        ('completed','Completed'),
        ('close','Close'),
    ],string='Status' , default="new" , tracking=True)
    assign_to = fields.Many2one('res.partner' , string="Assign To")
    line_ids = fields.One2many("todo.lines" , "task_id")
    is_late = fields.Boolean()

    _sql_constraints = [
        ('unique_name', 'unique(task_name)', 'This name is exist.')
    ]
    # to calculate Time in every line and display result in the total_time in the report
    def compute_total_time(self):
        for rec in self :
            rec.total_time = sum(line.time for line in rec.line_ids)

    # to check if total time ( time in every line ) is greater than estimated_time
    @api.constrains('line_ids', 'estimated_time')
    def time_validation (self):
        for rec in self:
            total_time = sum(line.time for line in rec.line_ids)
            if total_time > rec.estimated_time:
                raise ValidationError(
                    f"The Total Time {total_time} is greater than the Estimated Time {rec.estimated_time}"
                )
    # add logic to server action
    def action_close_todo (self):
        for rec in self:
            rec.status = 'close'

    # add logic to cron job action
    def check_due_date_if_late (self):
        tasks_ids = self.search([])
        for rec in tasks_ids:
            if rec.due_date and rec.due_date < fields.date.today() and ( rec.status == 'new' or rec.status == 'in progress') :
                rec.is_late = True
            else :
                rec.is_late = False

class TodoLines(models.Model):
    _name ="todo.lines"
    _inherit = ['mail.thread' , 'mail.activity.mixin']

    num = fields.Integer(string="ID" , required=True , tracking=True)
    date = fields.Date(string="Date" , required=True , tracking=True)
    description = fields.Char(string = "Description" , tracking=True)
    time = fields.Float(string="Time (hrs)" , required=True , tracking=True)
    task_id = fields.Many2one("todo.management", string="Task")



