# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _


class GeneralLedgerReportMoveLine(models.TransientModel):

    _inherit = 'report_general_ledger_qweb_move_line'

    # Adding Data fields, used for report display
    doc = fields.Char()


class GeneralLedgerReportCompute(models.TransientModel):

    _inherit = 'report_general_ledger_qweb'

    @api.multi
    def print_report(self, report_type):
        self.ensure_one()
        if report_type == 'xlsx':
            report_name = 'ener_account_ext.' \
                          'report_general_ledger_xlsx'
        else:
            report_name = 'account_financial_report_qweb.' \
                          'report_general_ledger_qweb'
        return self.env['report'].get_action(docids=self.ids,
                                             report_name=report_name)

    def _inject_line_not_centralized_values(
            self,
            is_account_line=True,
            is_partner_line=False,
            only_empty_partner_line=False,
            only_unaffected_earnings_account=False):
            """ Inject report values for report_general_ledger_qweb_move_line.

            If centralized option have been chosen,
            only non centralized accounts are computed.

            In function of `is_account_line` and `is_partner_line` values,
            the move_line link is made either with account or either with partner.

            The "only_empty_partner_line" value is used
            to compute data without partner.
            """
            query_inject_move_line = """
    INSERT INTO
        report_general_ledger_qweb_move_line
        (
            """
            if is_account_line:
                query_inject_move_line += """
        report_account_id,
                """
            elif is_partner_line:
                query_inject_move_line += """
        report_partner_id,
                """
            query_inject_move_line += """
        create_uid,
        create_date,
        move_line_id,
        date,
        entry,
        journal,
        account,
        doc,
        taxes_description,
        partner,
        label,
        cost_center,
        matching_number,
        debit,
        credit,
        cumul_balance,
        currency_id,
        amount_currency
        )
    SELECT
            """
            if is_account_line:
                query_inject_move_line += """
        ra.id AS report_account_id,
                """
            elif is_partner_line:
                query_inject_move_line += """
        rp.id AS report_partner_id,
                """
            query_inject_move_line += """
        %s AS create_uid,
        NOW() AS create_date,
        ml.id AS move_line_id,
        ml.date,
        m.name AS entry,
        j.code AS journal,
        a.code AS account,
        m.doc AS doc,
        CASE
            WHEN
                ml.tax_line_id is not null
            THEN
                COALESCE(at.description, at.name)
            WHEN
                ml.tax_line_id is null
            THEN
                (SELECT
                    array_to_string(
                        array_agg(COALESCE(at.description, at.name)
                    ), ', ')
                FROM
                    account_move_line_account_tax_rel aml_at_rel
                LEFT JOIN
                    account_tax at on (at.id = aml_at_rel.account_tax_id)
                WHERE
                    aml_at_rel.account_move_line_id = ml.id)
            ELSE
                ''
        END as taxes_description,
            """
            if not only_empty_partner_line:
                query_inject_move_line += """
        CASE
            WHEN
                NULLIF(p.name, '') IS NOT NULL
                AND NULLIF(p.ref, '') IS NOT NULL
            THEN p.name || ' (' || p.ref || ')'
            ELSE p.name
        END AS partner,
                """
            elif only_empty_partner_line:
                query_inject_move_line += """
        '""" + _('No partner allocated') + """' AS partner,
                """
            query_inject_move_line += """
        CONCAT_WS(' - ', NULLIF(ml.ref, ''), NULLIF(ml.name, '')) AS label,
        aa.name AS cost_center,
        fr.name AS matching_number,
        ml.debit,
        ml.credit,
            """
            if is_account_line:
                query_inject_move_line += """
        ra.initial_balance + (
            SUM(ml.balance)
            OVER (PARTITION BY a.code
                ORDER BY a.code, ml.date, ml.id)
        ) AS cumul_balance,
                """
            elif is_partner_line and not only_empty_partner_line:
                query_inject_move_line += """
        rp.initial_balance + (
            SUM(ml.balance)
            OVER (PARTITION BY a.code, p.name
                ORDER BY a.code, p.name, ml.date, ml.id)
        ) AS cumul_balance,
                """
            elif is_partner_line and only_empty_partner_line:
                query_inject_move_line += """
        rp.initial_balance + (
            SUM(ml.balance)
            OVER (PARTITION BY a.code
                ORDER BY a.code, ml.date, ml.id)
        ) AS cumul_balance,
                """
            query_inject_move_line += """
        c.id AS currency_id,
        ml.amount_currency
    FROM
            """
            if is_account_line:
                query_inject_move_line += """
        report_general_ledger_qweb_account ra
                """
            elif is_partner_line:
                query_inject_move_line += """
        report_general_ledger_qweb_partner rp
    INNER JOIN
        report_general_ledger_qweb_account ra ON rp.report_account_id = ra.id
                """
            query_inject_move_line += """
    INNER JOIN
        account_move_line ml ON ra.account_id = ml.account_id
    INNER JOIN
        account_move m ON ml.move_id = m.id
    INNER JOIN
        account_journal j ON ml.journal_id = j.id
    INNER JOIN
        account_account a ON ml.account_id = a.id
    LEFT JOIN
        account_tax at ON ml.tax_line_id = at.id
            """
            if is_account_line:
                query_inject_move_line += """
    LEFT JOIN
        res_partner p ON ml.partner_id = p.id
                """
            elif is_partner_line and not only_empty_partner_line:
                query_inject_move_line += """
    INNER JOIN
        res_partner p
            ON ml.partner_id = p.id AND rp.partner_id = p.id
                """
            query_inject_move_line += """
    LEFT JOIN
        account_full_reconcile fr ON ml.full_reconcile_id = fr.id
    LEFT JOIN
        res_currency c ON ml.currency_id = c.id
                        """
            if self.filter_cost_center_ids:
                query_inject_move_line += """
    INNER JOIN
        account_analytic_account aa
            ON
                ml.analytic_account_id = aa.id
                AND aa.id IN %s
                """
            else:
                query_inject_move_line += """
    LEFT JOIN
        account_analytic_account aa ON ml.analytic_account_id = aa.id
                """
            query_inject_move_line += """
    WHERE
        ra.report_id = %s
    AND
            """
            if only_unaffected_earnings_account:
                query_inject_move_line += """
        a.id = %s
    AND
                """
            if is_account_line:
                query_inject_move_line += """
        (ra.is_partner_account IS NULL OR ra.is_partner_account != TRUE)
                """
            elif is_partner_line:
                query_inject_move_line += """
        ra.is_partner_account = TRUE
                """
            if self.centralize:
                query_inject_move_line += """
    AND
        (a.centralized IS NULL OR a.centralized != TRUE)
                """
            query_inject_move_line += """
    AND
        ml.date BETWEEN %s AND %s
            """
            if self.only_posted_moves:
                query_inject_move_line += """
    AND
        m.state = 'posted'
            """
            if only_empty_partner_line:
                query_inject_move_line += """
    AND
        ml.partner_id IS NULL
    AND
        rp.partner_id IS NULL
            """
            if self.filter_journal_ids:
                query_inject_move_line += """
    AND
        j.id IN %s
                """
            if is_account_line:
                query_inject_move_line += """
    ORDER BY
        a.code, ml.date, ml.id
                """
            elif is_partner_line and not only_empty_partner_line:
                query_inject_move_line += """
    ORDER BY
        a.code, p.name, ml.date, ml.id
                """
            elif is_partner_line and only_empty_partner_line:
                query_inject_move_line += """
    ORDER BY
        a.code, ml.date, ml.id
                """

            query_inject_move_line_params = (
                self.env.uid,
            )
            if self.filter_cost_center_ids:
                query_inject_move_line_params += (
                    tuple(self.filter_cost_center_ids.ids),
                )
            query_inject_move_line_params += (
                self.id,
            )
            if only_unaffected_earnings_account:
                query_inject_move_line_params += (
                    self.unaffected_earnings_account.id,
                )
            query_inject_move_line_params += (
                self.date_from,
                self.date_to,
            )
            if self.filter_journal_ids:
                query_inject_move_line_params += (tuple(
                    self.filter_journal_ids.ids,
                ),)
            self.env.cr.execute(
                query_inject_move_line,
                query_inject_move_line_params
            )