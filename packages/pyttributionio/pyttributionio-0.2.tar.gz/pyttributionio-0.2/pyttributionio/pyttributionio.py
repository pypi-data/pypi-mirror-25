import logging
import json
import random
import string
import time

import requests
from requests import RequestException

logger = logging.getLogger(__name__)


class PyttributionIo:
    """
    A Python wrapper around the Attribution.io API (by Jakob Löhnertz – www.jakob.codes)
    """

    GET_REQUEST = 'GET'
    API_URL = 'https://attribution.io/api/v1'

    def __init__(self, api_key, api_secret):
        self._api_key = api_key
        self._api_secret = api_secret
        self.RequestException = RequestException

    """
    General methods
    """

    @staticmethod
    def _generate_random_id(size=24, chars=string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for n in range(size))

    def _build_identity_request_data(self, attributionio_id, client_id='', user_agent=''):
        return {
            'identity': {
                'aliases': [attributionio_id],
                'client_id': client_id if client_id else self._generate_random_id(),
                'public_key': self._api_key,
                'created_at': int(time.time()),
                'meta': {
                    'agent': user_agent if user_agent else 'User-Agent unknown'
                }
            }
        }

    def _build_event_request_data(self, attributionio_id, event_key, client_id='', user_agent='', last_url=''):
        client_id = client_id if client_id else self._generate_random_id()

        return {
            'event': {
                'aliases': [attributionio_id],
                'client_id': client_id,
                'event_public_key': event_key,
                'url': last_url if last_url else 'URL unknown',
                'public_key': self._api_key,
                'transaction_id': str(client_id) + '@' + str(int(time.time())),
                'is_informational': False,
                'created_at': int(time.time()),
                'meta': {
                    'agent': user_agent if user_agent else 'User-Agent unknown'
                }
            }
        }

    def _send_private_api_request(self, subject_id, method='GET', endpoint='customers', **params):
        params.update({'secret': self._api_secret})
        response = requests.request(
            method=method,
            url='{url}/{api_key}/{endpoint}/{subject_id}'.format(
                url=PyttributionIo.API_URL,
                api_key=self._api_key,
                endpoint=endpoint,
                subject_id=subject_id,
            ),
            params=params,
        )

        if not response.ok:
            raise RequestException(response.text)

        return json.loads(response.content)

    def _send_public_api_request(self, url, data):
        response = requests.post(
            url=url,
            json=data,
        )

        if not response.ok:
            raise RequestException(response.text)

        return response.status_code

    """
    Private API methods
    """

    """
    Section: Customer
    """

    def fetch_customer_info_base(self, client_id):
        """
        Retrieves the basic information about any customer.

        :param client_id: The identification earlier used to identify the customer e.g. an email address
        :return: The fetched data as native Python data structures
        """

        try:
            return self._send_private_api_request(
                method=PyttributionIo.GET_REQUEST,
                endpoint='customers',
                subject_id=client_id,
            ).get('customer')
        except RequestException as e:
            logger.error('Retrieval of base customer info failed with HTTP status {exception}'.format(exception=e))

    def fetch_customer_info_full(self, client_id):
        """
        Retrieves the full information about any customer.

        :param client_id: The identification earlier used to identify the customer e.g. an email address
        :return: The fetched data as native Python data structures
        """

        try:
            return self._send_private_api_request(
                method=PyttributionIo.GET_REQUEST,
                endpoint='customers',
                subject_id=client_id,
                show_all='true'
            ).get('customer')
        except RequestException as e:
            logger.error('Retrieval of full customer info failed with HTTP status {exception}'.format(exception=e))

    def fetch_customer_info_pageviews(self, client_id):
        """
        Retrieves the pageviews information about any customer.

        :param client_id: The identification earlier used to identify the customer e.g. an email address
        :return: The fetched data as native Python data structures
        """

        try:
            return self._send_private_api_request(
                method=PyttributionIo.GET_REQUEST,
                endpoint='customers',
                subject_id=client_id,
                show_pageviews='true'
            ).get('customer')
        except RequestException as e:
            logger.error('Retrieval of customer pageviews failed with HTTP status {exception}'.format(exception=e))

    def fetch_customer_info_touchpoints(self, client_id):
        """
        Retrieves the touchpoints information about any customer.

        :param client_id: The identification earlier used to identify the customer e.g. an email address
        :return: The fetched data as native Python data structures
        """

        try:
            return self._send_private_api_request(
                method=PyttributionIo.GET_REQUEST,
                endpoint='customers',
                subject_id=client_id,
                show_touchpoints='true'
            ).get('customer')
        except RequestException as e:
            logger.error('Retrieval of customer touchpoints failed with HTTP status {exception}'.format(exception=e))

    def fetch_customer_info_events(self, client_id):
        """
        Retrieves the events information about any customer.

        :param client_id: The identification earlier used to identify the customer e.g. an email address
        :return: The fetched data as native Python data structures
        """

        try:
            return self._send_private_api_request(
                method=PyttributionIo.GET_REQUEST,
                endpoint='customers',
                subject_id=client_id,
                show_events='true'
            ).get('customer')
        except RequestException as e:
            logger.error('Retrieval of customer events failed with HTTP status {exception}'.format(exception=e))

    def fetch_customer_info_identities(self, client_id):
        """
        Retrieves the identities information about any customer.

        :param client_id: The identification earlier used to identify the customer e.g. an email address
        :return: The fetched data as native Python data structures
        """

        try:
            return self._send_private_api_request(
                method=PyttributionIo.GET_REQUEST,
                endpoint='customers',
                subject_id=client_id,
                show_identities='true'
            ).get('customer')
        except RequestException as e:
            logger.error('Retrieval of customer identities failed with HTTP status {exception}'.format(exception=e))

    """
    Public API Methods
    """

    def trigger_identity(self, attributionio_id, client_id='', user_agent=''):
        """
        Links any type of identification e.g. an email address, a customer reference number etc. to a
        so far anonymous cookie.

        :param attributionio_id: The cookie value (AttrioP_)
        :param client_id: [optional] The chosen identification of the client e.g. an email address
        :param user_agent: [optional] The User Agent of the client
        :return: The HTTP status code of the request
        """

        try:
            return self._send_public_api_request(
                url='https://api.attribution.io/identities',
                data=self._build_identity_request_data(
                    attributionio_id=attributionio_id,
                    client_id=client_id,
                    user_agent=user_agent,
                )
            )
        except RequestException as e:
            logger.error(
                'Identity trigger for ID "{attributionio_id}" failed with HTTP status {exception}!'.format(
                    attributionio_id=attributionio_id,
                    exception=e,
                )
            )

    def trigger_event(self, attributionio_id, event_key, client_id='', user_agent='', last_url=''):
        """
        Triggers any event towards Attribution.io

        :param attributionio_id: The cookie value (AttrioP_)
        :param event_key: The event key chosen in the settings of Attribution.io
        :param client_id: [optional] The chosen identification of the client e.g. an email address
        :param user_agent: [optional] The User Agent of the client
        :param last_url: [optional] The most recent URL the client visited where he/she triggered the event
        :return: The HTTP status code of the request
        """

        try:
            event_trigger_response = self._send_public_api_request(
                url='https://api.attribution.io/events',
                data=self._build_event_request_data(
                    attributionio_id=attributionio_id,
                    event_key=event_key,
                    client_id=client_id,
                    user_agent=user_agent,
                    last_url=last_url,
                )
            )

            identity_trigger_response = self.trigger_identity(
                attributionio_id=attributionio_id,
                client_id=client_id,
                user_agent=user_agent,
            )

            return event_trigger_response, identity_trigger_response
        except RequestException as e:
            logger.error(
                'Event trigger for ID "{attributionio_id}" failed with HTTP status {exception}!'.format(
                    attributionio_id=attributionio_id,
                    exception=e,
                )
            )
