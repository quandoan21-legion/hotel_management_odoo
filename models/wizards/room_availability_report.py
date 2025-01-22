from odoo import api, models
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)


class RoomAvailabilityReport(models.AbstractModel):
    _name = 'report.hotel.report_room_availability'
    _description = 'Room Availability Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['room.availability.wizard'].browse(docids)

        # Debug logging
        _logger.critical(f"DocIDs: {docids}")
        _logger.critical(f"Number of docs: {len(docs)}")
        for doc in docs:
            _logger.critical(f"Doc ID: {doc.id}")
            _logger.critical(f"Start Date: {doc.start_date}")
            _logger.critical(f"End Date: {doc.end_date}")
            _logger.critical(f"Available Rooms: {doc.available_room_ids}")

        return {
            'doc_ids': docids,
            'doc_model': 'room.availability.wizard',
            'docs': docs,
            'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'user_login': self.env.user.login,
            'data': data,
        }