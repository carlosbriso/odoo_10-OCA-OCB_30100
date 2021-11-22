# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from odoo import models, fields, api, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.exceptions import Warning
from datetime import datetime
import logging
import pprint

_logger = logging.getLogger(__name__)


###############################################################################
#   account.invoice                                                           #
###############################################################################

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    # ------------------------ METHODS  OVERWRITTEN ---------------------------

    @api.multi
    def invoice_validate(self):
        result = super(AccountInvoice, self).invoice_validate()
        for invoice in self:
            if invoice.name:
                invoice.write({
                    'number': invoice.name,
                })
        return result

    # ---------------------------- NEW METHODS --------------------------------

    @api.multi
    def _set_date_due(self, FechaLimitePago):
        for invoice in self:
            invoice.write({
                'date_due': FechaLimitePago,
            })

    @api.multi
    def _set_line_concepto_repercutible(self, ConceptoRepercutibleMain):
        ConceptoRepercutible = ConceptoRepercutibleMain.find('ConceptoRepercutible').text
        TipoImpositivoConceptoRepercutible = ConceptoRepercutibleMain.find('TipoImpositivoConceptoRepercutible').text
        FechaDesde = ConceptoRepercutibleMain.find('FechaDesde').text
        FechaHasta = ConceptoRepercutibleMain.find('FechaHasta').text
        UnidadesConceptoRepercutible = ConceptoRepercutibleMain.find('UnidadesConceptoRepercutible').text
        PrecioUnidadConceptoRepercutible = ConceptoRepercutibleMain.find('PrecioUnidadConceptoRepercutible').text
        ImporteTotalConceptoRepercutible = ConceptoRepercutibleMain.find('ImporteTotalConceptoRepercutible').text
        for invoice in self:
            concepto = self.env['account.invoice.103'].search([
                ('code', '=', ConceptoRepercutible)
            ])
            if len(concepto) > 0:
                concepto_name = concepto[0].name
            else:
                concepto_name = _('Unknown')
            invoice_line = self.env['account.invoice.line'].create({
                'name': concepto_name,
                'quantity': float(UnidadesConceptoRepercutible),
                'price_unit': float(PrecioUnidadConceptoRepercutible),
                'account_id': self.env.ref('l10n_es.1_pgc_7000_child').id,
            })
            invoice.write({
                'invoice_line_ids': [(6, 0, [invoice_line.id])],
            })

    @api.multi
    def _set_line_potencia(self, Potencia, NumeroDias, IVA):
        TerminoPotencia = Potencia.find('TerminoPotencia')
        FechaDesde = TerminoPotencia.find('FechaDesde').text
        FechaHasta = TerminoPotencia.find('FechaHasta').text
        Periodo = TerminoPotencia.find('Periodo')
        PotenciaContratada = Periodo.find('PotenciaContratada').text
        PotenciaMaxDemandada = Periodo.find('PotenciaMaxDemandada').text
        PotenciaAFacturar = Periodo.find('PotenciaAFacturar').text
        PrecioPotencia = Periodo.find('PrecioPotencia').text
        ImporteTotalTerminoPotencia = Potencia.find('ImporteTotalTerminoPotencia').text
        BaseImponible = IVA.find('BaseImponible').text
        Porcentaje = IVA.find('Porcentaje').text
        Importe = IVA.find('Importe').text
        if Porcentaje == '21':
            tax_id = self.env.ref('l10n_es.1_account_tax_template_s_iva21b').id
        else:
            tax_id = False
        for invoice in self:
            invoice_line = self.env['account.invoice.line'].create({
                'name': _('Power'),
                'quantity': float(float(PotenciaAFacturar) * float(NumeroDias)),
                'price_unit': float(PrecioPotencia),
                'account_id': self.env.ref('l10n_es.1_pgc_7000_child').id,
                'invoice_line_tax_ids': [(6, 0, [tax_id])],
            })
            invoice.write({
                'invoice_line_ids': [(4, invoice_line.id)],
            })

    @api.multi
    def _set_line_energia_activa(self, EnergiaActiva, NumeroDias, IVA):
        TerminoEnergiaActiva = EnergiaActiva.find('TerminoEnergiaActiva')
        FechaDesde = TerminoEnergiaActiva.find('FechaDesde').text
        FechaHasta = TerminoEnergiaActiva.find('FechaHasta').text
        Periodo = TerminoEnergiaActiva.find('Periodo')
        ValorEnergiaActiva = Periodo.find('ValorEnergiaActiva').text
        PrecioEnergia = Periodo.find('PrecioEnergia').text
        ImporteTotalEnergiaActiva = EnergiaActiva.find('ImporteTotalEnergiaActiva').text
        BaseImponible = IVA.find('BaseImponible').text
        Porcentaje = IVA.find('Porcentaje').text
        Importe = IVA.find('Importe').text
        if Porcentaje == '21':
            tax_id = self.env.ref('l10n_es.1_account_tax_template_s_iva21b').id
        else:
            tax_id = False
        for invoice in self:
            invoice_line = self.env['account.invoice.line'].create({
                'name': _('Active energy'),
                'quantity': float(ValorEnergiaActiva),
                'price_unit': float(PrecioEnergia),
                'account_id': self.env.ref('l10n_es.1_pgc_7000_child').id,
                'invoice_line_tax_ids': [(6, 0, [tax_id])],
            })
            invoice.write({
                'invoice_line_ids': [(4, invoice_line.id)],
            })

    @api.multi
    def _set_line_alquileres(self, Alquileres, IVA):
        ImporteFacturacionAlquileres = Alquileres.find('ImporteFacturacionAlquileres').text
        PrecioDiarioAlquiler = Alquileres.find('PrecioDiarioAlquiler')
        PrecioDia = PrecioDiarioAlquiler.find('PrecioDia').text
        NumeroDias = PrecioDiarioAlquiler.find('NumeroDias').text
        BaseImponible = IVA.find('BaseImponible').text
        Porcentaje = IVA.find('Porcentaje').text
        Importe = IVA.find('Importe').text
        if Porcentaje == '21':
            tax_id = self.env.ref('l10n_es.1_account_tax_template_s_iva21b').id
        else:
            tax_id = False
        for invoice in self:
            invoice_line = self.env['account.invoice.line'].create({
                'name': _('Renting'),
                'quantity': float(NumeroDias),
                'price_unit': float(PrecioDia),
                'account_id': self.env.ref('l10n_es.1_pgc_7000_child').id,
                'invoice_line_tax_ids': [(6, 0, [tax_id])],
            })
            invoice.write({
                'invoice_line_ids': [(4, invoice_line.id)],
            })
