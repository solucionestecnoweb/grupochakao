from odoo import api, fields, models


class PurchaseCompareMultiple(models.Model):
    _name = 'purchase.compare.multiple'
    _description = 'Model for comparations of multiple purchase order prices'

    name = fields.Char(string='Reference')
    purchase_order_ids = fields.Many2many(comodel_name='purchase.order', string='Purchase Orders')
    is_comparable = fields.Boolean(compute='_compute_comparable')
    purchase_compared_prices_ids = fields.One2many(comodel_name='purchase.compared.prices', inverse_name='purchase_compare_multiple_id', string='Purchase Compared Prices')
    
    def _compute_comparable(self):
        if len(purchase_order_ids) > 3 or len(purchase_order_ids) < 2:
            return {'warning': {'message':'El número de ordenes de pago debe ser entre 2 y 3 registros'}}

    def compare_price(self):
        for item in self.purchase_order_ids: #Inicia el ciclo para comparar precios
            price_l = 0
            provider_l = ''
            price_m = 0
            provider_m = ''
            price_h = 0
            provider_h = ''
            for line in item.order_line: #Ubica en las lineas de productos
                
                if line.price_unit < price_l or price_l == 0:
                    price_l = line.price_unit
                    provider_l = item.partner_id.name
                if line.price_unit > price_h or price_h == 0:
                    price_h = line.price_unit
                    provider_h = item.partner_id.name
                if line.price_unit > price_l and line.price_unit < price_h or price_m == 0:
                    price_m = line.price_unit
                    provider_m = item.partner_id.name
                values = {
                    'provider_id': item.partner_id.id,
                    'product_id': line.product_template_id.id,
                    'price1': ,
                    'price2': ,
                    'price3': ,
                    'purchase_compare_multiple_id': self.id,
                }
                

    @api.constrains('id')
    def _compute_name(self):
        if self.id == False and self.name == False:
            self.name = self.env['ir.sequence'].next_by_code('purchase.compare.multiple.sequence')

class PurchaseComparedPrices(models.Model):
    _name = 'purchase.compared.prices'

    product_id = fields.Many2one(comodel_name='product.product', string='Product')
    price1 = fields.Text(string='Provider + lower price')
    price2 = fields.Text(string='Provider + half price')
    price3 = fields.Text(string='Provider + higher price')
    purchase_compare_multiple_id = fields.Many2one(comodel_name='purchase.compare.multiple', string='Purchase Compare')

class PurchaseComparedPrices(models.Model):
    _name = 'purchase.compared.prices.lines'

    product_id = fields.Many2one(comodel_name='product.product', string='Product')
    price1 = fields.Text(string='Provider + lower price')
    price2 = fields.Text(string='Provider + half price')
    price3 = fields.Text(string='Provider + higher price')
    purchase_compare_multiple_id = fields.Many2one(comodel_name='purchase.compare.multiple', string='Purchase Compare')

