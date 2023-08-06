# State [![support python versions](https://img.shields.io/pypi/pyversions/botstory.svg)](https://pypi.python.org/pypi/botstory/) [![PyPI version](https://img.shields.io/pypi/v/botstory.svg)](https://pypi.python.org/pypi/botstory/) [![Build Status](https://travis-ci.org/botstory/botstory.svg?branch=develop)](https://travis-ci.org/botstory/botstory) [![Coverage Status](https://coveralls.io/repos/github/botstory/botstory/badge.svg?branch=develop)](https://coveralls.io/github/botstory/botstory?branch=develop) [![](https://img.shields.io/pypi/l/botstory.svg)](https://github.com/botstory/botstory/blob/develop/LICENSE.txt)

Under active development. API could change so please follow for changes.

# Get Started

```python
import botstory
from botstory.integrations import aiohttp, fb, mongodb
import os


story = botstory.Story()

# setup modules

# facebook integration
story.use(fb.FBInterface(
    webhook_url='/webhook{}'.format(os.environ.get('FB_WEBHOOK_URL_SECRET_PART', '')),
    webhook_token=os.environ.get('FB_WEBHOOK_TOKEN', None),
))

# http interface 
story.use(aiohttp.AioHttpInterface(
    port=int(os.environ.get('PORT', 8080)),
))

# db interface
story.use(mongodb.MongodbInterface(
    uri=os.environ.get('MONGODB_URI', 'mongo'),
    db_name=os.environ.get('MONGODB_DB_NAME', 'todobot'),
))

# match user queries
@story.on('Hello')
def hello_story():
    @story.part()
    async def say_hi(ctx):
        await story.say('Hello {}!'.format(ctx['user'].name))
        
        
# start service 

asyncio.get_event_loop().run_until_complete(story.start())

```

# Features

- **Use frontier features of Python**
*Botstory is heavily based on brand new Python features, like async/await.
We always focus on its evolution and don't support legacy versions (<3.5).*

- **All messengers in one place**
*Right now botstory supports only fb Messengers, but we are going to 
support many others. So you can use common code base for different 
platform and seamlessly organize communication between them. As well 
we always open for contribution. And if you sure that one platform 
should be here, just drop PR with unit tests.*

- **More than 90% test coverage**
*Code is covered by tests except few trivial places. 
That way we are almost sure that any changes won't break other 
functionality. And any breaking features won't come hidden.*  

- **Declarative user dialogs**
*Match user queries, lead, fork and loop dialogs.*

- **Store use session**
*We remember user context and could return it any time and on any 
app instance. So you can scale app, and start and stop it without 
fair of bot amnesia.*

- **Easily scale**
*We focus on micro-services and especially on Docker. So you can 
very easy scale any part of the system.*

- **Open source**
*MIT licence gives you many rights. And we are very open for your 
contribution and would love to hear about your experience.*

and many other features

# News and Changelog

[CHANGELOG.md](CHANGELOG.md)

# Background

We are developing botstory mindful of the need to have easily reading API 
which describe dialogues (scenario) of bots in Python language.
Key problem is async nature of any dialog - 
we can wait answer from user for are months and should store context 
until that. As well dialog structure should be simply and clear 
and show sequence of questions and reactions. 
 
Sure dialog can be made in diagrams but my thought that code should 
clear enough to show story of dialog and should be open for modification.

As well it is too hard to use git for store versions of diagrams.

# Install

```bash
pip install botstory
```

# Examples

- [TODO bot](https://github.com/botstory/todo-bot) - support fb messenger

## Linear dialog

```python
"""
v0.0.63
Bot asks user about destination of space travelling.
- stateless story. it stores context of story (current question and results) somewhere (maybe DB)
"""
@story.on('lets go!')
def stateless_story():
    @story.part()
    async def ask_destination(ctx):
        return await story.ask('Where do you go?', 
                               user=ctx['user'])

    @story.part()
    async def ask_origin(ctx):
        store_destination(ctx['message']['location'])
        return await story.ask('Where do you now?', 
                               user=ctx['user'])

    @story.part()
    async def thanks(ctx):
        store_origin(ctx['message']['location'])
        return await story.say('Thanks!\n'
                               'Give me a minute I will find you right spaceship!', 
                               user=ctx['user'])
```

## Forking of Dialog (bifurcations)

```python
"""
v0.0.63
Bot asks user about destination of space travelling.
- stateless story. it stores context of story (current question and results) somewhere (maybe DB)
"""
@story.on('lets go!')
def stateless_story_with_bifurcation():
    @story.part()
    async def request_destination(ctx):
        return await story.ask('Where do you go?',
                               user=ctx['user'])

    @story.case('stars')
    def stars():
        @story.part()
        async def receive_destination_options(ctx):
            return await story.ask('Which star do you prefer?', 
                                   user=ctx['user'])

    @story.case('planets')
    def planets():
        @story.part()
        async def request_origin(ctx):
            return await story.ask('Which planet do you prefer?', 
                                   user=ctx['user'])

    @story.case(default=True)
    def other():
        @story.part()
        async def choose_from_top10_planets(ctx):
            return await choose_option(top10_planets,
                                       text='Here is the most popular places. Maybe you would like to choose one?',
                                       user=ctx['user'])

    @story.part()
    async def receive_destination(ctx):
        store_destination(ctx['message']['location'])
        return await story.say('Thanks! Give me a minute I will find you right spaceship!', 
                               user=ctx['user'])

```

## Reuse parts of Dialog (callable) and Dialog Loops

```python

from botstory.ast import callable, loop, story_context
from botstory.middlewares import option, sticker, text
import emoji
import logging
from todo import reflection


# Loop version
async def show_list_next_page(ctx):
    user_data = story_context.get_user_data(ctx)
    page_index = user_data.get('page_index', 0)
    list_title = user_data['list_title']
    title_field = user_data['title_field']
    page_length = user_data['page_length']
    list_type = user_data.get('list_type', 'pure')
    # render page of list ....


@story.callable()
def pagination_loop():
    @story.part()
    async def show_zero_page(ctx):
        if not await _show_list_next_page(ctx):
            return callable.EndOfStory()

    @story.loop()
    def list_loop():
        @story.on([
            option.Match('NEXT_PAGE_OF_A_LIST'),
            sticker.Like(),
            text.text.EqualCaseIgnore('more'),
            text.text.EqualCaseIgnore('next'),
        ])
        def next_page():
            @story.part()
            async def show_part_of_list(ctx):
                if not await show_list_next_page(ctx):
                    return loop.BreakLoop()
                return None


@story.on([
    text.EqualCaseIgnore('todo'),
])
def list_of_tasks_story():
    @story.part()
    async def list_of_tasks(ctx):
        logger.info('list of tasks')
        return await pagination_list.pagination_loop(
            ctx,
            subtitle_renderer=reflection.class_to_str(tasks_document.task_details_renderer),
            list_title='List of actual tasks:',
            list_type='template',
            page_length=os.environ.get('LIST_PAGE_LENGTH', 4),
            target_document=reflection.class_to_str(tasks_document.TaskDocument),
            title_field='description',
        )

```

# License

[MIT](LICENSE.txt)

# Contributing

Contributions of all sizes are welcome.

