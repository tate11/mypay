# -*- coding: utf-8 -*-
{
    'name': "Nati Filter Date",

    'summary': """
   Nati Filter """,
    'description': """
   Nati Filter 
   """,

    'author': "Mali, MuhlhelITS",
    'website': "http://natigroup.biz",
    'price': 100.00,
    'currency': 'USD',
    'license': 'OPL-1',
    'version': '14.0.0.0',
    'category': 'Tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','account','purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,

}
