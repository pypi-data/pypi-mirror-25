import botstory
from botstory.ast import story_context
from botstory.utils import build_fake_session, build_fake_user


class Talk:
    def __init__(self, session=None, user=None, story=None):
        if not user:
            user = build_fake_user()
        if not session:
            session = build_fake_session()
        self.session = session
        self.user = user
        self.story = story

    def __enter__(self):
        self.story = botstory.Story()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.story.clear()
        return False

    def __call__(self, *args, **kwargs):
        return self.wrap_user_talk(args[0])

    def init_by_ctx(self, ctx):
        self.session = ctx.message['session']

    async def location(self, loc):
        return await self.wrap_user_talk(location)(loc)

    async def pure_text(self, text):
        return await self.wrap_user_talk(pure_text)(text)

    async def option(self, payload):
        return await self.wrap_user_talk(option)(payload)

    async def ask(self, payload):
        if payload is None:
            return await self.story.match_message(
                story_context.set_message_data(
                    story_context.clean_message_data({
                        'session': self.session,
                        'user': self.user,
                    }), {}))
        if 'sticker_id' in payload:
            return await self.wrap_user_talk(sticker)(payload)
        if isinstance(payload, str):
            return await self.pure_text(payload)
        raise NotImplementedError('put all other message types here')

    def wrap_user_talk(self, fn):
        async def fn_wrapper(payload):
            mutated_ctx = await fn(payload,
                                   self.session,
                                   self.user,
                                   self.story)
            self.session = mutated_ctx['session']
            self.user = mutated_ctx['user']
            return mutated_ctx

        return fn_wrapper


async def location(loc, session=None, user=None, story=None):
    return await story.match_message(
        story_context.set_message_data(
            story_context.clean_message_data({
                'session': session,
                'user': user,
            }), 'attachments', [{
                'type': 'location',
                'payload': loc
            }]))


async def pure_text(text, session=None, user=None, story=None):
    return await story.match_message(
        story_context.set_message_data(
            story_context.clean_message_data({
                'session': session,
                'user': user,
            }), 'text', {
                'raw': text,
            }))


async def option(payload, session=None, user=None, story=None):
    return await story.match_message(
        story_context.set_message_data(
            story_context.clean_message_data({
                'session': session,
                'user': user,
            }), 'option',
            'value', payload))


async def sticker(payload, session=None, user=None, story=None):
    return await story.match_message(
        story_context.set_message_data(
            story_context.clean_message_data({
                'session': session,
                'user': user,
            }), 'sticker_id', payload['sticker_id']))
