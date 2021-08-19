# -*- coding: utf-8 -*-
{
    'name': "Nati Interface",


    'summary': """
 Inter face color and some icon""",

    'description': """
 """,

    'author': "Mali, MuhlhelITS",
    'website': "http://natigroup.biz",
    'license': 'AGPL-3',
    'version': '14.0.0.0',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Services',
    # any module necessary for this one to work correctly
    'depends': ['web_enterprise'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/linkestatic.xml',
    ],

    'images': ['static/description/banner.png'],
    'installable': True,

}
