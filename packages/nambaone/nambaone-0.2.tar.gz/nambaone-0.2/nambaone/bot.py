import requests
from . chat import Chat
from . message import Message
from . event_handler import EventHandler

class Bot:
    _response = {
        'code': 200,
        'success': True,
    }

    def __init__(self,
                 token,
                 base_url=None,
                 user_follow_handler=None,
                 user_unfollow_handler=None,
                 message_new_handler=None,
                 message_update_handler=None,
                 chat_new_handler=None):

        self._base_url = base_url or 'https://api.namba1.co'

        self._token = token

        self.handler = EventHandler(
            self,
            user_follow_handler,
            user_unfollow_handler,
            message_new_handler,
            message_update_handler,
            chat_new_handler
        )

    @property
    def response(self):
        self._response['success'] = self._response['code'] == 200
        return self._response

    @property
    def header(self):
        return {
            'X-Namba-Auth-Token': self._token
        }

    def run(self, request):
        event = str(request['event']).replace('/', '_')

        try:
            update = getattr(self.handler, 'event_{}'.format(event))(request['data'])
            self.__call_handler(event, update)
        except Exception as e:
            self._response['code'] = 520

    def __call_handler(self, event, update):
        if hasattr(self.handler, event) and callable(getattr(self.handler, event)):
            getattr(self.handler, event)(self, update)

    def send_message(self, chat_id, content, content_type):
        params = {
            'type': content_type,
            'content': content,
        }
        url = '{}/chats/{}/write'.format(self._base_url, chat_id)

        response = requests.post(url, params, headers=self.header).json()

        return Message.from_dict(response['data'])

    def create_chat(self, user_id, name='', image=''):
        params = {
            'name': name,
            'image': image,
            'members[]': user_id,
        }
        url = '{}/chats/create'.format(self._base_url)

        response = requests.post(url, params, headers=self.header).json()

        return Chat.from_dict(response['data'])

    def typing_start(self, chat_id):
        url = '{}/chats/{}/typing'.format(self._base_url, chat_id)

        return requests.get(url, headers=self.header)

    def typing_stop(self, chat_id):
        url = '{}/chats/{}/stoptyping'.format(self._base_url, chat_id)

        return requests.get(url, headers=self.header)
