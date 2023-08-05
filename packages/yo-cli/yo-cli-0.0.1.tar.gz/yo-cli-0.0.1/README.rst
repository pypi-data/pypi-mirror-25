Yo CLI
======

Introduction
------------

A simple command line service for the world's simplest messaging
service!

Commands
--------

Set Your API Key
~~~~~~~~~~~~~~~~

To send a ``Yo`` or check the existence of a user, you need to set your
API key.

``yo set_api_key`` ...and then follow the prompt

OR

``yo set_api_key --api_key={your_api_key_here}``

Send a ``Yo``
~~~~~~~~~~~~~

To send a ``Yo`` (assuming you've set your API Key)

``yo send`` ...and then follow the prompts for a recipient ``username``
and ``message``

OR

``yo send --username={some_username} --message={some_message} --link={some_optional_link}``

Check if a Username Exists
~~~~~~~~~~~~~~~~~~~~~~~~~~

To check if a username exists (assuming you've set your API Key)

``yo username_exists`` ...and then follow the prompts for the
``username`` in question

OR

``yo username_exists --username={some_username}``
