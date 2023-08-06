from botstory import ast, matchers
from collections import OrderedDict
import logging
import json

logger = logging.getLogger(__name__)


class Undefined:
    """
    Because we can got ever None value we should have something
    that definitely noted that value wasn't defined
    """

    def __init__(self):
        pass


class StoryPartFork:
    def __init__(self):
        self.local_scope = ast.library.StoriesScope()

    @property
    def __name__(self):
        return 'StoryPartFork'

    # this one very similar to validation in story loop
    def by_topic(self, topic):
        stories = self.local_scope.by_topic(topic)
        return stories[0] if len(stories) > 0 else None

    @property
    def children(self):
        return self.local_scope.stories

    def children_matcher(self):
        return Switch(
            self.local_scope.all_filters()
        )

    def should_loop(self):
        return False

    def __call__(self, *args, **kwargs):
        return None

    def get_child_by_validation_result(self, validation_result):
        case_stories = self.local_scope.get_story_by(case_id=validation_result)
        if len(case_stories) == 0:
            case_stories = self.local_scope.get_story_by(case_equal=validation_result)
        if len(case_stories) == 0:
            case_stories = self.local_scope.get_story_by(default_case=True)

        if len(case_stories) == 0:
            logger.debug('#######################################')
            logger.debug('# get_child_by_validation_result      #')
            logger.debug('#######################################')
            logger.debug('# [!] do not have any fork here       #')
            logger.debug('# context = {}'.format(self))
            logger.debug('# validation_result = {}'.format(validation_result))
            logger.debug('#######################################')
            return None

        return case_stories[0]

    def to_json(self):
        return {
            'type': 'StoryPartFork',
            'children': self.local_scope.to_json(),
        }

    def __repr__(self):
        return json.dumps(self.to_json())


@matchers.matcher()
class Switch:
    def __init__(self, cases):
        assert isinstance(cases, list)
        assert all(isinstance(i, tuple) for i in cases)
        self.cases = OrderedDict(cases)

    def validate(self, message):
        for case_id, validator in self.cases.items():
            if validator.validate(message):
                return case_id
        return None

    def serialize(self):
        return [{
                    'id': id,
                    'data': matchers.serialize(c),
                } for id, c in self.cases.items()]

    @staticmethod
    def deserialize(data):
        return Switch([(case['id'], matchers.deserialize(case['data']))
                       for case in data])

    def to_json(self):
        return {
            'type': 'Switch',
            'cases': self.serialize(),
        }

    def __repr__(self):
        return json.dumps(self.to_json())


class SwitchOnValue:
    """
    don't need to wait result
    """

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'SwitchOnValue({})'.format(self.value)


class ForkingStoriesAPI:
    def __init__(self, parser_instance):
        self.parser_instance = parser_instance

    def case(self,
             value=Undefined,
             validator=Undefined,
             default=Undefined,
             equal_to=Undefined,
             match=Undefined,
             ):
        def decorate(story_part):
            fork_node = self.parser_instance.get_last_story_part()
            if not isinstance(fork_node, StoryPartFork):
                fork_node = StoryPartFork()
                self.parser_instance.add_to_current_node(fork_node)

            compiled_story = self.parser_instance.compile_fork(fork_node, story_part)

            if default is True:
                compiled_story.extensions['default_case'] = True
            if equal_to is not Undefined:
                compiled_story.extensions['case_equal'] = equal_to
            if match is not Undefined:
                compiled_story.extensions['case_id'] = match
            if validator is not Undefined:
                compiled_story.extensions['validator'] = matchers.get_validator(validator)
            if value is not Undefined:
                compiled_story.extensions['validator'] = matchers.get_validator(value)
                compiled_story.extensions['case_equal'] = value

            return story_part

        return decorate
