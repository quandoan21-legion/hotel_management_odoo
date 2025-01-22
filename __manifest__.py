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

    'depends': ['base', 'hr'],

    'data': [
        'data/hotel_room_descriptions_data.xml',
        'security/employee.xml',
        'security/manager.xml',
        'security/admin.xml',
        'security/ir.model.access.csv',
        'views/rooms/report/room_availability_wizard_view.xml',
        'views/rooms/report/room_availability_report_template.xml',
        'views/rooms/portal/room_template.xml',
        'views/rooms/portal/room_detail_template.xml',
        'views/room_orders/server_action/hotel_order_server_action.xml',
        'views/hotels/search/hotel_search_views.xml',
        'views/rooms/search/hotel_room_search_views.xml',
        'views/rooms/list/hotel_room_list_views.xml',
        'views/room_orders/search/hotel_order_search_views.xml',
        'views/room_orders/list/hotel_order_list_views_filtered.xml',
        'views/room_orders/form/hotel_order_form_views.xml',
        'views/hotels/form/hotel_form_views.xml',
        'views/hotels/list/hotel_list_views.xml',
        'views/rooms/form/hotel_room_form_views.xml',
        'views/room_descriptions/room_descriptions_list_view.xml',
        'views/notification/notify.xml',
        'views/room_orders/form/room_payment_wizard_form.xml',
        'views/room_orders/window_action/hotel_order_action_window.xml',
        'views/rooms/cron/cron_check_last_time_room_rent.xml',
        'views/menus.xml',
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
