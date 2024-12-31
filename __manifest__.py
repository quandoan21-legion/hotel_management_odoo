# -*- coding: utf-8 -*-
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
        'security/ir.model.access.csv',
        'views/hotel_room_list_views.xml',
        # 'views/hotel_room_form_views.xml',
        'views/hotel_views.xml',
        # 'views/room_description_views.xml',
    ],

    'demo': [
        'demo/demo.xml',
    ],
}