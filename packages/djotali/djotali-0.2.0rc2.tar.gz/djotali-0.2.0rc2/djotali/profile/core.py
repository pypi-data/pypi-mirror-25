from datetime import date

import six
from django.conf import settings
from django.utils.crypto import salted_hmac, constant_time_compare
from django.utils.http import int_to_base36, base36_to_int


class InvitationTokenGenerator:
    def check_token(self, token, email, organization):
        """
        Check that an invitation token is correct.
        """
        if not (email and organization and token):
            return False
        # Parse the token
        try:
            ts_b36, token = token.split("-")
        except ValueError:
            return False

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

        # Check that the timestamp/uid has not been tampered with
        if not constant_time_compare(self._make_token_with_timestamp(email, organization, ts).split("-")[1], token):
            return False

        # Check the timestamp is within limit
        if (self._num_days(self._today()) - ts) > settings.INVITATION_TIMEOUT_DAYS:
            return False

        return True

    def generate_token(self, email, organization):
        return self._make_token_with_timestamp(email, organization, self._num_days(self._today()))

    def _make_token_with_timestamp(self, email, organization, timestamp):
        invitation_signing_key = settings.INVITATION_SIGNING_KEY
        ts_b36 = int_to_base36(timestamp)
        token = salted_hmac(
            invitation_signing_key,
            self._make_hash_value(email, organization, timestamp),
        ).hexdigest()[::2]
        return "%s-%s" % (ts_b36, token)

    @staticmethod
    def _make_hash_value(email, organization, timestamp):
        # Ensure results are consistent across DB backends
        return six.text_type(email) + six.text_type(organization) + six.text_type(timestamp)

    @staticmethod
    def _num_days(dt):
        return (dt - date(2001, 1, 1)).days

    @staticmethod
    def _today():
        # Used for mocking in tests
        return date.today()
