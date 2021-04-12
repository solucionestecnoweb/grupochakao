from odoo import api, fields, models


class ProductPricesList(models.Model):
    _inherit = 'product.product'

    prices_list_ids = fields.One2many('product.pricelist', 'item_ids', string=' Prices', compute='_compute_prices_list')

    def _compute_prices_list(self):
        xfind = self.env['product.pricelist'].search([
            ('item_ids.product_tmpl_id', '=', self.product_tmpl_id.id)
        ])
        self.prices_list_ids = xfind

class TemplatePricesList(models.Model):
    _inherit = 'product.template'

    prices_list_ids = fields.One2many('product.pricelist', 'item_ids', string=' Prices', compute='_compute_prices_list')

    def _compute_prices_list(self):
        xfind = self.env['product.pricelist'].search([
            ('item_ids.product_tmpl_id', '=', self.id)
        ])
        self.prices_list_ids = xfind