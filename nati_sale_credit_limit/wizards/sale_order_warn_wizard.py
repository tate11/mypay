from odoo import fields, models


class SaleOrderWarnWizard(models.TransientModel):
    _name = "sale.order.warn.wizard"
    _description = "Sale Order Warning"

    warning_message = fields.Text()
    sale_order_id = fields.Many2one("sale.order")

    def action_confirm(self):
        """
        Action confirm warning.
        Call `Confirm Order` method for Sale order
        """
        self.ensure_one()
        return self.sale_order_id.with_context({"force_confirm": True}).action_confirm()
