# My Hotel Management

## Overview
My Hotel Management is an Odoo module designed to manage hotel rooms, orders, and descriptions. This module allows you to handle various aspects of hotel management, including room details, customer orders, and room descriptions.

##Folder Structure
```plaintext
hotel/
 ├── __init__.py
 ├── __manifest__.py
 ├── models/
 │   ├── __init__.py
 │   ├── hotel.py
 │   ├── room.py
 │   ├── room_description.py
 │   ├── room_order.py
 ├── views/
 │   ├── hotel_views.xml
 │   ├── room_views.xml
 │   ├── room_description_views.xml
 │   ├── room_order_views.xml
 │   ├── hotel_search_views.xml
 │   ├── hotel_room_search_views.xml
 │   ├── hotel_room_list_views.xml
 │   ├── hotel_order_list_views.xml
 │   ├── hotel_order_form_views.xml
 │   ├── hotel_form_views.xml
 │   ├── hotel_list_views.xml
 │   ├── hotel_room_form_views.xml
 │   ├── menus.xml
 ├── data/
 │   ├── hotel_room_descriptions_data.xml
 ├── security/
 │   ├── ir.model.access.csv
 ├── static/
 │   ├── css/
 │   │   ├── style.css
 ├── demo/
 │   ├── demo.xml
 ├── README.md
```

## __Manifest__.py file 
```
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

```

## Features
- Manage hotel details including name, address, floors, and rooms.
- Manage room details including room ID, bed type, room prize, and status.
- Manage room descriptions with different views.
- Handle room orders with customer details, check-in/check-out dates, and order status.

## Installation
1. Clone the repository into your Odoo addons directory:
    ```bash
    git clone <repository_url> addons/hotel
    ```
2. Update the Odoo module list:
    ```bash
    ./odoo-bin -u all
    ```
3. Install the "My Hotel Management" module from the Odoo apps menu.

## Models
### Hotel
- **name**: Name of the hotel (required)
- **address**: Address of the hotel (required)
- **floors**: Number of floors in the hotel (required)
- **rooms**: Number of rooms in the hotel (required)

### Room
- **hotel_id**: Reference to the hotel (required)
- **hotel_address**: Address of the hotel (related field)
- **roomId**: Room ID (required)
- **bed_type**: Type of bed (single, double, triple) (required)
- **room_prize**: Price of the room (required)
- **room_status**: Status of the room (available, occupied) (required)
- **room_description**: Many-to-many relationship with room descriptions

### Room Description
- **view**: View from the room (sea, city, garden)

### Room Order
- **customer_name**: Name of the customer (required)
- **check_in_date**: Check-in date and time (required)
- **check_out_date**: Check-out date and time (required)
- **room_id**: Reference to the room (required)
- **order_status**: Status of the order (confirmed, new) (required)
- **room_prize**: Price of the room (related field)

## Views
- **Hotel Views**: Form and tree views for managing hotel details.
- **Room Views**: Form and tree views for managing room details.
- **Room Description Views**: Form and tree views for managing room descriptions.
- **Room Order Views**: Form and tree views for managing room orders.

## Usage
1. Navigate to the "Hotel Management" menu in Odoo.
2. Manage hotels, rooms, room descriptions, and room orders using the provided views.

## License
This project is licensed under the MIT License.