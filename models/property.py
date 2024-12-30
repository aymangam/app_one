# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import requests

class Property(models.Model):
    _name = 'property'
    _description = 'Property'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ref = fields.Char(default='New', readonly=1)
    name = fields.Char(required=1, default='New', size=50, translate=True)
    description = fields.Text(tracking=1)
    postcode = fields.Char(required=1)
    date_availability = fields.Date(tracking=1)
    expected_selling_date = fields.Date(tracking=1)
    is_late = fields.Boolean()
    expected_Price = fields.Float(digits=(0, 2))
    selling_Price = fields.Float()
    diff = fields.Float(compute='_compute_diff', store=1, readonly=0)
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean(groups="app_one.property_manager_group")
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], default='north')
    owner_id = fields.Many2one('owner')
    tag_ids = fields.Many2many('tag')
    owner_adderss = fields.Char(related='owner_id.address', readonly=0, store=1)
    owner_phone = fields.Char(related='owner_id.phone', readonly=0, store=1)
    active = fields.Boolean(default=1)
    create_time = fields.Datetime(default=fields.Datetime.now())
    next_time = fields.Datetime(compute='_compute_next_time')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('closed', 'Closed'),
    ], default='draft')

    _sql_constraints = [
        ('unique_name', 'unique("name")', 'This name is exist!')
    ]

    line_ids = fields.One2many('property.line', 'property_id')

    @api.depends('create_time')
    def _compute_next_time(self):
        for rec in self:
            if rec.create_time:
                rec.next_time = rec.create_time + timedelta(hours=6)
            else:
                rec.next_time = False

    @api.depends('expected_Price', 'selling_Price')
    def _compute_diff(self):
        for rec in self:
            rec.diff = rec.expected_Price - rec.selling_Price


    @api.onchange('expected_Price')
    def _onchange_expected_Price(self):
        for rec in self:
            if rec.expected_Price < 0:
                return {
                    'warning': {'title': 'warning', 'message': 'negative value.', 'type': 'notification'}
                }

    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms == 0:
                raise ValidationError('Please add valid number of bedrooms!')

    def action_draft(self):
        for rec in self:
            rec.create_history_recoed(rec.state, 'draft')
            rec.state = 'draft'
            # rec.write({
            #     'state': 'draft'
            # })

    def action_pending(self):
        for rec in self:
            rec.create_history_recoed(rec.state, 'pending')
            rec.write({
                'state': 'pending'
            })

    def action_sold(self):
        for rec in self:
            rec.create_history_recoed(rec.state, 'sold')
            rec.state = 'sold'

    def action_closed(self):
        for rec in self:
            rec.create_history_recoed(rec.state, 'closed')
            # rec.create_history_recoed(rec.state, 'closed', '')
            rec.state = 'closed'

    def check_expected_selling_date(self):
        property_ids = self.search([])
        for rec in property_ids:
            if rec.expected_selling_date and rec.expected_selling_date < fields.Date.today():
                rec.is_late = True


    @api.model_create_multi
    def create(self, vals):
        res = super(Property, self).create(vals)
        # res = super().create(self, vals)
        print('inside create method')
        return res

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        res = super(Property, self)._search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
        # print('inside search method(read)')
        return res

    # with out @api
    def write(self, vals):
        res = super(Property, self).write(vals)
        # if replace write=> crate = duplicate
        print('inside write method(update)')
        return res

    # with out @api
    def unlink(self):
        res = super(Property, self).unlink()
        print('inside unlink method(delete)')
        return res

    def action(self):
        print(self.env['property'].search(['!', ('name', '=', 'Property 1'), ('postcode', '!=', '13')]))

    @api.model
    def create(self, vals):
        res = super(Property, self).create(vals)
        if res.ref == 'New':
            res.ref = self.env['ir.sequence'].next_by_code('property_seq')
        return res

    def create_history_recoed(self, old_state, new_state, reason=""):
        for rec in self:
            rec.env['property.history'].create({
                'user_id': rec.env.uid,
                'property_id': rec.id,
                'old_state': old_state,
                'new_state': new_state,
                'reason': reason or "",
                'line_ids': [(0, 0, {'description': line.description, 'area': line.area}) for line in rec.line_ids],
            })

    def action_open_change_state_wizard(self):
        action = self.env["ir.actions.actions"]._for_xml_id("app_one.change_state_wizard_action")
        action['context'] = {'default_property_id': self.id}
        return action

    def action_open_related_owner(self):
        action = self.env["ir.actions.actions"]._for_xml_id("app_one.owner_action")
        view_id = self.env.ref("app_one.owner_form_view").id
        action['res_id'] =  self.owner_id.id
        action['views'] =  [[view_id, 'form']]
        return action

    def get_properties(self):
        payload = dict()
        try:
            response = requests.get('http://127.0.0.1:8069/v1/properties', data=payload)
            if response.status_code == 200:
                print("successful")
            else:
                print("fail")
        except Exception as error:
            raise ValidationError(str(error))
        # print(response.content)
        print(response.status_code)

class Propertyline(models.Model):
    _name = 'property.line'

    property_id = fields.Many2one('property')
    area = fields.Float()
    description = fields.Char()

