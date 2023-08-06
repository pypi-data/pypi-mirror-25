import time
import requests
from threading import Thread, Lock

import .errors
from .config import slackurl
from .client import WebAPIClient

slackurl = { 'test': slack + 'auth.test',
             'rtm': slack + 'rtm.start',
             'users': slack + 'users.list',
             'channels': slack + 'channels.list',
             'groups': slack + 'groups.list',
             'ims': slack + 'im.list',
             'im.open': slack + 'im.open' }

class SlackMap(object):

    user_map = {}
    user_lock = Lock()

    channel_map = {}
    channel_lock = Lock()

    def __init__(self, token):
        self._client = WebAPIClient(token)
        self.refresh_users()
        self.refresh_channels()

    def refresh_users(self):
        """
        Fetch users and updates the user_map property
        """

        self.user_lock.acquire()
        try:
            response = self._call_slack_rtm(slackurl['users'])
            self.loaded_users = response['members']
        finally:
            self.user_lock.release()

    def refresh_channels(self):
        """
        Fetch channel info and updates the channel_map property
        """

        self.channel_lock.acquire()
        try:
            for channel_type in ['channels', 'groups', 'ims']:
                response = self._call_slack_rtm(slackurl[channel_type])
                channel_list = response[channel_type]
                self.loaded_channels[channel_type] = channel_list
        finally:
            self.channel_lock.release()

    def _lookup_user(self, user_id):
        """
        Look up a username from user id
        """
        if user_id == 'USLACKBOT':
            return "slackbot"

        name = self._find_user_name(user_id)

        # if the user is not found may be a new user got added after
        # cache is loaded so reload it one more time
        if not name:
            self.refresh_users()
            name = self._find_user_name(user_id)

        return name if name else "unknown"

    def _find_user_name(self, user_id):
        """
        Finds user's name by their id.
        """
        self.user_lock.acquire()
        try:
            users = self.loaded_users
        finally:
            self.user_lock.release()

        for user in users:
            if user['id'] == user_id:
                return user['name']

    def _find_user_id(self, username):
        """
        Finds user's id by their name.
        """
        with self.load_user_lock:
            users = self.loaded_users

        for user in users:
            if user['name'] == username:
                return user['id']

    def _lookup_channel_by_id(self, id):
        """
        Looks up a channel name from its id
        params:
         - id(str): The channel id to lookup
        """
        channel_type, matching = self._find_channel(['channels', 'groups', 'ims'],
                                                    "id",
                                                    id)

        # may be channel got created after the cache got loaded so reload the it one more time
        if not matching:
            self._load_channels()
            channel_type, matching = self._find_channel(['channels', 'groups', 'ims'],
                                                        "id",
                                                        id)

        if matching:
            channel = matching[0]
            if channel_type == 'ims':
                channel_name = self._lookup_user(channel['user'])
            else:
                channel_name = channel['name']

            return {'channel_type': channel_type,
                    'channel_name': channel_name}

        # if no matches were found
        return {'channel_type': 'unknown',
                'channel_name': 'unknown'}

    def _find_channel(self, channel_types, channel_key, value):
        """
        filters channels present in the cache using key and value
        """
        self.load_channel_lock.acquire()
        try:
            channels = self.loaded_channels
        finally:
            self.load_channel_lock.release()

        for channel_type, channel_list in channels.items():
            if channel_type not in channel_types:
                continue;
            matching = [c for c in channel_list if c[channel_key] == value]
            if matching:
                return channel_type, matching

        return [None, False]

    def _lookup_channel_by_name(self, name):
        """
        Look up a channel id from a given name
        params:
         - name(str): The channel name to lookup
        """
        channel_type, matching = self._find_channel(['channels', 'groups'],
                                                    "name",
                                                    name)
        # may be channel got created after the cache got loaded so reload the it one more time
        if not matching:
            self._load_channels()
            channel_type, matching = self._find_channel(['channels', 'groups'],
                                                        "name",
                                                        name)

        if matching:
            channel = matching[0]

            return {'channel_type': channel_type,
                    'channel_id': channel['id']}

        # if no matches were found
        return {'channel_type': 'unknown',
                'channel_id': 'unknown'}
