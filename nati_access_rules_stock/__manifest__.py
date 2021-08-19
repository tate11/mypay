# -*- coding: utf-8 -*-
{
    'name': "Nati Stock Access Rules",
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
    'category': 'Inventory',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
