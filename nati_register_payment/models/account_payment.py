# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class AccPaymentReg(models.Model):
    _inherit = 'account.payment'

    paymentreg_id = fields.Many2one(
        comodel_name='nati_register_payment.payment',
        string='Register Payment', readonly=True, ondelete='cascade',
        check_company=True)