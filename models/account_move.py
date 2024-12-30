# -*- coding: utf-8 -*-

from odoo import models

class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_do_something(self):
        print(self, "inside action_do_something")
