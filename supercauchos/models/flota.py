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

class FlotaCombustible(models.Model):
    _inherit = "fleet.vehicle.log.fuel"

    fuel_type = fields.Selection(string='Tipo de Combustible', selection=[('gasolina', 'Gasolina'), ('gasoil', 'Gasoil')])
    cistern_lts = fields.Float(string='Litros Cisterna')
    vehicle_consume = fields.Float(string='Consumo Vehículo')
    cistern_lts_ava = fields.Float(string='Disponible Litros Cisterna')
    lts_cistern = fields.Float(string='Cisterna Litros')

class FlotaMantenimiento(models.Model):
    _name = "fleet.vehicle.log.internal.services"

    name = fields.Char(string='Título')
    status = fields.Selection(string='Etapas', selection=[('nueva_solicitud', 'Nueva Solicitud'), ('en_progreso', 'En Progreso'), ('reparado', 'Reparado'), ('desechar', 'Desechar')], default="nueva_solicitud")
    created_by = fields.Many2one('res.users',string='Creado Por')
    e_type = fields.Selection(string='Tipo de Equipamento', selection=[('flota_vehiculos', 'Flota de Vehículos'), ('maquinas_herramientas', 'Máquinas o Herramientas')])
    placa = fields.Char(string='Placa')
    km = fields.Float(string='Kilometraje')
    driver = fields.Char(string='Conductor')
    m_type = fields.Selection(string='Tipo de Mantenimiento', selection=[('preventivo', 'Preventivo'), ('correctivo', 'Correctivo')])
    m_team = fields.Selection(string='Equipo', selection=[('internal', 'Mantenimiento Interno'), ('external', 'Mantenimiento Externo')], default="internal")
    responsable = fields.Char(string='Responsable')
    planned_date = fields.Date(string='Fecha Prevista')
    duration = fields.Float(string='Duración')
    priority = fields.Selection(string='Prioridad', selection=[('', ''), ('low', 'Baja'), ('med', 'Media'), ('high', 'Alta')])
    company_id = fields.Many2one('res.company',string='Compañía')
    treatment = fields.Char(string='Tratamiento')
    internal_note = fields.Text(string='Nota interna')

    def status_ep(self):
        self.status = "en_progreso"

    def status_r(self):
        self.status = "reparado"

    def status_d(self):
        self.status = "desechar"

class FlotaMantenimiento(models.Model):
    _name = "fleet.vehicle.log.disponibility.control"

    name = fields.Many2one('fleet.vehicle', string='Vehículo')
    plate_num = fields.Char(string='Placa', related='name.license_plate')
    calendar_day = fields.Date(string='Día Calendario')
    total_ava = fields.Integer(string='Disponibilidad Total')
