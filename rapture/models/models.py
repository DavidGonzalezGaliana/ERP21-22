# -*- coding: utf-8 -*-
from odoo import models, fields, api


class rapture(models.Model):
    _name = 'rapture.rapture'
    _description = 'rapture.rapture'

    name = fields.Char()
    science  = fields.Integer(default=100)


class player(models.Model):
    _name = 'rapture.player'
    _description = 'rapture.player'

    playerName = fields.Char(default="Andrew Ryan")
    birthplace = fields.Char(default="Russian Empire")
    gender = fields.Char(default="Male")
    year_of_birth = fields.Integer(default=1911)

    life = fields.Integer(default=100)
    hunger = fields.Integer(default=100)
    sanity = fields.Integer(default=100)
    oxygen_consumption = fields.Integer(default=0)


#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
