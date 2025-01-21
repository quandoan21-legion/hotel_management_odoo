# controllers/portal.py

from odoo import http
from odoo.http import request
from datetime import datetime, timedelta


class PortalRooms(http.Controller):
    @http.route(['/hotel/rooms', '/hotel/rooms/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_rooms(self, page=1, **kw):
        Room = request.env['hotels.room']
        domain = []
        rooms_count = Room.search_count(domain)
        rooms = Room.search(domain)

        values = {
            'rooms': rooms,
            'rooms_count': rooms_count,
            'page_name': 'rooms',
        }
        return request.render("hotel.portal_rooms_list", values)

    @http.route(['/hotel/rooms/<int:room_id>'], type='http', auth="user", website=True)
    def portal_room_detail(self, room_id, **kw):
        room = request.env['hotels.room'].sudo().browse(room_id)
        if not room.exists():
            return request.redirect('/hotel/rooms')

        # Fetch unavailable dates for the room
        orders = request.env['hotels.room.order'].sudo().search([
            ('room_id', '=', room_id),
            ('order_status', '!=', 'cancelled')
        ])

        unavailable_dates = []
        for order in orders:
            check_in_date = order.check_in_date
            check_out_date = order.check_out_date
            current_date = check_in_date
            while current_date <= check_out_date:
                unavailable_dates.append(current_date.strftime('%Y-%m-%d'))
                current_date += timedelta(days=1)

        values = {
            'room': room,
            'page_name': 'room_detail',
            'datetime': datetime,  # To use in template for date validation
            'unavailable_dates': unavailable_dates,
        }
        return request.render("hotel.portal_room_detail", values)

    @http.route(['/hotel/rooms/book'], type='http', auth="user", website=True, methods=['POST'])
    def book_room(self, **post):
        if not all(post.get(field) for field in ['room_id', 'check_in_date', 'check_out_date']):
            return request.redirect('/hotel/rooms')

        try:
            vals = {
                'room_id': int(post.get('room_id')),
                'customer_name': request.env.user.partner_id.id,
                'check_in_date': post.get('check_in_date'),
                'check_out_date': post.get('check_out_date'),
                'order_status': 'new'
            }
            booking = request.env['hotels.room.order'].sudo().create(vals)
            return request.redirect('/hotel/rooms?message=booking_success')
        except Exception as e:
            return request.redirect(f'/hotel/rooms/{post.get("room_id")}?error=booking_failed')