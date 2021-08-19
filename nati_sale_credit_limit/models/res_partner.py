from odoo import api, fields, models

from odoo.addons.base.models.res_partner import WARNING_MESSAGE, WARNING_HELP


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _compute_effective_due(self):
        """
        Compute effective due for current partner
        """
        sale_order_obj = self.env["sale.order"]
        for record in self:
            total_due = record.total_due
            orders = sale_order_obj.search(
                [
                    ("partner_id", "=", record.id),
                    ("state", "in", ["sale", "done"]),
                ],
            )
            amount_unpaid_total = 0
            for order in orders:
                posted_invoices = order.mapped("invoice_ids").filtered(lambda inv: inv.state == "posted")
                posted_amount_total = sum(posted_invoices.mapped("amount_total_signed"))
                total = order.amount_total - posted_amount_total
                amount_unpaid_total += total

            record.effective_due = total_due + amount_unpaid_total

    pos_warn = fields.Selection(
        WARNING_MESSAGE,
        "Warnings",
        default="no-message",
        help=WARNING_HELP,
    )
    pos_warn_msg = fields.Text(
        "Message for POS/Sale Order",
    )
    effective_due = fields.Monetary(
        compute="_compute_effective_due",
        compute_sudo=True,
    )

    def check_credit_limit(self, amount_total=0):
        """
        Check credit limit for the current partner
        """
        self.ensure_one()
        amount_total_due = self.effective_due + amount_total
        limit = self.credit_limit
        if amount_total_due > limit:
            res = {
                "type": self.pos_warn or self.sale_warn,
                "message": self.pos_warn_msg or self.sale_warn_msg,
            }
        else:
            res = False
        return res
