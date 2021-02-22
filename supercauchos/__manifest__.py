# Copyright 2020 GregorioCode <Info@gregoriocode.com>


{
    "name": "Super Cauchos Chakao",
    "version": "13.0.1.0.1",
    "category": "app",
    "author": "Ing Gregorio Blanco",
    "website": "https://gregoriocode.com",
    "license": "AGPL-3",
    "depends": ['base', 'fleet', 'stock'],
    "data": [
        "security/ir.model.access.csv",
        "views/inventory_products.xml",
        "report/inventario_toma_fisica.xml",
        "report/inventario_picking_salidas.xml",
        "views/wizard_inventory_picking_salida.xml",
        "views/wizard_inventory_toma_fisica.xml",
        #"views/flota_registro_combustible.xml",
        #"views/flota_registro_servicios_internos_vehiculos.xml",
        #"views/flota_registro_control_disponibilidad.xml",
        #"report/flota_consumo_combustible.xml",
    ],
    'installable': True,
}
