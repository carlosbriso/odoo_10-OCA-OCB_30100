# -*- coding: utf-8 -*-
################################################################
#    License, author and contributors information in:          #
#    __openerp__.py file at the root folder of this module.    #
################################################################

# XML MANAGEMENT
from lxml import etree
from lxml.etree import Element as ET
from lxml.etree import SubElement as SE

import base64
import magic
import csv
from zipfile import ZipFile
from cStringIO import StringIO
import codecs

from openerp import models, fields, api, _
from openerp.exceptions import Warning
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)


class AccountInvoiceImportWizard(models.TransientModel):
    _name = 'account.invoice.import.wizard'

    name = fields.Char(
        string='File name',
    )

    file = fields.Binary(
        string='ZIP file to import to Odoo',
        required=True,
    )

    msg = fields.Char(
        string='Created pickings',
        readonly=True,
    )

    @api.multi
    def import_invoices(self):
        self.ensure_one()

        content = base64.decodestring(self.file)  # en content hay datos binarios
        content = content.decode('latin1').encode('utf-8')  # convert content from latin1 to utf-8
        # _logger.warning(content.decode('latin1').encode('utf-8').decode('utf-8'))

        # if codecs.BOM_UTF8 == content[:3]:  # para eliminar el "byte order mark" si lo hubiera
        #     content = content[3:]

        file_type = magic.from_buffer(content, mime=True)
        self.msg = 0  # reinicialización del mensaje

        """ IMPORTACION DE CSV (en texto plano) """

        if file_type == 'text/plain':
            self._create_invoices_from_csv(content)
            return self._show_result_wizard()

        """ IMPORTACION DE FICHEROS ZIP """

        if file_type == 'application/zip':
            try:
                zip_file = ZipFile(StringIO(content))
            except Exception:
                raise Warning(_('Make sure that the ZIP is the format of the file'))
            for file_name in zip_file.namelist():
                if not file_name.endswith('.csv'):
                    raise Warning(_('There should be only CSV files in the ZIP file'))
                file_content = zip_file.read(file_name)
                if not file_content:
                    raise Warning(_('CSV with wrong data: %s') % file_name)
                self._generate_picking_from_xml(file_content, file_name)
            return self._show_result_wizard()
        raise Warning(
            _('WRONG FILETYPE'),
            _('You should upload a zip, or csv file')
        )

    def _show_result_wizard(self):
        # if self.msg:
        #     self.msg = self.msg[:-2]  # para eliminar la coma final
        self = self.with_context(default_msg=str(self.msg))
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': self.env.context,
        }

    def _create_invoices_from_csv(self, data):
        try:
            reader = csv.DictReader(StringIO(data), delimiter=';')
        except Exception:
            raise Warning(
                _('ERROR getting data from csv file'),
                _('There was some error trying to get the data from the csv file.'
                  'Make sure you are using the right format: plain CSV with ";" as delimiter')
            )
        n = 1
        for row in reader:
            _logger.warning('>> IMPORTING INVOICE: {}'.format(n))
            n += 1

            """ VALIDACIÓN CAMPOS """

            if n == 2:
                csv_fields = [
                    'DTB_CIF', 'FACT_NUMSERIE', 'FACT_EMISION', 'FACT_TIPO', 'RECTIF_TIPO',
                    'RECTIF_NUMSERIE', 'RECTIF_EMISION', 'RECTIF_BI', 'RECTIF_IVA', 'FACT_TOTAL',
                    'DESCR_OPERACION', 'CLIE_NOMBRE', 'CLIE_TIPOIDFISCAL', 'CLIE_IDFISCAL',
                    'FACT_TIPONOEXENTA', 'DCHO_EXTENSION', 'DCHO_ACCESO', 'DCHO_ENGANCHE',
                    'DCHO_VERIFICACION', 'DCHO_ACTUACIONEQUIPO', 'DCHO_CESIONLINEA', 'DCHO_CESIONCT',
                    'FIANZA', 'FACT_ALQUILER', 'FACT_ISE', 'FACT_TIPOIVA', 'FACT_BASEISE',
                    'FACT_BLIQUIDABLE', 'FACT_BI', 'FACT_IVA', 'PAGADOR', 'CIF_PAGADOR', 'TIPO_CONTRATO'
                ]

                for key in row:
                    if key not in csv_fields:
                        raise Warning(  # este error podría salir por más que estos motivos. Por problemas de codificación también sale
                            _(
                                "ERROR Validating data. Verify the columns header names:\n"
                                "'DTB_CIF', 'FACT_NUMSERIE', 'FACT_EMISION', 'FACT_TIPO', 'RECTIF_TIPO',"
                                "'RECTIF_NUMSERIE', 'RECTIF_EMISION', 'RECTIF_BI', 'RECTIF_IVA', 'FACT_TOTAL',"
                                "'DESCR_OPERACION', 'CLIE_NOMBRE', 'CLIE_TIPOIDFISCAL', 'CLIE_IDFISCAL',"
                                "'FACT_TIPONOEXENTA', 'DCHO_EXTENSION', 'DCHO_ACCESO', 'DCHO_ENGANCHE',"
                                "'DCHO_VERIFICACION', 'DCHO_ACTUACIONEQUIPO', 'DCHO_CESIONLINEA', 'DCHO_CESIONCT',"
                                "'FIANZA', 'FACT_ALQUILER', 'FACT_ISE', 'FACT_TIPOIVA', 'FACT_BASEISE',"
                                "'FACT_BLIQUIDABLE', 'FACT_BI', 'FACT_IVA', 'PAGADOR', 'CIF_PAGADOR', 'TIPO_CONTRATO'"
                            )
                        )

            # DESCR_OPERACION    > product_id
            # CLIE_IDFISCAL      > NIF cliente, debería existir
            # FACT_EMISION       > fecha
            # FACT_TOTAL         > total factura
            # Impuestos          > se coge el del producto
            # Subtotal de linea  > que coincidira con el FACT_TOTAL??

            ''' FACTURA '''

            partner_id = self._get_partner_id(n, row)
            virt_inv = self.env['account.invoice'].new({
                'partner_id': partner_id.id,
                'type': 'out_invoice',   # by default
                'date_invoice': self._get_date_invoice(n, row),
            })
            virt_inv._onchange_partner_id()
            inv_vals = virt_inv._convert_to_write(virt_inv._cache)
            number = row.get('FACT_NUMSERIE', False) if row.get('FACT_NUMSERIE', False) != '' else False
            if number:
                inv_vals.update({
                    'invoice_number': number
                })
            try:
                invoice = self.env['account.invoice'].create(inv_vals)
                self.msg = int(self.msg) + 1
            except Exception, e:
                raise Warning(
                    _('ERROR creating invoice'
                      '\nROW: %s'
                      '\nError message: %s') % (n, e.message)
                )

            ''' LINEA DE FACTURA '''

            product_id = self._get_product_id(n, row)
            iva = product_id.taxes_id.amount / 100
            virt_inv_line_id = self.env['account.invoice.line'].new({
                'product_id': product_id.id,
                'invoice_id': invoice.id
            })
            virt_inv_line_id._onchange_product_id()
            inv_line_vals = virt_inv_line_id._convert_to_write(virt_inv_line_id._cache)
            inv_line_vals.update({
                'price_unit': self._get_price_unit(n, row, iva),
            })

            try:
                invoice.write({
                    'invoice_line_ids': [(0, 0, inv_line_vals)]
                })
                invoice._onchange_invoice_line_ids()
            except Exception, e:
                raise Warning(
                    _('ERROR updating invoice lines'
                      '\nROW: %s'
                      '\nError message: %s') % (n, e.message)
                    )

    def _get_price_unit(self, n, row, iva):
        total = row.get('FACT_TOTAL', False) if row.get('FACT_TOTAL', False) != '' else False
        if not total:
            raise Warning(
                _('VALIDATION ERROR\nThe "FACT_TOTAL" field is required.'
                  '\nROW: %s') % n
            )
        try:
            total = float(total)
        except Exception:
            raise Warning(
                _('VALIDATION ERROR\nThe "FACT_TOTAL" cannot be converted to float value.'
                    '\nROW: %s') % n)
        price_unit = (1 + iva) / total
        return price_unit

    def _get_date_invoice(self, n, row):
        date_invoice = row.get('FACT_EMISION', False) if row.get('FACT_EMISION', False) != '' else False
        if not date_invoice:
            date_invoice = datetime.now().date()
        else:
            try:
                date_invoice = datetime.strptime(date_invoice, "%d/%m/%Y")
            except Exception:
                raise Warning(
                    _('VALIDATION ERROR\nThe "FACT_EMISION" has an incorrect format.'
                      ' The format must be "dd/mm/YYYY"'
                      '\nROW: %s') % n)

        return date_invoice

    def _get_partner_id(self, n, row):
        vat = 'ES{}'.format(row.get('CLIE_IDFISCAL', False))
        if vat == 'ES':
            raise Warning(
                _('VALIDATION ERROR'
                  '\nThe VAT field must be filled'
                  '\nROW: %s') % n
            )
        partner_id = self.env['res.partner'].search([
            ('vat', '=ilike', vat),
            ('parent_id', '=', False),
        ])
        if len(partner_id) > 1:
            raise Warning(
                _('VALIDATION ERROR'
                  '\nMore than one partner with the same NIF'
                  '\nROW: %s | PARTNERS: %s') % (n, ', '.join(partner_id.mapped('name')))
            )
        elif len(partner_id) == 0:
            raise Warning(
                _('VALIDATION ERROR'
                  '\nThe customer name was not found in the database'
                  '\nROW: %s') % n
            )
        return partner_id

    def _get_product_id(self, n, row):
        product_name = row.get('DESCR_OPERACION', False)
        product = self.env['product.product'].search(
            [('name', '=ilike', product_name)]
        )
        if len(product) == 1:
            return product
        elif len(product) > 1:
            raise Warning(
                _('ERROR'
                  '\nMore than one product with the same name'  # deberia haber restriccion, pero daba problemas al importar
                  '\nROW: %s') % n)
        else:
            raise Warning(
                _('ERROR: The product name was not found in the database'
                  '\nROW: %s') % n)
