import ssl
import json
import time
import logging
import websocket
import requests
from threading import Thread, Lock

try:
    import queue as Queue # python3
except ImportError:
    import Queue # python2

import slacksocket.errors as errors
from .config import slackurl, event_types
from .models import SlackEvent, SlackMsg

log = logging.getLogger('slacksocket')

class WebAPIClient(requests.Session):
    """ A very small client for connecting to Slack web API """

    def __init__(self, token):
        self._token = token
        super(Client, self).__init__()

    def get(self, url, method='GET', max_attempts=3, **params):
        if max_attempts == 0:
            raise errors.SlackAPIError('Max retries exceeded')
        elif max_attempts < 0:
            message = 'Expected max_attempts >= 0, got {0}'\
                .format(max_attempts)
            raise ValueError(message)

        params['token'] = self._token
        res = self.request(method, url, params=params)

        try:
            res.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise errors.SlackAPIError(e)

        rj = res.json()

        if rj['ok']:
            return rj

        # process error
        if rj['error'] == 'migration_in_progress':
            log.info('socket in migration state, retrying')
            time.sleep(2)
            return self.get(url,
                            method=method,
                            max_attempts=max_attempts - 1,
                            **params)
        else:
            raise errors.SlackAPIError('Error from slack api:\n%s' % res.text)

class SlackSocket(object):
    """
    SlackSocket class provides a streaming interface to the Slack Real Time
    Messaging API
    params:
     - token(str): token to authenticate with slack
     - translate(bool): yield events with human-readable names
        rather than id. default true
     - event_filter(list): Slack event type(s) to filter by. Excluding a
            filter returns all slack events. See https://api.slack.com/events
            for a listing of valid event types.
    """

    def __init__(self, token, translate=True, event_filters='all'):
        if type(translate) != bool:
            raise TypeError('translate must be a boolean')
        self._validate_filters(event_filters)

        self._eventq = Queue.Queue()
        # self._eventq = []
        self._sendq = []
        self.connected = False
        self._translate = translate
        self.event_filters = event_filters

        self._client = WebAPIClient(token)
        self.team, self.user = self._auth_test()

        self._thread = Thread(target=self._open)
        self._thread.daemon = True
        self._thread.start()

        # wait for websocket connection to be established before returning
        while not self.connected:
            time.sleep(.2)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    def get_event(self, timeout=None):
        """
        return a single event object or block until an event is
        received and return it.
        """
        # return or block until we have something to return or timeout
        return self._eventq.get(timeout=timeout)

    def events(self, timeout=None):
        """
        returns a blocking generator yielding Slack event objects
        params:
        """
        done = False
        while not done:
            try:
                e = self.get_event(timeout)
                yield (e)
            except (KeyboardInterrupt, Queue.Empty):
                done = True

        self.close()

    def send_msg(self, text, channel_name=None, channel_id=None, confirm=True):
        """
        Send a message via Slack RTM socket, returning the message object
        after receiving a reply-to confirmation
        """
        if not channel_name and not channel_id:
            raise Exception('One of channel_id or channel_name \
                             parameters must be given')
        if channel_name:
            c = self._lookup_channel_by_name(channel_name)
            channel_id = c['channel_id']

        self._send_id += 1
        msg = SlackMsg(self._send_id, channel_id, text)
        self.ws.send(msg.json)

        if confirm:
            # Wait for confirmation our message was received
            for e in self.events():
                if 'reply_to' in e.event:
                    if e.event['reply_to'] == self._send_id:
                        msg.sent = True
                        msg.ts = e.ts
                        return msg
        else:
            return msg

    def get_im_channel(self, user_name):
        """
        Get a direct message channel to a particular user. Create
        one if it does not exist.
        """
        user_id = self._find_user_id(user_name)
        channel_info = self._find_channel(['ims'], 'user', user_id)

        if channel_info is None:
            channel = self._open_im_channel(user_id)

        else:
            (channel_type, matching) = channel_info
            assert channel_type == 'ims'
            assert len(matching) == 1
            channel = matching[0]

        return channel

    def close(self):
        self.ws.on_close = lambda ws: True
        self.ws.close()

    #######
    # Internal Methods
    #######

    def _open(self):
        # reset id for sending messages with each new socket
        self._send_id = 0
        self.ws = websocket.WebSocketApp(self._get_websocket_url(),
                                         on_message=self._event_handler,
                                         on_error=self._error_handler,
                                         on_open=self._open_handler,
                                         on_close=self._exit_handler)
        self.ws.run_forever(sslopt={'cert_reqs': ssl.CERT_NONE})

    def _validate_filters(self, filters):
        if filters == 'all':
            filters = event_types

        if type(filters) != list:
            raise TypeError('filters must be given as a list')

        for f in filters:
            if f not in event_types:
                raise errors.SlackSocketEventNameError('unknown event type %s\n \
                             see https://api.slack.com/events' % filters)

    def _get_websocket_url(self):
        """
        Retrieve a fresh websocket url from slack api
        """
        return self._client.get(slackurl['rtm'])['url']

    def _auth_test(self):
        """
        Perform API auth test and get our user and team
        """
        test = self._client.get(slackurl['test'])

        if self._translate:
            return (test['team'], test['user'])
        else:
            return (test['team_id'], test['user_id'])


    def _open_im_channel(self, user_id):
        """
        Open a direct message channel with a user
        """
        result = self._client.get(slackurl['im.open'],
                                      method='POST',
                                      user=user_id)
        return result['channel']

    def _translate_event(self, event):
        """
        Translate all user and channel ids in an event to human-readable names
        """
        if 'user' in event.event:
            event.event['user'] = self._lookup_user(event.event['user'])

        if 'channel' in event.event:
            c = self._lookup_channel_by_id(event.event['channel'])
            event.event['channel'] = c['channel_name']

        event.mentions = [self._lookup_user(u) for u in event.mentions]

        return event

    #######
    # Websocket Handlers
    #######

    def _event_handler(self, ws, event_json):
        log.debug('event recieved: %s' % event_json)

        json_object = json.loads(event_json)

        if self.event_filters != "all" and json_object.get("type") not in self.event_filters:
            log.debug("Ignoring the event {} as it not matching event_filers {}"
                      .format(event_json, self.event_filters))
            return

        event = SlackEvent(json_object)

        # TODO: make use of ctype returned from _lookup_channel
        if self._translate:
            event = self._translate_event(event)

        # self._eventq.append(event)
        self._eventq.put(event)

    def _open_handler(self, ws):
        log.info('websocket connection established')
        self.connected = True
        self.connect_ts = time.time()

    def _error_handler(self, ws, error):
        log.critical('websocket error:\n %s' % error)

    def _exit_handler(self, ws):
        log.warn('websocket connection closed')
        # Don't attempt reconnect if our last attempt was less than 30s ago
        if (time.time() - self.connect_ts) < 30:
            raise errors.SlackSocketConnectionError(
                'Failed to establish a websocket connection'
            )
        log.warn('attempting to reconnect')
        self._thread = Thread(target=self._open)
        self._thread.start()
