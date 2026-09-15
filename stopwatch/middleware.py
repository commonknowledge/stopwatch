import logging
import time
from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from stopwatch.models.core import MailHeartbeat

logger = logging.getLogger(__name__)

HEARTBEAT_INTERVAL = timedelta(days=7)
# How often each worker process checks the database (seconds).
CHECK_INTERVAL = 60 * 60


class MailHeartbeatMiddleware:
    """
    Sends a weekly email so the Mailgun account never goes inactive.

    Mailgun blocks sending from accounts that have been idle for a long time
    ("Domain ... is not allowed to send: Account Inactivity"). The site only
    sends email when someone submits a form, which can be months apart. This
    piggybacks on normal web requests rather than needing a separate cron
    service: at most once an hour per worker it checks when the last heartbeat
    went out, and sends another if it was more than a week ago.

    Set MAIL_HEARTBEAT_TO to enable it. Failures are logged and never affect
    the request.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.last_checked = None

    def __call__(self, request):
        response = self.get_response(request)
        try:
            self.maybe_send_heartbeat()
        except Exception:
            logger.exception('Mail heartbeat failed')
        return response

    def maybe_send_heartbeat(self):
        to_address = getattr(settings, 'MAIL_HEARTBEAT_TO', None)
        if not to_address:
            return
        now = time.monotonic()
        if self.last_checked is not None and now - self.last_checked < CHECK_INTERVAL:
            return
        self.last_checked = now

        latest = MailHeartbeat.objects.order_by('-sent_at').first()
        if latest and timezone.now() - latest.sent_at < HEARTBEAT_INTERVAL:
            return

        # Record first so concurrent workers don't all send at once.
        MailHeartbeat.objects.create()
        send_mail(
            'StopWatch website mail heartbeat',
            'This weekly email keeps the Mailgun account for stop-watch.org active. '
            'If it stops arriving, check that the site can still send email.',
            settings.DEFAULT_FROM_EMAIL,
            [x.strip() for x in to_address.split(',') if x.strip()],
        )
        logger.info('Sent mail heartbeat to %s', to_address)
