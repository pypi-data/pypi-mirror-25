import json
from pprint import pprint
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from fbbot.bot import Bot

FB_VERIFY_TOKEN = "VERIFY_TOKEN_DEFINED_BY_DEVELOPER"
FB_PAGE_TOKEN = "FACEBOOK_PAGE_TOKEN"
BASE_URL = "URL_PROVIDED_FOR_NGROK" #example: https://12346578.ngrok.io or https://www.yourdomain.com


# HTTPRequestHandler class
class TestRequestHandler(BaseHTTPRequestHandler):
    myBot = Bot(FB_PAGE_TOKEN, BASE_URL)

    def do_GET(self):
        print(self.path)
        message = "default message"
        if self.path.startswith('/webhook'):
            query = urlparse(self.path).query
            query = dict(qc.split("=") for qc in query.split("&"))
            if 'hub.verify_token' in query and query['hub.verify_token'] == FB_VERIFY_TOKEN:
                message = query['hub.challenge']
            else:
                message = "Hello World, webhook enable"
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


def run():
    print('starting server...')
    server_address = ('127.0.0.1', 8080)
    httpd = HTTPServer(server_address, TestRequestHandler)
    print('running server...')
    httpd.serve_forever()

run()
