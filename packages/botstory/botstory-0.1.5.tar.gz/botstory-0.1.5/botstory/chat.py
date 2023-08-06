import asyncio
import logging

from .middlewares import any, location, text

logger = logging.getLogger(__name__)


class Chat:
    def __init__(self):
        self.interfaces = {}

    async def ask(self, body, quick_replies=None, options=None, user=None):
        """
        simple ask with predefined quick replies

        :param body:
        :param quick_replies: (optional) in form of
        {'title': <message>, 'payload': <any json>}
        :param options:
        :param user:
        :return:
        """
        await self.send_text_message_to_all_interfaces(
            recipient=user,
            text=body,
            quick_replies=quick_replies,
            options=options,
        )
        return any.Any()

    # TODO: move to middlewares/location/location.py and make async

    def ask_location(self, body, user):
        # TODO:
        # 1 ask user
        say(body, user)

        # 2 wait for answer
        # 3 process answer
        # 4 ask details once we not sure
        return [location.Any(), text.Any()]

    async def list_elements(self, elements, buttons, user, options):
        tasks = [interface.send_list(recipient=user,
                                     elements=elements,
                                     buttons=buttons,
                                     options=options)
                 for _, interface in self.interfaces.items()]

        res = [body for body in await asyncio.gather(*tasks)]
        return res

    async def say(self, body, user, options):
        """
        say something to user

        :param body:
        :param user:
        :return:
        """
        return await self.send_text_message_to_all_interfaces(
            recipient=user, text=body, options=options)

    async def send_image(self, url, user, options=None):
        tasks = [interface.send_image(user, url, options) for _, interface in self.interfaces.items()]
        return [body for body in await asyncio.gather(*tasks)]

    async def send_template(self, payload, user):
        tasks = [interface.send_template(recipient=user,
                                         payload=payload)
                 for _, interface in self.interfaces.items()]

        res = [body for body in await asyncio.gather(*tasks)]
        return res

    async def send_text_message_to_all_interfaces(self, *args, **kwargs):
        """
        TODO:
        we should know from where user has come and use right interface
        as well right interface can be chosen

        :param args:
        :param kwargs:
        :return:
        """
        logger.debug('async_send_text_message_to_all_interfaces')
        tasks = [interface.send_text_message(*args, **kwargs)
                 for _, interface in self.interfaces.items()]

        logger.debug('  tasks')
        logger.debug(tasks)

        res = [body for body in await asyncio.gather(*tasks)]
        logger.debug('  res')
        logger.debug(res)
        return res

    async def start_typing(self, user):
        logger.debug('# start typing')
        tasks = [interface.start_typing(user)
                 for _, interface in self.interfaces.items()]

        res = [body for body in await asyncio.gather(*tasks)]
        return res

    async def stop_typing(self, user):
        logger.debug('# stop typing')
        tasks = [interface.stop_typing(user)
                 for _, interface in self.interfaces.items()]

        res = [body for body in await asyncio.gather(*tasks)]
        return res

    def add_interface(self, interface):
        logger.debug('add_interface')
        logger.debug(interface)
        self.interfaces[interface.type] = interface
        return interface

    def clear(self):
        self.interfaces = {}
