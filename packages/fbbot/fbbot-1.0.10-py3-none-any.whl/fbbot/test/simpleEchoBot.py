#!/usr/bin/env python


import sys
sys.path.append('../../')

import json
from pprint import pprint
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from fbbot.bot import Bot

#FB_VERIFY_TOKEN = "VERIFY_TOKEN_DEFINED_BY_DEVELOPER"
#FB_PAGE_TOKEN = "FACEBOOK_PAGE_TOKEN"


def make_handler_with_tokens(verify_token, page_token, bot=None):
    # HTTPRequestHandler class
    class TestRequestHandler(BaseHTTPRequestHandler):
        if bot:
            myBot = bot
        else:
            myBot = Bot(page_token)

        def do_GET(self):
            print(self.path)
            message = "default message"
            if self.path.startswith('/webhook'):
                query = urlparse(self.path).query
                try:
                    query = dict(qc.split("=") for qc in query.split("&"))
                    if 'hub.verify_token' in query and query['hub.verify_token'] == verify_token:
                        message = query['hub.challenge']
                    else:
                        message = "Hello World, webhook enable"
                except Exception as e:
                    message = "Hello World, webhook enable :: ERROR :: " + repr(e)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(message, "utf8"))
            return

        def do_POST(self):
            if self.path.startswith('/webhook'):
                content_len = int(self.headers.get('Content-Length'))
                post_body = self.rfile.read(content_len)
                pprint(":: post_body ::")
                pprint(post_body)
                incoming_message = json.loads(str(post_body, 'utf-8'))
                if 'object' in incoming_message and incoming_message['object'] == 'page':
                    for entry in incoming_message['entry']:
                        for message in entry['messaging']:
                            pprint(":: message ::")
                            pprint(message)
                            for message_type in self.myBot.message_type_functions:
                                if message_type in message:
                                    self.myBot.message_type_functions[message_type](message)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes("ok", "utf8"))
            return
    return TestRequestHandler


def run(verify_token=None, page_token=None, port=8080, bot=None):
    if not verify_token:
        raise KeyError("'verify_token' is required: 'VERIFY_TOKEN_DEFINED_BY_DEVELOPER'")
    if not page_token:
        raise KeyError("'page_token' is required: 'FACEBOOK_PAGE_TOKEN'")
    print('starting server...')
    server_address = ('127.0.0.1', port)
    request_handler = make_handler_with_tokens(verify_token, page_token, bot=bot)
    httpd = HTTPServer(server_address, request_handler)
    print('running server...')
    httpd.serve_forever()
