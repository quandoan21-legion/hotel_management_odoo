from odoo import fields, models
import logging


_logger = logging.getLogger(__name__)

class RoomAvailabilityWizard(models.TransientModel):
    _name = 'room.availability.wizard'
    _description = 'Room Availability Wizard'

    start_date = fields.Date(string='Start Date', required=True, default=fields.Date.context_today)
    end_date = fields.Date(string='End Date', required=True, default=fields.Date.context_today)
    available_room_ids = fields.Many2many('hotels.room', string='Available Rooms', readonly=True)

    def action_check_availability(self):
        self.ensure_one()
        _logger = logging.getLogger(__name__)

        # Log initial request details
        _logger.info("=" * 50)
        _logger.info("ROOM AVAILABILITY CHECK STARTED")
        _logger.info("=" * 50)
        _logger.info(f"Request initiated by user: {self.env.user.name} (ID: {self.env.user.id})")
        _logger.info(f"Checking availability for date range: {self.start_date} to {self.end_date}")
        _logger.info("-" * 50)

        try:
            # Step 1: Get all rooms
            all_rooms = self.env['hotels.room'].search([])
            _logger.info(f"Total rooms in system: {len(all_rooms)}")
            _logger.info("Room details:")
            for room in all_rooms:
                _logger.info(
                    f"Room ID: {room.id} | Name: {room.name} | Price: {room.room_price}")
            _logger.info("-" * 50)

            # Step 2: Find booked rooms in the date range
            domain = [
                ('check_in_date', '<=', self.end_date),
                ('check_out_date', '>=', self.start_date),
            ]
            _logger.info(f"Searching orders with domain: {domain}")

            booked_orders = self.env['hotels.room.order'].search(domain)
            _logger.info(f"Found {len(booked_orders)} booking orders in the date range")

            # Log booking details
            if booked_orders:
                _logger.info("Booking details found:")
                for order in booked_orders:
                    _logger.info(
                        f"Order ID: {order.id} | "
                        f"Room: {order.room_id.name} | "
                        f"Check-in: {order.check_in_date} | "
                        f"Check-out: {order.check_out_date} | "
                    )
            else:
                _logger.info("No bookings found in the specified date range")
            _logger.info("-" * 50)

            # Step 3: Get booked room IDs
            booked_rooms = booked_orders.mapped('room_id')
            _logger.info(f"Number of booked rooms: {len(booked_rooms)}")
            if booked_rooms:
                _logger.info("Booked room IDs:")
                for room in booked_rooms:
                    _logger.info(f"Room ID: {room.id} | Name: {room.name}")
            _logger.info("-" * 50)

            # Step 4: Calculate available rooms
            available_rooms = all_rooms - booked_rooms
            _logger.info(f"Number of available rooms: {len(available_rooms)}")
            if available_rooms:
                _logger.info("Available room details:")
                for room in available_rooms:
                    _logger.info(
                        f"Room ID: {room.id} | "
                        f"Name: {room.name} | "
                        f"Price: {room.room_price}"
                    )
            else:
                _logger.info("No rooms available for the selected date range")

            # Step 5: Update wizard's available rooms
            self.available_room_ids = [(6, 0, available_rooms.ids)]
            _logger.info(f"Updated wizard (ID: {self.id}) with {len(available_rooms)} available rooms")

            # Final summary
            _logger.info("=" * 50)
            _logger.info("AVAILABILITY CHECK SUMMARY")
            _logger.info(f"Total Rooms: {len(all_rooms)}")
            _logger.info(f"Booked Rooms: {len(booked_rooms)}")
            _logger.info(f"Available Rooms: {len(available_rooms)}")
            _logger.info("=" * 50)

            return self.env.ref('hotel.action_report_room_availability').report_action(self)

        except Exception as e:
            _logger.error("=" * 50)
            _logger.error("ERROR IN AVAILABILITY CHECK")
            _logger.error(f"Error occurred: {str(e)}")
            _logger.error("Traceback:", exc_info=True)
            _logger.error("=" * 50)
            raise