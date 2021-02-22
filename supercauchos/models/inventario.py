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

class InventarioProductos(models.Model):
	_inherit = "product.product"

	model = fields.Char(string='Modelo', related='product_tmpl_id.model')
	iva = fields.Char(string='I.V.A.', related='product_tmpl_id.iva')
	type_cauchos = fields.Char(string='Tipo de Caucho', related='product_tmpl_id.type_cauchos')
	tarps = fields.Char(string='Lonas', related='product_tmpl_id.tarps')
	load_speed = fields.Char(string='Load/Speed', related='product_tmpl_id.load_speed')
	service_in = fields.Char(string='Service Index', related='product_tmpl_id.service_in')
	filler = fields.Float(string='Nro. Filler', related='product_tmpl_id.filler')
	filler_per = fields.Float(string='Filler Facturado (%)', related='product_tmpl_id.filler_per')
	brand_id = fields.Many2one('product.brand', string='Marca', related='product_tmpl_id.brand_id')
	#group_id = fields.Many2one('product.group', string='Grupo', related='product_tmpl_id.group_id')
	qty_hq = fields.Char(string='Qty Of 40HQ', related='product_tmpl_id.qty_hq')
	
	tax_cloud = fields.Char(string='Categoría TaxCloud', related='product_tmpl_id.tax_cloud')
	deote = fields.Date(string='Fecha de Fabricación', related='product_tmpl_id.deote')
	deoten = fields.Date(string='Fecha de Caducidad/Vencimiento', related='product_tmpl_id.deoten')
	estr_retir_prod = fields.Char(string='Estrategia de Retirada del producto.', related='product_tmpl_id.estr_retir_prod')

class InventarioProductos(models.Model):
	_inherit = "product.template"

	model = fields.Char(string='Modelo')
	iva = fields.Char(string='I.V.A.')
	type_cauchos = fields.Char(string='Tipo de Caucho')
	tarps = fields.Char(string='Lonas')
	load_speed = fields.Char(string='Load/Speed')
	service_in = fields.Char(string='Service Index')
	filler = fields.Float(string='Nro. Filler')
	filler_per = fields.Float(string='Filler Facturado (%)')
	brand_id = fields.Many2one('product.brand', string='Marca')
	group_id = fields.Many2one('product.group', string='Grupo')
	qty_hq = fields.Char(string='Qty Of 40HQ')

	tax_cloud = fields.Char(string='Categoría TaxCloud')
	deote = fields.Date(string='Fecha de Fabricación')
	deoten = fields.Date(string='Fecha de Caducidad/Vencimiento')
	estr_retir_prod = fields.Char(string='Estrategia de Retirada del producto.')

class MarcasProductos(models.Model):
	_name = 'product.brand'

	name = fields.Char(string='Nombre')

class GruposProductos(models.Model):
	_name = 'product.group'

	name = fields.Char(string='Nombre')
