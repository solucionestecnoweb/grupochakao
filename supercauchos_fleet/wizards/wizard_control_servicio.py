from datetime import datetime, timedelta
from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT

from odoo import models, fields, api, _, tools
from odoo.exceptions import UserError
import openerp.addons.decimal_precision as dp
import logging

import io
from io import BytesIO

import xlsxwriter
import shutil
import base64
import csv
import xlwt

_logger = logging.getLogger(__name__)

class FlotaControlServicioLineas(models.TransientModel):
    _name = "fleet.wizard.services.lines"

    type_vehicle = fields.Selection(string='Tipo de Transporte', selection=[('propio', 'propio'), ('externo', 'Externo')], default="propio")
    driver_id = fields.Many2one('res.partner', string='Conductor')
    travel_qty = fields.Integer(string='Cantidad de Viajes')
    filler = fields.Float(string='Filler')
    km_traveled = fields.Float(string='KM Recorrido')
    days_street = fields.Integer(string='Días en la calle')

class FlotaControlServicio(models.TransientModel):
    _name = "fleet.wizard.services"

    date_from = fields.Date(string='Date From', default=lambda *a:datetime.now().strftime('%Y-%m-%d'))
    date_to = fields.Date('Date To', default=lambda *a:(datetime.now() + timedelta(days=(1))).strftime('%Y-%m-%d'))
    date_now = fields.Datetime(string='Date Now', default=lambda *a:datetime.now())

    lines_ids = fields.Many2many('fleet.wizard.services.lines',string='Lineas')

    def print_ordenes(self):
        self.env['fleet.wizard.services.lines'].search([]).unlink()
        self._get_lineas()
        return {'type': 'ir.actions.report','report_name': 'supercauchos_fleet.flota_control_servicio','report_type':"qweb-pdf"}


    #VEHICULOS
    def vehiculos_p(self):
        values = []
        temp_id = 0
        busqueda = self.env['fleet.wizard.services.lines'].search([
            ('type_vehicle', '=', 'propio')
        ])
        for item in busqueda.sorted(key=lambda driver: driver.driver_id.id):
            busqueda2 = self.env['fleet.wizard.services.lines'].search([
                ('type_vehicle', '=', 'propio'),
                ('driver_id', '=', item.driver_id.id),
            ])
            vehicle_type = ''
            driver = ''
            travels = 0
            fillers = 0
            traveled_km = 0.0
            days = 0
            temp_value = []
            for line in busqueda2:
                driver = line.driver_id.name
                travels = travels + line.travel_qty
                fillers = fillers + line.filler
                traveled_km = traveled_km + line.km_traveled
                days = days + line.days_street
            if temp_id != item.driver_id.id:
                temp_value = [driver, travels, fillers, traveled_km, days]
                values.append(temp_value)
                temp_id = item.driver_id.id
        return values

    def vehiculos_e(self):
        values = []
        temp_id = 0
        busqueda = self.env['fleet.wizard.services.lines'].search([
            ('type_vehicle', '=', 'externo')
        ])
        for item in busqueda.sorted(key=lambda driver: driver.driver_id.id):
            busqueda2 = self.env['fleet.wizard.services.lines'].search([
                ('type_vehicle', '=', 'externo'),
                ('driver_id', '=', item.driver_id.id),
            ])
            vehicle_type = ''
            driver = ''
            travels = 0
            fillers = 0
            traveled_km = 0.0
            days = 0
            temp_value = []
            for line in busqueda2:
                driver = line.driver_id.name
                travels = travels + line.travel_qty
                fillers = fillers + line.filler
                traveled_km = traveled_km + line.km_traveled
                days = days + line.days_street
            if temp_id != item.driver_id.id:
                temp_value = [driver, travels, fillers, traveled_km, days]
                values.append(temp_value)
                temp_id = item.driver_id.id
        return values

    #LINEAS
    def _get_lineas(self):
        t = self.env['fleet.wizard.services.lines']
        ###Busqueda de asignaciones
        busqueda = self.env['fleet.vehicle.log.assignment.control'].search([
            ('status', 'in', ('confirmed','done')),
            ('date_ini', '>=', self.date_from),
            ('date_end', '<=', self.date_to)
        ])
        ###Iteración de todas las asignaciones
        for item in busqueda.sorted(key=lambda driver: driver.driver_id.id):
            dias = item.date_end - item.date_ini
            street_days = dias.days + 1
            filler = 0
            odometer = 0
            for line in item.stock_picking_ids:
                l = line.move_ids_without_package
                if len(l) > 1:
                    for lines in l:
                        filler = filler + (lines.product_id.filler * lines.product_uom_qty)
                else:
                    filler = filler + (l.product_id.filler * l.product_uom_qty)
            find_odometer = item.env['fleet.vehicle.odometer'].search([
                ('date', '>=', item.date_ini),
                ('date', '<=', item.date_end),
                ('vehicle_id', '=', item.vehicle_id.id),
                ('driver_id', '=', item.driver_id.id)
            ])
            for lines in find_odometer:
                odometer = odometer + lines.value
            values = {
            'type_vehicle': item.vehicle_id.type_vehicle,
            'driver_id': item.driver_id.id,
            'travel_qty': 1,
            'filler': filler,
            'km_traveled': odometer,
            'days_street': street_days,
            }
            t.create(values)
        self.lines_ids = t.search([])

        