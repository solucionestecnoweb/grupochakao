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

class PurchaseOrderImports(models.Model):
	_inherit = "purchase.order"

	load_plan = fields.Binary(string='Load Plan')
	package_list = fields.Binary(string='Package List')
	landed_date = fields.Date(string='Landed Date')
	merchandise_available_load = fields.Binary(string='Merchandise Available for Load')

	aduana_agency_id = fields.Many2one(comodel_name='purchase.order.imports.aduana', string='Aduana Agency')
	aduana_costs = fields.Float(string='Aduana Estimated Costs')
	aduana_date = fields.Date(string='Aduana Estimated Date')
	aduana_doc = fields.Binary(string='Attach Document')

	aduana_payment_ids = fields.One2many(comodel_name='purchase.order.imports.aduana.payment', inverse_name='purchase_order_id', string=' Aduana Payment')
	
class PurchaseOrderLineImports(models.Model):
	_inherit = "purchase.order.line"

	pr = fields.Char(string='PR')
	pronto_pago = fields.Char(string='Pronto Pago Promotion')
	super_promo = fields.Char(string='Super Promo Promotion')
	apart_to_seller = fields.Integer(string='Set Apart to Seller', compute="compute_seller")
	apart_qty_available = fields.Integer(string='Set Apart Quantity Available', compute='compute_available')
	
	def compute_seller(self):
		for item in self:
			xfind = self.env['sale.order.line'].search([
				('state', 'in', ('draft', 'sent')),
				('product_template_id', '=', item.product_template_id.id)
			])
			item.apart_to_seller = 0
			for line in xfind:
				item.apart_to_seller += line.product_uom_qty

	def compute_available(self):
		for item in self:
			item.apart_qty_available = item.product_qty - item.apart_to_seller

class PurchaseOrderImportsAduana(models.Model):
	_name = "purchase.order.imports.aduana"
	_inherit = ['mail.thread', 'mail.activity.mixin']
	
	name = fields.Char(string='Aduana name')
	
class PurchaseOrderImportsAduanaPayment(models.Model):
	_name = "purchase.order.imports.aduana.payment"
	_inherit = ['mail.thread', 'mail.activity.mixin']
	
	payment_date = fields.Date(string='Payment Date')
	payment_concept = fields.Char(string='Payment Concept')
	payment_amount = fields.Float(string='Payment Amount')
	payment_approve = fields.Boolean(string='Approve?')
	payment_doc = fields.Binary(string='Attach Document')
	payment_observation = fields.Text(string='Observation')
	purchase_order_id = fields.Many2one(comodel_name='purchase.order', string='Purchase Order')
	currency_id = fields.Many2one(comodel_name='res.currency', string='Currency', default=lambda self: self.env.user.company_id.currency_id)

class PurchaseOrderImportsPayment(models.Model):
	_name = "purchase.order.imports.payment"
	_inherit = ['mail.thread', 'mail.activity.mixin']

	name = fields.Many2one(comodel_name='res.partner', string='Supplier')
	import_model = fields.Char(string='Model')
	import_brand = fields.Char(string='Brand')
	invoice_number = fields.Char(string='Invoice Number / Proforma')
	import_qty = fields.Float(string='Quantity')
	percent_payed = fields.Selection(string='%', selection=[('30', '30%'), ('70', '70%'),('100', '100%')], default='30')
	import_amount = fields.Float(string='Amount')
	payment_date = fields.Date(string='Payment Date', default=fields.Date.today())
	etd = fields.Date(string='ETD')
	eta = fields.Date(string='ETA')
	status = fields.Selection(string='Status', selection=[('transit', 'Transit'), ('production', 'Production')], default='transit', track_visibility='onchange')
	currency_id = fields.Many2one(comodel_name='res.currency', string='Currency', default=lambda self: self.env.user.company_id.currency_id)
	status_payment = fields.Selection(string='Status Payment', selection=[('paid', 'Paid'), ('not_paid', 'Not Paid')], default='not_paid', track_visibility='onchange')
	alert_field = fields.Boolean(compute='compute_alert')

	def compute_alert(self):
		for item in self:
			item.alert_field = False
			date_today = fields.Date.today()
			if (item.payment_date - date_today).days <= 7:
				item.alert_field = True
	
class PurchaseOrderImportsContainers(models.Model):
	_name = "purchase.order.imports.containers"
	_inherit = ['mail.thread', 'mail.activity.mixin']

	nbl_container = fields.Date(string='N BL / Container')
	invoice_number = fields.Many2one(comodel_name='account.move', string='Invoice Number')
	container_type = fields.Char(string='Type')
	container_brand = fields.Char(string='Brand')
	cont = fields.Float(string='CONT')
	tires = fields.Float(string='Tires')
	agency = fields.Many2one(comodel_name='res.partner', string='Agency')
	shipping_company = fields.Many2one(comodel_name='res.partner', string='Shipping Company')
	eta_ven = fields.Date(string='ETA/VEN')
	harbor = fields.Float(string='Harbor')
	warehouse = fields.Date(string='Warehouse')
	estate = fields.Selection(string='Estate', selection=[('transit', 'Transit'), ('to_board', 'To Board')], default='transit')
	vessel = fields.Char(string='Vessel')
	condition = fields.Selection(string='Condition', selection=[('to_be_released', 'To be released'), ('released', 'Released')], default='to_be_released')

class PurchaseOrderImportsImportations(models.Model):
	_name = "purchase.order.imports.importations"
	_inherit = ['mail.thread', 'mail.activity.mixin']

	name = fields.Many2one(comodel_name='res.partner', string='Supplier')
	importation_brand = fields.Char(string='Brand')
	prof = fields.Char(string='Prof')
	importation_type = fields.Char(string='Type')
	f_prof = fields.Date(string='F/Prof')
	invoice_id = fields.Many2one(comodel_name='account.move', string='Invoice')
	container = fields.Float(string='Cont')
	bl_date = fields.Date(string='BL Date')
	transc = fields.Float(string='Transc', compute='compute_transac')
	accumulated = fields.Float(string='Accumulated', compute='compute_accumulated')
	eta = fields.Date(string='ETA')
	transit = fields.Float(string='Transit', compute='compute_transit')
	nac = fields.Float(string='NAC')
	total = fields.Float(string='Total', compute='compute_total')
	
	def compute_transac(self):
		for item in self:
			item.transc = 0
			if item.f_prof and item.bl_date:
				item.transc = (item.bl_date - item.f_prof).days

	def compute_accumulated(self):
		for item in self:
			item.accumulated = 0
			if (item.container * item.transc) > 0:
				item.accumulated = item.container * item.transc
		
	def compute_transit(self):
		for item in self:
			item.transit = 0
			if item.bl_date and item.eta:
				item.transit = (item.eta - item.bl_date).days

	def compute_total(self):
		for item in self:
			item.total = item.transc + item.transit + item.nac
