from odoo import api, fields, models


class PurchaseConditionsPayment(models.Model):
    _inherit = 'purchase.order'

    request_payment_order = fields.Boolean(string='Request Payment Order')
    
class ResPartnerConditionsPayment(models.Model):
    _inherit = 'res.partner'

    trading_conditions = fields.Html(string='Trading Conditions')
