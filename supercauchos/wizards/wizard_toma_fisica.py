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

class TomaFisica(models.TransientModel):
    _name = "stock.wizard.toma.fisica" ## = nombre de la carpeta.nombre del archivo deparado con puntos

    # date_from = fields.Date(string='Date From', default=lambda *a:datetime.now().strftime('%Y-%m-%d'))
    # date_to = fields.Date('Date To', default=lambda *a:(datetime.now() + timedelta(days=(1))).strftime('%Y-%m-%d'))
    date_now = fields.Datetime(string='Date Now', default=lambda *a:datetime.now())

    def print_inventario(self):
        return {'type': 'ir.actions.report','report_name': 'supercauchos.inventario_toma_fisica','report_type':"qweb-pdf"}
