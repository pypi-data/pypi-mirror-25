import logging
import os
import pytest

from . import db
from .. import mongodb
from ..fb import messenger
from ... import di, Story, utils

logger = logging.getLogger(__name__)

story = None


def teardown_function(function):
    logger.debug('tear down!')
    story and story.clear()


@pytest.fixture
def build_context():
    async def builder(mongodb, no_session=False, no_user=False):
        user = None
        if not no_user:
            user = utils.build_fake_user()
            await mongodb.set_user(user)

        if not no_session:
            session = utils.build_fake_session(user=user)
            await mongodb.set_session(session)

        global story
        story = Story()
        story.use(mongodb)
        fb = story.use(messenger.FBInterface(page_access_token='qwerty'))

        return fb, user

    return builder


@pytest.fixture
@pytest.mark.asyncio
def open_db():
    class AsyncDBConnection:
        def __init__(self):
            self.db_interface = db.MongodbInterface(uri=os.environ.get('TEST_MONGODB_URL', 'mongo'), db_name='test')

        async def __aenter__(self):
            await self.db_interface.start()
            await self.db_interface.clear_collections()
            return self.db_interface

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            self.db_interface.stop()
            await self.db_interface.clear_collections()
            self.db_interface = None

    return AsyncDBConnection


@pytest.mark.asyncio
async def test_store_restore_session(open_db):
    EXCLUDE_FIELDS = ['lastModified']

    def compare_sessions(s1, s2):
        if s1 == s2:
            return True

        for (key, value) in s2.items():
            if key not in ['_id'] and key not in EXCLUDE_FIELDS:
                assert s1[key] == s2[key]

    async with open_db() as db_interface:
        session = utils.build_fake_session()
        session_id = await db_interface.set_session(session)

        logger.info('session_id')
        logger.info(session_id)

        restored_session = await db_interface.get_session(_id=session_id)
        logger.info('restored_session {}'.format(restored_session))
        compare_sessions(session, restored_session)

        restored_session = await db_interface.get_session(user_id=session['user_id'])
        compare_sessions(session, restored_session)

        session['facebook_user_id'] = utils.uniq_id()
        await db_interface.set_session(session)
        restored_session = await db_interface.get_session(user_id=session['user_id'])
        compare_sessions(session, restored_session)


@pytest.mark.asyncio
async def test_store_restore_user(open_db):
    async with open_db() as db_interface:
        user = utils.build_fake_user()

        user_id = await db_interface.set_user(user)
        restored_user = await db_interface.get_user(id=user_id)

        assert user.items() == restored_user.items()


@pytest.mark.asyncio
async def test_create_new_session(open_db):
    async with open_db() as db_interface:
        user = await db_interface.new_user(facebook_user_id='1234567890')
        session = await db_interface.new_session(facebook_user_id='1234567890', user=user)
        assert session['facebook_user_id'] == '1234567890'
        assert 'stack' in session
        assert isinstance(session['stack'], list)
        assert session['user_id'] == user['_id']


@pytest.mark.asyncio
async def test_create_new_user(open_db):
    async with open_db() as db_interface:
        user = await db_interface.new_user(facebook_user_id='1234567890')
        assert user['facebook_user_id'] == '1234567890'


@pytest.mark.asyncio
async def test_start_should_open_connection_and_close_on_stop():
    db_interface = db.MongodbInterface(uri=os.environ.get('TEST_MONGODB_URL', 'mongo'), db_name='test')
    assert not db_interface.session_collection
    assert not db_interface.user_collection
    assert not db_interface.db

    await db_interface.start()

    assert db_interface.session_collection
    assert db_interface.user_collection
    assert db_interface.db

    await db_interface.stop()

    assert not db_interface.session_collection
    assert not db_interface.user_collection
    assert not db_interface.db


def test_get_mongodb_as_dep():
    global story
    story = Story()
    story.use(mongodb.MongodbInterface())

    with di.child_scope():
        @di.desc()
        class OneClass:
            @di.inject()
            def deps(self, storage):
                self.storage = storage

        assert isinstance(di.injector.get('one_class').storage, mongodb.MongodbInterface)
