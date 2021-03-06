# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class Goal(models.Model):

    _name = "qms.goal"

    name = fields.Char(
        required=True
    )

    description = fields.Html()

    cancel_date = fields.Date(
        readonly=True
    )

    date_open = fields.Date()

    date_close = fields.Date()

    approved = fields.Boolean()

    _state_ = [
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled')
    ]

    responsible_id = fields.Many2one(
        comodel_name='qms.interested_party',
        required=True
    )

    process_ids = fields.Many2many(
        comodel_name='qms.process',
        required=True
    )

    resource_ids = fields.Many2many(
        comodel_name='qms.resource'
    )

    measurement_ids = fields.One2many(
        comodel_name='qms.goal.measurement',
        inverse_name='goal_id'
    )

    action_ids = fields.One2many(
        comodel_name='qms.action',
        inverse_name='goal_id',
        ondelete='cascade'
    )

    state = fields.Selection(
        selection=_state_,
        default='draft',
        required=True
    )

    review_ids = fields.One2many(
        comodel_name='qms.review',
        inverse_name='goal_id'
    )

    last_measurement_date = fields.Date(compute='_compute_last_measurement_date')

    last_measurement_result = fields.Char(compute='_compute_last_measurement_result')

    last_review_date = fields.Date(compute='_compute_last_review_date')

    @api.multi
    @api.depends('measurement_ids')
    def _compute_last_measurement_date(self):
        for goal in self:
            domain = [
                ('goal_id', '=', goal.id),
                #('modify_concession', '=', True)
            ]
            related_measurement = goal.env['qms.goal.measurement'].search(domain)
            last_measurement = related_measurement.sorted(
                key=lambda r: r.measurement_date,
                reverse=True)
            goal.last_measurement_date = last_measurement[0].measurement_date

    @api.multi
    @api.depends('measurement_ids')
    def _compute_last_measurement_result(self):
        for goal in self:
            domain = [
                ('goal_id', '=', goal.id),
                #('modify_concession', '=', True)
            ]
            related_measurement = goal.env['qms.goal.measurement'].search(domain)
            last_measurement = related_measurement.sorted(
                key=lambda r: r.measurement_date,
                reverse=True)
            goal.last_measurement_result = last_measurement[0].result

    @api.multi
    @api.depends('review_ids')
    def _compute_last_review_date(self):
        for goal in self:
            domain = [
                ('goal_id', '=', goal.id),
                #('modify_concession', '=', True)
            ]
            related_reviews = goal.env['qms.review'].search(domain)
            last_review = related_reviews.sorted(
                key=lambda r: r.date,
                reverse=True)
            goal.last_review_date = last_review[0].date

    @api.one
    def toggle_approved(self):
        self.approved = not self.approved
