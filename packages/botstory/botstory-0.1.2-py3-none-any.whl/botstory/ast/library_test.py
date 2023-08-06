import pytest
from . import forking, library, parser


@pytest.fixture(scope='function')
def story_library():
    l = library.StoriesLibrary()
    story_1 = parser.ASTNode('hi!')
    fork = story_1.append(forking.StoryPartFork())
    story_1_1 = parser.ASTNode('How do you feel?')
    fork.local_scope.add(story_1_1)

    story_2 = parser.ASTNode('bye!')
    story_3 = parser.ASTNode('where to go?')

    l.add_global(story_1)
    l.add_global(story_2)
    l.add_callable(story_3)
    return l


def test_empty_library_should_return_none():
    lib = library.StoriesLibrary()
    story = lib.get_story_by_topic('hi!')
    assert story is None


def test_get_top_level_story(story_library):
    story = story_library.get_story_by_topic('hi!')
    assert story.topic == 'hi!'


def test_get_substory(story_library):
    stack = [{
        'topic': 'hi!'
    }]
    story = story_library.get_story_by_topic('How do you feel?', stack=stack)
    assert story.topic == 'How do you feel?'
