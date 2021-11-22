# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import xml.etree.ElementTree as ET
from lxml import etree, objectify
import base64
import os
import re

import logging
_logger = logging.getLogger(__name__) 

FILE_EXTENSION = '.xml'


###############################################################################
#   import.xml                                                                #
###############################################################################

class ImportXML(models.TransientModel):
    _name = 'import.xml'

    # --------------------------- ENTITY  FIELDS ------------------------------

    source_file = fields.Binary(
        string='Choose a XML File',
        required=False,
        states={
            'importing': [('required', True)],
        }
    )

    filename = fields.Char(
        string='Filename',
        readonly=False,
    )

    state = fields.Selection(
        selection=[
            ('importing', 'Importing'),
            ('imported', 'Imported'),
        ],
        string='Status',
        default='importing',
    )

    xml_msg = fields.Text(
        string='OK message for records with no attachment',
        readonly=True,
    )

    error_msg = fields.Text(
        string='Error message for attachments',
        readonly=True,
    )

    # ------------------------------ METHODS ----------------------------------

    # @api.constrains('filename', 'state')
    # def _check_filename(self):
    #     for wzd in self:
    #         if wzd.state == 'importing':
    #             if wzd.filename:
    #                 file_extension = os.path.splitext(wzd.filename)[1]
    #                 if file_extension != '.xml':
    #                     raise ValidationError(
    #                         _('The file must have a xml extension.')
    #                     )

    # @api.onchange('filename')
    # def onchange_filename(self):
    #     if self.filename:
    #         file_extension = os.path.splitext(self.filename)[1]
    #         if file_extension != '.xml':
    #             raise ValidationError(
    #                 _('The file must have a xml extension.')
    #             )

    # @api.multi
    # def go_to_importing(self):
    #     self.write({
    #         'xml_msg': False,
    #         'error_msg': False,
    #         'state': 'importing',
    #     })
    #     return self.reopen_current_wizard()

    # @api.multi
    # def go_to_imported(self):
    #     self.write({
    #         'filename': False,
    #         'source_file': False,
    #         'state': 'imported',
    #     })
    #     return self.reopen_current_wizard()

    # @api.multi
    # def reopen_current_wizard(self):
    #     self.ensure_one()
    #     action = self.env.ref('ener_import_xml.action_import_xml').\
    #         read()[0]
    #     action.update({
    #         'res_id': self.id,
    #     })
    #     return action

    # ----------------------------- NEW METHODS -------------------------------

    @api.model
    def _get_data(self, data):
        name = data
        return name

    @api.model
    def _get_partner_id(self, Identificador):
        NIF = "ES" + Identificador
        partner = self.env['res.partner'].search([('vat', '=', NIF)])
        if not partner:
            raise ValidationError(
                _('Partner not found with this vat')
            )
        return partner.id

    @api.model
    def create_other_invoice(self, Factura):
        # DatosGeneralesOtrasFactura
        DatosGeneralesOtraFactura = Factura.find('DatosGeneralesOtrasFacturas')
            # DireccionSuministro
        DireccionSuministro = DatosGeneralesOtraFactura.find('DireccionSuministro')
        Pais = DireccionSuministro.find('Pais').text
        Provincia = DireccionSuministro.find('Provincia').text
        Municipio = DireccionSuministro.find('Municipio').text
        Poblacion = DireccionSuministro.find('Poblacion').text
        CodPostal = DireccionSuministro.find('CodPostal').text
        Calle = DireccionSuministro.find('Calle').text
        NumeroFinca = DireccionSuministro.find('NumeroFinca').text
            # DatosGeneralesOtrasFactura
        Cliente = DatosGeneralesOtraFactura.find('Cliente')
        TipoIdentificador = Cliente.find('TipoIdentificador').text
        Identificador = Cliente.find('Identificador').text
            # CodContrato
        CodContrato = DatosGeneralesOtraFactura.find('CodContrato').text
            # DatosGeneralesFactura
        DatosGeneralesFactura = DatosGeneralesOtraFactura.find('DatosGeneralesFactura')
        CodigoFiscalFactura = DatosGeneralesFactura.find('CodigoFiscalFactura').text
        TipoFactura = DatosGeneralesFactura.find('TipoFactura').text
        MotivoFacturacion = DatosGeneralesFactura.find('MotivoFacturacion').text
        FechaFactura = DatosGeneralesFactura.find('FechaFactura').text
        IdentificadorEmisora = DatosGeneralesFactura.find('IdentificadorEmisora').text
        ImporteTotalFactura = DatosGeneralesFactura.find('ImporteTotalFactura').text
        TipoMoneda = DatosGeneralesFactura.find('TipoMoneda').text
            # FechaBOE
        FechaBOE = DatosGeneralesOtraFactura.find('FechaBOE').text
        # ConceptoRepercutible
        ConceptoRepercutibleMain = Factura.find('ConceptoRepercutible')        
        # IVA
        IVA = Factura.find('IVA')
        BaseImponible = IVA.find('BaseImponible').text
        Porcentaje = IVA.find('Porcentaje').text
        Importe = IVA.find('Importe').text
        # --- Crear factura ---
        existing_invoice = self.env['account.invoice'].search([
            ('name', '=', self._get_data(CodigoFiscalFactura)),
            ('state', '=', 'draft'),
        ])
        if len(existing_invoice) > 0:
            existing_invoice.unlink()
        invoice = self.env['account.invoice'].create({
            'name': self._get_data(CodigoFiscalFactura),
            'partner_id': self._get_partner_id(Identificador),
            'date_invoice': self._get_data(FechaFactura),
            'origin': self._get_data(CodContrato),
        })
        invoice._set_line_concepto_repercutible(ConceptoRepercutibleMain)
        invoice.compute_taxes()
        return invoice

    @api.model
    def create_atr_invoice(self, Factura):
        # DatosGeneralesFacturaATR
        DatosGeneralesFacturaATR = Factura.find('DatosGeneralesFacturaATR')
            # DireccionSuministro
        DireccionSuministro = DatosGeneralesFacturaATR.find('DireccionSuministro')
        Pais = DireccionSuministro.find('Pais').text
        Provincia = DireccionSuministro.find('Provincia').text
        Municipio = DireccionSuministro.find('Municipio').text
        Poblacion = DireccionSuministro.find('Poblacion').text
        CodPostal = DireccionSuministro.find('CodPostal').text
        Calle = DireccionSuministro.find('Calle').text
        NumeroFinca = DireccionSuministro.find('NumeroFinca').text
            # DatosGeneralesOtrasFactura
        Cliente = DatosGeneralesFacturaATR.find('Cliente')
        TipoIdentificador = Cliente.find('TipoIdentificador').text
        Identificador = Cliente.find('Identificador').text
            # CodContrato
        CodContrato = DatosGeneralesFacturaATR.find('CodContrato').text
            # DatosGeneralesFactura
        DatosGeneralesFactura = DatosGeneralesFacturaATR.find('DatosGeneralesFactura')
        CodigoFiscalFactura = DatosGeneralesFactura.find('CodigoFiscalFactura').text
        TipoFactura = DatosGeneralesFactura.find('TipoFactura').text
        MotivoFacturacion = DatosGeneralesFactura.find('MotivoFacturacion').text
        FechaFactura = DatosGeneralesFactura.find('FechaFactura').text
        IdentificadorEmisora = DatosGeneralesFactura.find('IdentificadorEmisora').text
        Comentarios = DatosGeneralesFactura.find('Comentarios').text
        ImporteTotalFactura = DatosGeneralesFactura.find('ImporteTotalFactura').text
        TipoMoneda = DatosGeneralesFactura.find('TipoMoneda').text
            # DatosFacturaATR
        DatosFacturaATR = DatosGeneralesFacturaATR.find('DatosFacturaATR')
        FechaBOE = DatosFacturaATR.find('FechaBOE').text
        TarifaATRFact = DatosFacturaATR.find('TarifaATRFact').text
        ModoControlPotencia = DatosFacturaATR.find('ModoControlPotencia').text
        MarcaMedidaConPerdidas = DatosFacturaATR.find('MarcaMedidaConPerdidas').text
        IndicativoCurvaCarga = DatosFacturaATR.find('IndicativoCurvaCarga').text
                # PeriodoCCH
        PeriodoCCH = DatosFacturaATR.find('PeriodoCCH')
        FechaDesdeCCH = PeriodoCCH.find('FechaDesdeCCH').text
        FechaHastaCCH = PeriodoCCH.find('FechaHastaCCH').text
                # Periodo
        Periodo = DatosFacturaATR.find('Periodo')
        FechaDesdeFactura = Periodo.find('FechaDesdeFactura').text
        FechaHastaFactura = Periodo.find('FechaHastaFactura').text
        NumeroDias = Periodo.find('NumeroDias').text
        # Potencia
        Potencia = Factura.find('Potencia')
        # EnergiaActiva
        EnergiaActiva = Factura.find('EnergiaActiva')
        # ImpuestoElectrico
        ImpuestoElectrico = Factura.find('ImpuestoElectrico')
        BaseImponible = ImpuestoElectrico.find('BaseImponible').text
        Porcentaje = ImpuestoElectrico.find('Porcentaje').text
        Importe = ImpuestoElectrico.find('Importe').text
        # Alquileres
        Alquileres = Factura.find('Alquileres')
        # IVA
        IVA = Factura.find('IVA')
        # Medidas
        Medidas = Factura.find('Medidas')
        CodPM = Medidas.find('CodPM').text
            # ModeloAparato
        ModeloAparato = Medidas.find('ModeloAparato')
        TipoAparato = ModeloAparato.find('TipoAparato').text
        MarcaAparato = ModeloAparato.find('MarcaAparato').text
        NumeroSerie = ModeloAparato.find('NumeroSerie').text
        TipoDHEdM = ModeloAparato.find('TipoDHEdM').text
                # Integrador
        Integrador = ModeloAparato.find('Integrador')
        Magnitud = Integrador.find('Magnitud').text
        CodigoPeriodo = Integrador.find('CodigoPeriodo').text
        ConstanteMultiplicadora = Integrador.find('ConstanteMultiplicadora').text
        NumeroRuedasEnteras = Integrador.find('NumeroRuedasEnteras').text
        NumeroRuedasDecimales = Integrador.find('NumeroRuedasDecimales').text
        ConsumoCalculado = Integrador.find('ConsumoCalculado').text
                    # LecturaDesde
        LecturaDesde = Integrador.find('LecturaDesde')
        Fecha = LecturaDesde.find('Fecha').text
        Procedencia = LecturaDesde.find('Procedencia').text
        Lectura = LecturaDesde.find('Lectura').text
                    # LecturaHasta
        LecturaHasta = Integrador.find('LecturaHasta')
        Fecha = LecturaHasta.find('Fecha').text
        Procedencia = LecturaHasta.find('Procedencia').text
        Lectura = LecturaHasta.find('Lectura').text
        # --- Crear factura ---
        existing_invoice = self.env['account.invoice'].search([
            ('name', '=', self._get_data(CodigoFiscalFactura)),
            ('state', '=', 'draft'),
        ])
        if len(existing_invoice) > 0:
            existing_invoice.unlink()
        invoice = self.env['account.invoice'].create({
            'name': self._get_data(CodigoFiscalFactura),
            'partner_id': self._get_partner_id(Identificador),
            'date_invoice': self._get_data(FechaFactura),
            'origin': self._get_data(CodContrato),
            'comment': self._get_data(Comentarios),
        })
        invoice._set_line_potencia(Potencia, NumeroDias, IVA)
        invoice._set_line_energia_activa(EnergiaActiva, NumeroDias, IVA)
        invoice._set_line_alquileres(Alquileres, IVA)
        invoice.compute_taxes()
        return invoice

    @api.multi
    def import_zip(self):
        self.ensure_one()
        content = base64.decodestring(self.source_file)
        content = re.sub(' xmlns="[^"]+"', '', content, count=1)
        xml_pdf_msg = ''
        xml_msg = ''
        error_msg = ''
        full_filename = os.path.basename(content)
        filename, file_extension = os.path.splitext(full_filename)
        root = etree.fromstring(content)

        # Cabecera
        Cabecera = root.find('Cabecera')
        CodigoREEEmpresaEmisora = Cabecera.find('CodigoREEEmpresaEmisora').text
        CodigoREEEmpresaDestino = Cabecera.find('CodigoREEEmpresaDestino').text
        CodigoDelProceso = Cabecera.find('CodigoDelProceso').text
        CodigoDePaso = Cabecera.find('CodigoDePaso').text
        CodigoDeSolicitud = Cabecera.find('CodigoDeSolicitud').text
        SecuencialDeSolicitud = Cabecera.find('SecuencialDeSolicitud').text
        FechaSolicitud = Cabecera.find('FechaSolicitud').text
        CUPS = Cabecera.find('CUPS').text

        invoices = self.env['account.invoice']

        # Facturas
        for Factura in root.findall('Facturas'):

            # OtrasFacturas
            for OtraFactura in Factura.findall('OtrasFacturas'):
                other_invoice = self.create_other_invoice(OtraFactura)
                _logger.warning("###### other_invoice: %s" % other_invoice)
                invoices = invoices + other_invoice

            # FacturasATR
            for FacturaATR in Factura.findall('FacturaATR'):
                atr_invoice = self.create_atr_invoice(FacturaATR)
                _logger.warning("###### atr_invoice: %s" % atr_invoice)
                invoices = invoices + atr_invoice

            # RegistroFin
            RegistroFin = Factura.find('RegistroFin')
            ImporteTotal = RegistroFin.find('ImporteTotal').text
            TotalRecibos = RegistroFin.find('TotalRecibos').text
            TipoMoneda = RegistroFin.find('TipoMoneda').text
            FechaValor = RegistroFin.find('FechaValor').text
            FechaLimitePago = RegistroFin.find('FechaLimitePago').text
            IBAN = RegistroFin.find('IBAN').text
            IdRemesa = RegistroFin.find('IdRemesa').text

            _logger.warning("###### invoices: %s" % invoices)
            invoices._set_date_due(FechaLimitePago)

        # OtrosDatosFactura
        OtrosDatosFactura = root.find('OtrosDatosFactura')
        SociedadMercantilEmisora = OtrosDatosFactura.find('SociedadMercantilEmisora').text
        SociedadMercantilDestino = OtrosDatosFactura.find('SociedadMercantilDestino').text
        DireccionEmisora = OtrosDatosFactura.find('DireccionEmisora').text
        DireccionDestino = OtrosDatosFactura.find('DireccionDestino').text

        self.xml_pdf_msg = xml_pdf_msg
        self.xml_msg = xml_msg
        self.error_msg = error_msg
