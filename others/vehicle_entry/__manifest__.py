# -*- coding: utf-8 -*-
{
    'name': "Vehicle Entry",

    'summary': """
        This module is for the generation of token""",

    'description': """
        Module that track the record of vehicle enter. Generates the token for the turn.
    """,

    'author': "BI Solutions",
    'website': "www.bisolutions.asia",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management', 'contacts', 'mail'],

    # always loaded
    'data': [
        'reports/paper_format.xml',
        'security/user_groups.xml',
        'security/ir.model.access.csv',  
	    'views/contact_ext_views.xml',    
        'views/views.xml',
        'views/res_config_setting_view.xml',
        # 'views/templates.xml',
        # 'views/web_asset_backend_template.xml',
        'data/entry_data.xml',
        'reports/print_token.xml',
        
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],

    'qweb': [
        "static/src/xml/vehicle_entry.xml",
    ],
}
