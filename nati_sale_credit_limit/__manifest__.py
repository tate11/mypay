# -*- coding: utf-8 -*-
{
    'name': "Nati Credit Limit",

    'summary': """
       customer credit limit """,
    'description': """
       customer credit limit 
       """,

    'author': "Mali, MuhlhelITS",
    'website': "http://natigroup.biz",
    'price': 200.00,
    'currency': 'USD',
     'license': 'OPL-1',
    'version': '14.0.0.0',
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    "depends": [
        "account_followup",
        "sale",

    ],
    "data": [
        "views/res_partner_view.xml",
        "views/sale_order_view.xml",
        "wizards/sale_order_warn_wizard_view.xml",
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
}
