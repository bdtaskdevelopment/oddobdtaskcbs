# -*- coding: utf-8 -*-

{
    'name': 'Core Banking System',
    'version': '1.0',
    'summary': 'Core Banking 2',
    'description': 'Core Banking 3',
    'category': 'Banking addons',
    'author': 'Bdtask Limited(A Leading Software Company)',
    'company': 'Bdtask Limited',
    'maintainer': '',
    'depends': ['base', 'account_accountant', 'contacts'],
    'website': 'https://www.bdtask.com/',
    'data': [
    'security/ir.model.access.csv',

    # 'data/demo_data.xml',

    'views/link_account.xml',
    'views/product_service.xml',
    'views/res_partner.xml',
    'views/cbs_bank_account.xml',
    'views/product_type.xml',
    'views/cbs_branch.xml',
    'views/cbs_transaction.xml',
    'views/res_users.xml',
    'views/cbs_transaction_line.xml',
    'views/teller_account.xml',
    'views/cbs_calendar_setup.xml',
    'views/cbs_weekend_setup.xml',
    'views/cbs_holiday_setup.xml',
    'views/day_open_close.xml',

    'views/cbs_menus.xml',
    ],
    
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
