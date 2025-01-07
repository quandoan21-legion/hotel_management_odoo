# -*- coding: utf-8 -*-
# noinspection PyStatementEffect
{
    'name': "Hotel Management",

    'summary': "Manage hotels, rooms, and room descriptions",

    'description': """
        This module allows you to manage hotels, their rooms, and room descriptions.
    """,

    'author': "Your Company",
    'website': "https://www.yourcompany.com",

    'category': 'Management',
    'version': '1.0',

    'depends': ['base'],

    'data': [
        'data/hotel_room_descriptions_data.xml',
        'security/employee.xml',
        'security/manager.xml',
        'security/custom_user.xml',
        'security/ir.model.access.csv',
        'views/hotel_search_views.xml',
        'views/hotel_room_search_views.xml',
        'views/hotel_room_list_views.xml',
        'views/hotel_order_list_views.xml',
        'views/hotel_order_form_views.xml',
        'views/hotel_form_views.xml',
        'views/hotel_list_views.xml',
        'views/hotel_room_form_views.xml',
        'views/menus.xml',
        # 'views/hotel_views.xml',
        # 'views/room_description_views.xml',
    ],

'assets': {
        'web.assets_backend': [
            'hotel/static/css/style.css',  # Add your CSS here
        ],
    },
    'demo': [
        'demo/demo.xml',
    ],
}
