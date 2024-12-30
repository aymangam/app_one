# -*- coding: utf-8 -*-

from odoo import models, fields



class Tag(models.Model):
    _name = 'tag'


    name = fields.Char(required=1, default='tag', size=10)

