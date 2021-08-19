# -*- coding: utf-8 -*-
import odoo
from odoo import models, fields, api,_
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
from datetime import datetime


class RegisterPayment(models.Model):
   _name = 'nati_register_payment.payment'
   #_inherit = ['mail.thread', 'mail.activity.mixin']
   _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
   _order = "date desc, name desc"

   state = fields.Selection(selection=[
       ('draft', 'Draft'),
       ('confirmed', 'Confirmed'),
       ('printed', 'Printed'),
       ('posted', 'Posted'),
       ('cancelled', 'Cancelled'),
   ], string='Status', required=True, readonly=True, copy=False, tracking=True,
       default='draft')

   name = fields.Char(string="Payment Number", readonly=True, required=True, copy=False, default='Draft')
   user_id = fields.Many2one(
       'res.users', string='Salesperson', index=True, tracking=2, default=lambda self: self.env.user, readonly=True,
       domain=lambda self: [('groups_id', 'in', self.env.ref('sales_team.group_sale_salesman').id)])
   date = fields.Date(
       string='Date',
       required=True,
       index=True,
       readonly=False,
       copy=False,
       default=fields.Date.context_today
   )
   # == Synchronized fields with the account.move.lines ==

   currency_id = fields.Many2one('res.currency', string='Currency', store=True, readonly=False,
                                 compute='_compute_currency_id',
                                 help="The payment's currency.")
   amount = fields.Monetary(
       currency_field='currency_id',
       required=True, readonly=False,
   )
   num_word = fields.Char(string=_("Amount In Words:"), compute='_compute_amount_in_word')

   ref = fields.Char(string='Reference', copy=False, tracking=True)
   partner_id = fields.Many2one(
        comodel_name='res.partner', required=True,
        string="Customer",
        store=True, readonly=False, ondelete='restrict',
        domain="['|', ('parent_id','=', False), ('is_company','=', True)]",
        check_company=True)

   payment_method  = fields.Selection([
        ('cash', 'Cash'),
        ('bank', 'Bank'),
        ('pos', 'POS'),
        ('gateway', 'Payment Gateway'),
   ], string='Payment Method', default='cash', required=True)
   posno = fields.Char(string='POS NO')

   journal_id = fields.Many2one('account.journal', store=True, readonly=False,
                                domain="[('company_id', '=', company_id), ('type', 'in', ('bank', 'cash'))]")
   payment_id = fields.Many2one(
       comodel_name='account.payment',
       string='Receive Payment', readonly=True, ondelete='cascade',
       check_company=True)

   _sql_constraints = [
    (
        'check_amount_not_negative',
        'CHECK(amount >= 0.0)',
        "The payment amount cannot be negative.",
    ),
    ]
   @api.onchange('payment_method')
   def _update_journal_id(self):
       for pay in self:
           domain = None
           if pay.payment_method == 'cash':
               domain = [
                   ('type', '=', 'cash'),
                   ('company_id', '=', pay.user_id.company_id.id),
               ]
           else:
               domain = [
                   ('type', '=', 'bank'),
                   ('company_id', '=', pay.user_id.company_id.id),
               ]
           if not domain:
               domain = [
                   ('type', '=', 'cash'),
                   ('company_id', '=', pay.user_id.company_id.id),
               ]
           journal = None
           if pay.currency_id:
               journal = self.env['account.journal'].search(
                   domain + [('currency_id', '=', pay.currency_id.id)], limit=1).filtered(lambda jr: jr.type == "cash")
           if not journal:
               journal = self.env['account.journal'].search(domain, limit=1)

           pay.journal_id = journal


   def _compute_amount_in_word(self):
       for rec in self:
           rec.num_word = str(rec.currency_id.amount_to_text(rec.amount))

   @api.depends('user_id')
   def _compute_currency_id(self):
       for pay in self:
           pay.currency_id = pay.user_id.currency_id or pay.user_id.company_id.currency_id

   def action_register_payment(self):
       ''' Open the account.payment.register wizard to pay the selected journal entries.
       :return: An action opening the account.payment.register wizard.
       '''
       comm = self.name
       comm += '-' + self.payment_method
       if self.posno:
           comm += '-' + self.posno
       if self.ref:
           comm += '-' + self.ref


       return {
           'name': _('Register Payment'),
           'res_model': 'nati_register_payment.payment.register',
           'view_mode': 'form',
           'context': {
               'active_model': 'nati_register_payment.payment',
               'active_ids': self.ids,
               'id': self.id,
               'partner_id': self.partner_id.id,
               'journal_id': self.journal_id.id,
               'amount': self.amount,
               'name': self.name,
               'ref': comm,
               'date': self.date,
           },
           'target': 'new',
           'type': 'ir.actions.act_window',
       }

   def action_post(self):
        ''' confirmed -> posted (in wizard)'''
        # self.write({'state': 'posted'})
        return self.action_register_payment()

   def action_confirm(self):
       ''' draft -> confirmed '''
       if self.name == 'Draft':
           self.name = self.env['ir.sequence'].next_by_code('register.payment') or 'Draft'
       self.write({'state': 'confirmed'})

   def action_print_customer(self):
       return self.env.ref('nati_register_payment.action_register_payment_slip_customer').report_action(self)

   def action_print_dealer(self):
       return self.env.ref('nati_register_payment.action_register_payment_slip_dealer').report_action(self)

   def action_print(self):
       ''' confirmed -> printed '''
       self.write({'state': 'printed'})
       printc = self.action_print_customer()
       printd = self.action_print_dealer()
       return printc

   def action_cancel(self):
        ''' draft -> cancelled '''
        self.write({'state': 'cancelled'})

   def action_draft(self):
        ''' posted -> draft '''
        self.write({'state': 'draft'})
