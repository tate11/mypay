# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountPaymentRegister(models.TransientModel):
    _name = 'nati_register_payment.payment.register'
    _description = 'Register Payment'

    # == Business fields ==
    payment_date = fields.Date(string="Payment Date", required=True,
                               default=fields.Date.context_today)
    amount = fields.Monetary(currency_field='currency_id', store=True, readonly=False,
                             compute='_compute_amount')
    communication = fields.Char(string="Memo", store=True, readonly=False,
                                compute='_compute_communication')
    currency_id = fields.Many2one('res.currency', string='Currency', store=True, readonly=False,
                                  compute='_compute_currency_id',
                                  help="The payment's currency.")
    journal_id = fields.Many2one('account.journal', store=True, readonly=False,
                                 compute='_compute_journal_id',
                                 domain="[('company_id', '=', company_id), ('type', 'in', ('bank', 'cash'))]")

    partner_id = fields.Many2one('res.partner',
                                 string="Customer", store=True, copy=False, readonly=False, ondelete='restrict',
                                 compute='_compute_partner_id')

    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 compute='_compute_company_id')

    payment_type = fields.Selection([
        ('outbound', 'Send Money'),
        ('inbound', 'Receive Money'),
    ], string='Payment Type', store=True, copy=False,
        default='inbound')
    partner_type = fields.Selection([
        ('customer', 'Customer'),
        ('supplier', 'Vendor'),
    ], store=True, copy=False,
        default='customer')
    paymentreg_id = fields.Many2one(
        comodel_name='nati_register_payment.payment', compute='_compute_paymentreg_id',
        string='Register Payment', required=True, readonly=True, ondelete='cascade',
        check_company=True)


    # -------------------------------------------------------------------------
    # Muhlhel Compute
    # -------------------------------------------------------------------------
    @api.depends('currency_id')
    def _compute_company_id(self):
        for wizard in self:
            wizard.company_id = wizard.journal_id.company_id

    @api.depends('company_id', 'currency_id')
    def _compute_partner_id(self):
        for wizard in self:
            wizard.partner_id = self._context.get('partner_id')

    @api.depends('company_id', 'currency_id')
    def _compute_journal_id(self):
        for wizard in self:
            wizard.journal_id = self._context.get('journal_id')

    @api.depends('company_id', 'currency_id', 'payment_date')
    def _compute_amount(self):
        for wizard in self:
                wizard.amount = self._context.get('amount')

    @api.depends('company_id')
    def _compute_communication(self):
        for wizard in self:
            wizard.communication = self._context.get('ref')

    @api.depends('journal_id')
    def _compute_currency_id(self):
        for wizard in self:
            wizard.currency_id = wizard.journal_id.currency_id  or wizard.company_id.currency_id

    @api.depends('company_id')
    def _compute_paymentreg_id(self):
        for wizard in self:
            wizard.paymentreg_id = self._context.get('id')


    def _create_payment_vals_from_wizard(self):
        payment_vals = {
            'date': self.payment_date,
            'amount': self.amount,
            'payment_type': self.payment_type,
            'partner_type': self.partner_type,
            'ref': self.communication,
            'journal_id': self.journal_id.id,
            'currency_id': self.currency_id.id,
            'partner_id': self.partner_id.id,
            'paymentreg_id': self.paymentreg_id.id,

        }

        return payment_vals


    def _create_payments(self):
        self.ensure_one()

        payment_vals = self._create_payment_vals_from_wizard()
        payment_vals_list = [payment_vals]
        payments = self.env['account.payment'].create(payment_vals_list)
        payments.action_post()
        return payments

    def action_create_payments(self):
        payments = self._create_payments()

        if self._context.get('dont_redirect_to_payments'):
            return True

        action = {
            'name': _('Payments'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.payment',
            'context': {'create': False},
        }
        if len(payments) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': payments.id,
            })
        else:
            action.update({
                'view_mode': 'tree,form',
                'domain': [('id', 'in', payments.ids)],
            })
        self.paymentreg_id.write({'state': 'posted'})
        self.paymentreg_id.write({'payment_id': payments.id})
        return action
