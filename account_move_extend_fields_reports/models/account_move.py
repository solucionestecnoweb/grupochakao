# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
import json
from datetime import datetime, timedelta
import base64
from io import StringIO
from odoo import api, fields, models
from datetime import date
from odoo.tools.float_utils import float_round
from odoo.exceptions import Warning

import time

class AccountMoveExtend(models.Model):
	_inherit = "account.move"

	seller_id = fields.Many2one(comodel_name='res.partner', string='Seller')
	payment_condition = fields.Selection(string='Payment Condition', selection=[('credit', 'Credit'), ('cash', 'Cash'),])

	@api.onchange('partner_id')
	def _onchange_partner_id(self):
		xfind = self.env['account.payment'].search([
			('partner_id', '=', self.partner_id.id),
			('anticipo', '=', True),
			('state', '=', 'posted')
		])
		if len(xfind) > 0:
			return {'warning': {'message':'El cliente posee un anticipo disponible'}}