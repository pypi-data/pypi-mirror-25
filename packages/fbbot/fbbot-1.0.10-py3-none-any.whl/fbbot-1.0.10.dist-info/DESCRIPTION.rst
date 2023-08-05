===============================
Facebook Messenger Bot : fbbot
===============================

fbbot is a sim1ple bot class to showcasing the Messenger Platform, make your facebook bot with django-fbbot

Install
----------------------------------------

1. Install **fbbot** package with python-pip::

    pip install fbbot

2. Create a simple echo bot 'my_fbbot.py'::

    from fbbot.test import simpleEchoBot

    FB_VERIFY_TOKEN = "VERIFY_TOKEN_DEFINED_BY_DEVELOPER"
    FB_PAGE_TOKEN = "FACEBOOK_PAGE_TOKEN"

    simpleEchoBot.run(FB_VERIFY_TOKEN, FB_PAGE_TOKEN, port="8000")


5. Run `python3 my_fbbot.py`.

6. Start the development server and visit http://127.0.0.1:8000/webhook

7. Visit http://127.0.0.1:8000/webhook and see "Hello World, webhook enable"

8. Send a message to your facebook page and the fbbot send the same text::

            Hello! :User
    Bot: Hello!
             Echo! :User
    Bot: Echo!

Uninstall
--------------------------------------------

1. If you want to uninstall this package run::

    pip uninstall fbbot



