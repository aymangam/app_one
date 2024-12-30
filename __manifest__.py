# -*- coding: utf-8 -*-
{
    'name': "App one",
    'license': 'LGPL-3',
    'application': True,
    'sequence':1,
    'summary': "Short (1 phrase/line) summary of the module's purpose",
    'author': "Ayman Gamal",
    'category': 'Uncategorized',
    'version': '17.0.0.1.0',
    'depends': ['base', 'sale_management', 'account', 'mail', 'contacts'],
    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/base_menu.xml',
        'views/property_views.xml',
        'views/owner_views.xml',
        'views/tag_views.xml',
        'views/sale_order_views.xml',
        'views/res_partner_view.xml',
        'views/building_view.xml',
        'views/property_history_views.xml',
        'views/account_move_views.xml',
        'wizard/change_state_wizard_view.xml',
        'reports/property_report.xml',
    ],
    'assets': {
        'web.assets_backend': ['app_one/static/src/css/property.css'],
        'web.report_assets_common': ['app_one/static/src/css/font.css']
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

