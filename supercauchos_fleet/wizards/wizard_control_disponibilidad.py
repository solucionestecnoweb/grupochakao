from datetime import datetime, timedelta, date
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

class FlotaControlDisponibilidadLineas(models.TransientModel):
    _name = "fleet.wizard.available.lines"

    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehículo')
    date_assign = fields.Datetime(string='Asignado')
    available = fields.Boolean(string='Disponibilidad')

class FlotaControlDisponibilidad(models.TransientModel):
    _name = "fleet.wizard.available"

    date_from = fields.Date(string='Date From', default=lambda *a:datetime.now().strftime('%Y-%m-%d'))
    date_now = fields.Datetime(string='Date Now', default=lambda *a:datetime.now())

    lines_ids = fields.Many2many('fleet.wizard.available.lines',string='Lineas')

    def print_ordenes(self):
        self.env['fleet.wizard.available.lines'].search([]).unlink()

        dia = self.obtener_dias_del_mes(self.date_from.month, self.date_from.year)
        self._get_lineas(self.date_from, dia)

        return {'type': 'ir.actions.report','report_name': 'supercauchos_fleet.flota_control_disponibilidad','report_type':"qweb-pdf"}


    #VEHICULOS
    def vehiculos(self):
        busqueda = self.env['fleet.vehicle'].search([])
        return busqueda

    #FECHAS
    def es_bisiesto(self, anio: int) -> bool:
        return anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0)


    def obtener_dias_del_mes(self, mes: int, anio: int) -> int:
        # Abril, junio, septiembre y noviembre tienen 30
        if mes in [4, 6, 9, 11]:
            return 30
        # Febrero depende de si es o no bisiesto
        if mes == 2:
            if self.es_bisiesto(anio):
                return 29
            else:
                return 28
        else:
            # En caso contrario, tiene 31 días
            return 31

    def nueva_fecha(self, dia, mes, agno):
        fecha = str(dia)+'/'+str(mes)+'/'+str(agno)
        fecha = datetime.strptime(fecha, '%d/%m/%Y')
        return fecha


    #LINEAS
    def _get_lineas(self, fecha, dia):
        fecha_ini = "01/" + str(fecha.month) + "/" + str(fecha.year)
        fecha_fin = str(dia) + "/" + str(fecha.month) + "/" + str(fecha.year)
        fecha_fin = datetime.strptime(fecha_fin, '%d/%m/%Y').date()
        t = self.env['fleet.wizard.available.lines']
        
        for item in self.vehiculos():
            assignments = self.env['fleet.vehicle.log.assignment.control'].search([
                ('date_ini', '>=', fecha_ini),
                ('date_end', '<=', fecha_fin),
                ('vehicle_id', '=', item.id),
                ('status', 'in', ('confirmed','done'))
            ])
            xdate = datetime.strptime(fecha_ini,'%d/%m/%Y').date()
            if len(assignments) > 0:
                while xdate <= fecha_fin:
                    temp = True
                    for line in assignments:
                        if xdate >= line.date_ini and xdate <= line.date_end:
                            values= {
                                'vehicle_id': line.vehicle_id.id,
                                'date_assign': xdate,
                                'available': False,
                            }
                            temp = False
                        elif temp:
                            values={
                                'vehicle_id': line.vehicle_id.id,
                                'date_assign': xdate,
                                'available': True,
                            }
                    t.create(values)
                    xdate = xdate + timedelta(days=1)
            else:
                while xdate <= fecha_fin:
                    values={
                        'vehicle_id': item.id,
                        'date_assign': xdate,
                        'available': True,
                    }
                    t.create(values)
                    xdate = xdate + timedelta(days=1)

        self.lines_ids = self.env['fleet.wizard.available.lines'].search([])
