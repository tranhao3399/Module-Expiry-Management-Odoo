{
    'name': 'Expiry Management',
    'version': '1.0',
    'summary': 'Expiry Management',
    'description': 'Quản lý lô sản phẩm hết hạn',
    'category': 'Other',
    'author': 'Tran Hao',
    'depends': ['stock', 'product_expiry', 'mail'],
    'data': ['views/expiryproduct_view.xml',
             'data/email_template.xml',
             'reports/expiry_report_views.xml',
             ],
    'icon': '/expiry_management/static/description/icon.jpg',
    'installable': True,
    'auto_install': False,
    'application': True
}
