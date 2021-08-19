from odoo import api, fields, models

from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    ignore_credit_limit_checking = fields.Boolean(
        default=False,
    )
    warning_type = fields.Selection(
        related="partner_id.pos_warn",
        readonly=True,
    )

    def action_confirm(self):
        """
        Overwrite core method to set check credit limit
        """
        self.ensure_one()
        warning = self.partner_id.check_credit_limit(self.amount_total)
        force_confirm = self.env.context.get("force_confirm")
        if warning and not force_confirm:
            message = warning.get("message")
            warn_type = warning.get("type")
            if warn_type == "block":
                raise UserError(message)
            elif warn_type == "warning":
                context = self.env.context.copy()
                context.update({
                    "default_sale_order_id": self.id,
                    "default_warning_message": message,
                })
                form_id = self.env.ref("cx_sale_credit_limit.sale_order_warn_wizard_view_form").id
                return {
                    "name": "Credit Limit Warning",
                    "res_model": "sale.order.warn.wizard",
                    "view_type": "form",
                    "view_mode": "form",
                    "views": [(form_id, "form")],
                    "view_id": form_id,
                    "type": "ir.actions.act_window",
                    "target": "new",
                    "context": context,
                }

        return super(SaleOrder, self).action_confirm()

    def write(self, vals):
        """
        Overwrite core method to check credit limit
        """
        res = super(SaleOrder, self).write(vals)
        if self.state == "sale" and vals.get("order_line"):
            warning = self.partner_id.check_credit_limit()
            if warning:
                message = warning.get("message")
                warn_type = warning.get("type")
                ignore_credit_limit_checking = self.ignore_credit_limit_checking or vals.get("ignore_credit_limit_checking")
                if warn_type == "block":
                    raise UserError(message)
                elif warn_type == "warning" and not ignore_credit_limit_checking:
                    raise UserError(message)
        return res
