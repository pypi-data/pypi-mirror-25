import asyncio
from botstory.ast import story_context
from botstory.integrations.commonhttp import errors as commonhttp_errors
import functools
import logging
from . import validate
from .. import commonhttp
from ... import di
from ...middlewares import option

logger = logging.getLogger(__name__)


@di.desc('fb', reg=False)
class FBInterface:
    type = 'facebook'

    def __init__(self,
                 api_uri='https://graph.facebook.com/v2.6',
                 greeting_text=None,
                 page_access_token='?',
                 persistent_menu=None,
                 webhook_url=None,
                 webhook_token=None,
                 ):
        """

        :param api_uri:
        :param greeting_text:
        :param page_access_token:
        :param persistent_menu:
        :param webhook_url:
        :param webhook_token:
        """
        self.api_uri = api_uri
        self.greeting_text = greeting_text
        self.persistent_menu = persistent_menu
        self.token = page_access_token
        self.webhook = webhook_url
        self.webhook_token = webhook_token

        self.library = None
        self.http = None
        self.story_processor = None
        self.storage = None
        self.users = None

    @di.inject()
    def add_library(self, stories_library):
        logger.debug('add_library')
        logger.debug(stories_library)
        self.library = stories_library

    @di.inject()
    def add_http(self, http):
        """
        inject http provider

        :param http:
        :return:
        """
        logger.debug('add_http')
        logger.debug(http)
        self.http = http

    @di.inject()
    def add_processor(self, story_processor):
        logger.debug('add_processor')
        logger.debug(story_processor)
        self.story_processor = story_processor

    @di.inject()
    def add_storage(self, storage):
        logger.debug('add_storage')
        logger.debug(storage)
        self.storage = storage

    @di.inject()
    def add_users(self, users):
        logger.debug('add_users')
        logger.debug(users)
        self.users = users

    async def send_text_message(self, recipient, text,
                                quick_replies=None,
                                options=None):
        """
        async send message to the facebook user (recipient)

        :param recipient:
        :param text:
        :param quick_replies:
        :param options

        :return:
        """

        try:
            validate.send_text_message(text, quick_replies)
        except validate.ExceedLengthException as i:
            # TODO: take first part of message show option `more`
            # store last part until user press `more`

            # TODO: register dynamic `quick answer` handler
            # with the rest of message

            # TODO: or handle it on application level?
            # motivation: if we're working with dynamic data or endless
            # we could just pass text. It should be generator
            logger.warn(str(i))

            if options and options.get('overflow', None) == 'cut':
                text = text[:i.limit]
            else:
                text = text[:i.limit - 2] + '\u2026'
        except validate.Invalid as i:
            logger.warn(str(i))

        if not quick_replies:
            quick_replies = []

        message = {
            'text': text,
        }

        quick_replies = [{'content_type': 'text', **reply} for reply in quick_replies]
        if len(quick_replies) > 0:
            message['quick_replies'] = quick_replies

        return await self.http.post(
            self.api_uri + '/me/messages/',
            params={
                'access_token': self.token,
            },
            json={
                'recipient': {
                    'id': recipient['facebook_user_id'],
                },
                'message': message,
            })

    async def send_list(self, recipient, elements, buttons=None, options=None):
        """
        send list of elements
        :param recipient:
        :param elements:
        :param buttons:
        :return:
        """
        # try:
        #     validate.send_listd
        # except
        # ....

        buttons = [{**b, 'type': b.get('type', 'postback')} for b in buttons]

        options = options or {}

        return await self.send_template(recipient, {
            'template_type': 'list',
            'top_element_style': options.get('top_element_style', 'large'),
            'elements': elements,
            'buttons': buttons,
        })

    async def send_image(self, recipient, url, options=None):
        if options is None:
            options = {}

        should_try = True
        delay = options.get('retry_delay', 1)
        tries = options.get('retry_times', 3)

        while should_try:
            try:
                await self._send_image(recipient, url)
                should_try = False
            except commonhttp_errors.HttpRequestError as err:
                if tries > 0:
                    tries -= 1
                    logger.warning('# retry to send image {}'.format(url))
                    should_try = True
                    await asyncio.sleep(delay)
                else:
                    raise err

    async def _send_image(self, recipient, url):
        return await self.http.post(
            self.api_uri + '/me/messages/',
            params={
                'access_token': self.token,
            },
            json={
                'recipient': {
                    'id': recipient['facebook_user_id'],
                },

                'message': {
                    'attachment': {
                        'type': 'image',
                        'payload': {
                            'url': url,
                        },
                    },
                },
            })

    async def send_template(self, recipient, payload):
        """
        send template based message

        :param recipient:
        :param payload:
        :return:
        """
        return await self.http.post(
            self.api_uri + '/me/messages/',
            params={
                'access_token': self.token,
            },
            json={
                'recipient': {
                    'id': recipient['facebook_user_id'],
                },

                'message': {
                    'attachment': {
                        'type': 'template',
                        'payload': payload,
                    }
                },
            })

    async def request_profile(self, facebook_user_id):
        """
        Make request to facebook
        to receive more information about user

        More: https://developers.facebook.com/docs/messenger-platform/user-profile

        :param facebook_user_id:
        :return:
        """
        return await self.http.get(
            '{}/{}'.format(self.api_uri, facebook_user_id),
            params={
                'access_token': self.token,
            },
        )

    async def handle(self, data):
        """
        handle fb messenger message and return 200Ok as quick as possible
        In background we launch process of handling incoming message
        This solution is ok only for small apps for bigger one it is much better
        to use a queue.

        TODO: support third party queue

        :param data:
        :return:
        """
        loop = asyncio.get_event_loop()
        loop.create_task(self.process(data))
        return {
            'status': 200,
            'text': 'Ok!',
        }

    async def process(self, data):
        """
        async process message which comes from fb messenger

        :param data:
        :return:
        """
        logger.debug('')
        logger.debug('> handle <')
        logger.debug('')
        logger.debug('  entry: {}'.format(data))
        try:
            for e in data.get('entry', []):
                messaging = e.get('messaging', [])
                logger.debug('  messaging: {}'.format(messaging))

                if len(messaging) == 0:
                    logger.warning('  entry {} list lack of "messaging" field'.format(e))

                for m in messaging:
                    logger.debug('  m: {}'.format(m))

                    facebook_user_id = m['sender']['id']

                    logger.debug('before get user with facebook_user_id={}'.format(facebook_user_id))
                    user = await self.storage.get_user(facebook_user_id=facebook_user_id)
                    if not user:
                        logger.debug('  should create new user {}'.format(facebook_user_id))

                        try:
                            messenger_profile_data = await self.request_profile(facebook_user_id)
                            logger.debug('receive fb profile {}'.format(messenger_profile_data))
                        except commonhttp.errors.HttpRequestError as err:
                            logger.debug('fail on request fb profile of {}. with {}'.format(facebook_user_id, err))
                            messenger_profile_data = {
                                'no_fb_profile': True,
                            }

                        logger.debug('before creating new user')
                        user = await self.storage.new_user(
                            facebook_user_id=facebook_user_id,
                            no_fb_profile=messenger_profile_data.get('no_fb_profile', None),
                            first_name=messenger_profile_data.get('first_name', None),
                            last_name=messenger_profile_data.get('last_name', None),
                            profile_pic=messenger_profile_data.get('profile_pic', None),
                            locale=messenger_profile_data.get('locale', None),
                            timezone=messenger_profile_data.get('timezone', None),
                            gender=messenger_profile_data.get('gender', None),
                        )

                        self.users.on_new_user_comes(user)

                    session = await self.storage.get_session(facebook_user_id=facebook_user_id)
                    if not session:
                        logger.debug('  should create new session for user {}'.format(facebook_user_id))
                        session = await self.storage.new_session(
                            facebook_user_id=facebook_user_id,
                            stack=[],
                            user=user,
                        )

                    ctx = story_context.clean_message_data({
                        'session': session,
                        'user': user,
                    })

                    if 'message' in m:
                        logger.debug('message notification')
                        raw_message = m.get('message', {})
                        if 'is_echo' in raw_message:
                            # TODO: should react somehow.
                            # for example storing for debug purpose
                            logger.debug('just echo message')
                        else:
                            text = raw_message.get('text', None)
                            if text is not None:
                                ctx = story_context.set_message_data(ctx,
                                                                     'text', {
                                                                         'raw': text,
                                                                     })
                            elif 'sticker_id' in raw_message:
                                ctx = story_context.set_message_data(ctx,
                                                                     'sticker_id', raw_message['sticker_id'],
                                                                     )
                            elif 'attachments' in raw_message:
                                ctx = story_context.set_message_data(ctx,
                                                                     'attachments', raw_message['attachments'])
                            else:
                                logger.warning('  entry {} "text"'.format(e))

                            quick_reply = raw_message.get('quick_reply', None)
                            if quick_reply is not None:
                                ctx = story_context.set_message_data(ctx,
                                                                     'option',
                                                                     'value', quick_reply['payload'])

                            ctx = await self.story_processor.match_message(ctx)

                    elif 'postback' in m:
                        ctx = story_context.set_message_data(ctx,
                                                             'option',
                                                             'value', m['postback']['payload'])
                        ctx = await self.story_processor.match_message(ctx)
                    elif 'delivery' in m:
                        logger.debug('delivery notification')
                    elif 'read' in m:
                        logger.debug('read notification')
                    else:
                        logger.warning('(!) unknown case {}'.format(e))

                    # after message were processed session and user information could change
                    # so we should store it for the next usage
                    await self.storage.set_session(ctx['session'])
                    await self.storage.set_user(ctx['user'])

        except BaseException as err:
            logger.exception(err)

        return {
            'status': 200,
            'text': 'Ok!',
        }

    async def setup(self):
        logger.debug('setup')

        if self.greeting_text:
            await self.replace_greeting_text(self.greeting_text)

        # check whether we have `On Start Story`

        # error if we don't have start button handler but have persistent menu:
        # (#100) You must set a Get Started button if you also wish to use persistent menu.
        have_on_start_story = not not self.library.get_global_story(story_context.set_message_data({
            'session': {}
        }, 'option',
            'value', option.OnStart.DEFAULT_OPTION_PAYLOAD))

        if have_on_start_story or self.persistent_menu:
            await self.remove_greeting_call_to_action_payload()
            await self.set_greeting_call_to_action_payload(option.OnStart.DEFAULT_OPTION_PAYLOAD)

        if self.persistent_menu:
            await self.replace_persistent_menu(self.persistent_menu)

        await self.subscribe()

    async def before_start(self):
        logger.debug('# start')
        if self.webhook and self.http:
            self.http.webhook(self.webhook, self.handle, self.webhook_token)

    async def replace_greeting_text(self, message):
        """
        delete greeting text before
        :param message:
        :return:
        """
        try:
            await self.remove_greeting_text()
        except Exception:
            pass

        await self.set_greeting_text(message)

    async def set_greeting_text(self, message):
        """
        set a greeting for new conversations

        can use for personalizing
            {{user_first_name}}
            {{user_last_name}}
            {{user_full_name}}

        more: https://developers.facebook.com/docs/messenger-platform/thread-settings/greeting-text

        :param message:
        :return:
        """
        logger.debug('set_greeting_text')

        greeting_data = {
            'locale': 'default',
            'text': message,
        }

        try:
            validate.greeting_text(message)
        except validate.Invalid as i:
            logger.warn(str(i))

        self.greeting_text = message

        if not self.http:
            # should wait until receive http
            return

        await self.http.post(
            self.api_uri + '/me/messenger_profile',
            params={
                'access_token': self.token,
            },
            json={
                'greeting': [
                    greeting_data,
                ],
            }
        )

    async def remove_greeting_text(self):
        logger.debug('# remove_greeting_text')
        if not self.http:
            return

        await self.http.delete(
            self.api_uri + '/me/messenger_profile',
            params={
                'access_token': self.token,
            },
            json={
                'fields': [
                    'greeting',
                ]
            }
        )

    async def set_greeting_call_to_action_payload(self, payload):
        logger.debug('# set_greeting_call_to_action_payload')
        """

        more: https://developers.facebook.com/docs/messenger-platform/thread-settings/get-started-button

        :param payload:
        :return:
        """
        await self.http.post(
            self.api_uri + '/me/messenger_profile',
            params={
                'access_token': self.token,
            },
            json={
                'get_started': {'payload': payload}
            }
        )

    async def remove_greeting_call_to_action_payload(self):
        logger.debug('# remove_greeting_call_to_action_payload')
        if not self.http:
            return

        await self.http.delete(
            self.api_uri + '/me/messenger_profile',
            params={
                'access_token': self.token,
            },
            json={
                'fields': [
                    'get_started',
                ]
            }
        )

    async def replace_persistent_menu(self, menu):
        logger.debug('# replace_persistent_menu')
        try:
            await self.remove_persistent_menu()
        except Exception:
            pass
        await self.set_persistent_menu(menu)

    async def set_persistent_menu(self, menu):
        """
        more: https://developers.facebook.com/docs/messenger-platform/thread-settings/persistent-menu

        :param menu:
        :return:
        """
        logger.debug('# set_persistent_menu')
        if not isinstance(menu, list) or len(menu) == 0:
            raise ValueError(
                'Menu should be not empty list. '
                'More info here: '
                'https://developers.facebook.com/docs/messenger-platform/messenger-profile/persistent-menu')
        if all('locale' in item for item in menu):
            # TODO: should validate as well
            persistent_menu = menu
        else:
            try:
                validate.persistent_menu(menu)
            except validate.Invalid as i:
                logger.warn(str(i))
            persistent_menu = [{
                'locale': 'default',
                'call_to_actions': menu,
            }]

        self.persistent_menu = persistent_menu

        if not self.http:
            # should wait until receive http
            logger.warning('There is no http interface yet')
            return

        await self.http.post(
            self.api_uri + '/me/messenger_profile',
            params={
                'access_token': self.token,
            },
            json={
                'persistent_menu': persistent_menu,
            }
        )

    async def remove_persistent_menu(self):
        logger.debug('# remove_persistent_menu')
        if not self.http:
            return

        await self.http.delete(
            self.api_uri + '/me/messenger_profile',
            params={
                'access_token': self.token,
            },
            json={'fields': [
                'persistent_menu',
            ]}
        )

    async def start_typing(self, user):
        logger.debug('# start typing')
        await self.http.post(
            self.api_uri + '/me/messages',
            params={
                'access_token': self.token,
            },
            json={
                'recipient': {
                    'id': user['facebook_user_id'],
                },
                'sender_action': 'typing_on',
            },
        )

    async def stop_typing(self, user):
        logger.debug('# stop typing')
        await self.http.post(
            self.api_uri + '/me/messages',
            params={
                'access_token': self.token,
            },
            json={
                'recipient': {
                    'id': user['facebook_user_id'],
                },
                'sender_action': 'typing_off',
            },
        )

    async def subscribe(self):
        """
        subscribe the app to page updates
        docs:
        https://developers.facebook.com/docs/messenger-platform/guides/setup#subscribe_app

        :return:
        """
        logger.debug('# subscribe page')
        await self.http.post(
            self.api_uri + '/me/subscribed_apps',
            params={
                'access_token': self.token,
            },
        )
