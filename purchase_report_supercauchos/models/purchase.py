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

class PurchaseOrderExtend(models.Model):
	_inherit = "purchase.order"

	assigned_to_id = fields.Many2one(comodel_name='res.partner', string='Assigned to')
	approve_by_id = fields.Many2one(comodel_name='res.partner', string='Approve by')
	vice_presidency = fields.Boolean(string='Viceprecidency')
	treasury_manager = fields.Boolean(string='Treasury Manager')
	approve_notes = fields.Text(string='Observations')
	

	department = fields.Char(string='Requesting Department')
	requisition = fields.Char(string='Requisition')
	priority = fields.Selection(string='Priority', selection=[('low', 'Low'), ('meddium', 'Meddium'), ('high', 'High')], default="low")
	
	def _date_now_purchase(self):
		xdate = datetime.now() - timedelta(hours=4)
		return xdate

class PurchaseOrderImportations(models.Model):
	_name = "purchase.order.importations"

	partner_id = fields.Many2one(comodel_name='res.partner', string='Supplier')
	import_model = fields.Char(string='Model')
	import_brand = fields.Char(string='Brand')
	invoice_number = fields.Char(string='Invoice Number / Proforma')
	import_qty = fields.Integer(string='Quantity')
	percent_30 = fields.Float(string='30%')
	percent_70 = fields.Float(string='70%')
	percent_100 = fields.Float(string='100%')
	import_amount = fields.Float(string='Amount')
	payment_date = fields.Date(string='Payment Date')
	etd = fields.Char(string='ETD')
	eta = fields.Char(string='ETA')
	status = fields.Char(string='Status')
	
class PurchaseOrderImportationsContainers(models.Model):
	_name = "purchase.order.importations.containers"

	nbl_container = fields.Char(string='N BL / Container')
	invoice_number = fields.Char(string='Invoice Number')
	container_type = fields.Char(string='Type')
	container_brand = fields.Char(string='Brand')
	cont = fields.Char(string='CONT')
	tires = fields.Char(string='Tires')
	agency = fields.Char(string='Agency')
	shipping_company = fields.Char(string='Shipping Company')
	eta_ven = fields.Char(string='ETA/VEN')
	harbor = fields.Char(string='Harbor')
	warehouse = fields.Char(string='Warehouse')
	status_w = fields.Char(string='Status')
	vessel = fields.Char(string='Vessel')
	status_v = fields.Char(string='Status')

class PurchaseOrderImportationsCycle(models.Model):
	_name = "purchase.order.importations.cycle"

	partner_id = fields.Many2one(comodel_name='res.partner', string='Supplier')
	cycle_brand = fields.Char(string='Brand')
	invoice_number = fields.Char(string='Proforma')
	cycle_type = fields.Char(string='Type')
	prof_date = fields.Date(string='Proforma Date')
	invoice_id = fields.Many2one(comodel_name='account.move', string='Invoice')
	cont = fields.Char(string='CONT')
	bl_date = fields.Date(string='BL Date')
	transc = fields.Char(string='Transc')
	acumulated = fields.Float(string='Acumulated')
	eta = fields.Char(string='ETA')
	traffic = fields.Float(string='Traffic')
	nac = fields.Float(string='NAC')
	total = fields.Float(string='Total')
	
class PurchaseOrderImportationsTraffic(models.Model):
	_name = "purchase.order.importations.traffic"

	availability = fields.Integer(string='Availability')
	measures = fields.Char(string='Measures')
	pr = fields.Char(string='PR')
	traffic_models = fields.Char(string='Models')
	price = fields.Float(string='Price')
	pronto_pago = fields.Char(string='Pronto Pago Promotion')
	super_promo = fields.Char(string='Super Promo Promotion')
	apart_to_seller = fields.Integer(string='Set Apart to Seller')
	apart_qty_available = fields.Integer(string='Set Apart Quantity Available')

class PurchaseOrderImportationsShipping(models.Model):
	_name = "purchase.order.importations.shipping"
	
	
