# Copyright 2020 GregorioCode <Info@gregoriocode.com>


{
    "name": "Purchase Extend",
    "version": "13.0.1.0.1",
    "author": "Ing Gregorio Blanco",
    "website": "https://gregoriocode.com",
    "license": "AGPL-3",
    "depends": ['base', 'purchase'],
    "data": [
        "security/ir.model.access.csv",
        "views/purchase_order_form_extend.xml",
        "report/purchase_order_budget_extend.xml",
        "report/purchase_order_purchases_extend.xml",
        "views/purchase_order_menu_items_extend.xml",
        "views/purchase_order_importations.xml",
        "views/purchase_order_importations_containers.xml",
        "views/purchase_order_importations_cycle.xml",
        "views/purchase_order_importations_traffic.xml",
        "views/purchase_order_importations_shipping.xml",
        #"report/paper_format.xml",
        #"report/invoices.xml",
    ],
    'installable': True,
}
