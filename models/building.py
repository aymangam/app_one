# -*- coding: utf-8 -*-
from odoo import models, fields


class Building(models.Model):
    _name = 'building'
    _description = 'Building'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'code'

    no = fields.Integer()
    code = fields.Char()
    description = fields.Text()
    active = fields.Boolean(default=1)
