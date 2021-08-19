# -*- coding: utf-8 -*-
{
    'name': "Nati Register Payment",

    'summary': """
    some times need some one to register payment this user can not access to accountant module ,so this module solve your problem""",

    'description': """
    you can register payment (Receive Money) as temporary from sales man without crate any Journal entry to make more control and Permissions,
    this is not as Outstanding Payments because outstanding payments create journal entry,
    so this is will be more benfit for company which need more control in Receive Money by sales man
    """,

    'author': "Mali, MuhlhelITS",
    'website': "http://natigroup.biz",
    'price': 400.00,
    'currency': 'USD',
     'license': 'OPL-1',
    'version': '14.0.0.0',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting/Accounting',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'sale', 'sales_team', 'nati_reports_base_style'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/nati_payment_security.xml',
        'views/main_inherit.xml',
        'views/report_register_payment_customer.xml',
        'views/report_register_payment_dealer.xml',
        'views/register_payment_view.xml',
        'views/account_payment_view.xml',
        'wizard/nati_account_payment_register_views.xml',

    ],

    'images': ['static/description/banner.png'],
    'installable': True,
}
