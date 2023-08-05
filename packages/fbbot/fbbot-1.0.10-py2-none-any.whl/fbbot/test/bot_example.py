import json
from pprint import pprint
import requests
import uuid

from fbbot import element
from fbbot.templates import ButtonTemplate, GenericTemplate

class Bot:
    def __init__(self, fb_page_token, base_url):
        self.FB_PAGE_TOKEN = fb_page_token
        self.BASE_URL = base_url
        self.API_VERSION = 'v2.6'
        self.message_type_functions = {'optin': self.receivedAuthentication,
                                       'message': self.receivedMessage,
                                       'delivery': self.receivedDeliveryConfirmation,
                                       'postback': self.receivedPostback,
                                       'read': self.receivedMessageRead,
                                       'account_linking': self.receivedAccountLink,
                                       }

    def get_user_info(self, fbid):
        user_url = "https://graph.facebook.com/v2.6/%s" % fbid
        user_params = {'fields': 'first_name,last_name,profile_pic',
                       'access_token': self.FB_PAGE_TOKEN}
        user_details = requests.get(user_url, user_params).json()
        pprint(user_details)
        return user_details

    def callSendAPI(self, msg_data):
        post_message_url = 'https://graph.facebook.com/' + self.API_VERSION + \
                           '/me/messages?access_token=' + self.FB_PAGE_TOKEN
        pprint(post_message_url)
        status = requests.post(post_message_url,
                               headers={"Content-Type": "application/json"},
                               data=json.dumps(msg_data))
        status_body = status.json()
        if status.status_code == 200:
            recipient_id = status_body['recipient_id']
            if 'message_id' in status_body:
                message_id = status_body['message_id']
                pprint("Successfully sent message with id " + message_id +
                       " to recipient " + recipient_id)
            else:
                pprint("Successfully called Send API for recipient " +
                       recipient_id)
        else:
            pprint(status_body)

    def receivedAuthentication(self, message):
        sender_id = message['sender']['id']
        recipient_id = message['recipient']['id']
        time_of_auth = message['timestamp']
        pass_through_param = message['optin']['ref']
        pprint("Received authentication for user " + sender_id + " and page " +
               recipient_id + " with pass " + "through param '" +
               pass_through_param + "' at " + repr(time_of_auth))
        self.sendTextMessage(sender_id, "Authentication successful")

    def receivedMessage(self, message):
        sender_id = message['sender']['id']
        recipient_id = message['recipient']['id']
        time_of_message = message['timestamp']
        received_message = message['message']
        pprint("Received message for user " + sender_id + " and page " +
               recipient_id + " at " + repr(time_of_message) +
               " with message:")
#        pprint(message)
#        pprint(received_message)
        is_echo = received_message['is_echo'] if 'is_echo' in received_message else False
        message_attachments = received_message['attachments'] if 'attachments' in received_message else False
        message_text = received_message['text'] if 'text' in received_message else False
        quick_reply = received_message['quick_reply'] if 'quick_reply' in received_message else False
        if is_echo:
            self.receivedMessageEcho(received_message)
            return
        elif quick_reply:
            self.receivedMessageQuickReply(received_message, sender_id)
            return
        if message_text:
            self.receivedMessageText(message_text, sender_id)
        elif message_attachments:
            self.receivedMessageAttachments(sender_id)

    def receivedMessageEcho(self, received_message):
        app_id = received_message['app_id'] if 'app_id' in received_message else ""
        metadata = received_message['metadata'] if 'metadata' in received_message else ""
        message_id = received_message['mid'] if 'mid' in received_message else ""
        pprint("Received echo for message " + message_id + " and app " +
               app_id + " with metadata " + metadata)

    def receivedMessageQuickReply(self, received_message, sender_id):
        message_id = received_message['mid'] if 'mid' in received_message else ""
        quick_reply = received_message['quick_reply'] if 'quick_reply' in received_message else False
        quick_reply_payload = quick_reply['payload']
        pprint("Quick reply for message " + message_id + " with payload " +
               quick_reply_payload)
        self.sendTextMessage(sender_id, "Quick reply tapped")

    def receivedMessageAttachments(self, message_attachments, sender_id):
        self.sendTextMessage(sender_id, "Message with attachment received")

    def receivedMessageText(self, message_text, sender_id):
        if message_text == 'image':
            self.sendImageMessage(sender_id, "fbbot/python.png")
        elif message_text == 'gif':
            self.sendGifMessage(sender_id, "fbbot/falling_down.gif")
        elif message_text == 'audio':
            self.sendAudioMessage(sender_id, "fbbot/sample.mp3")
#        elif message_text == 'video':
#            sendVideoMessage(sender_id,"fbbot/animal.mp4")
        elif message_text == 'file':
            self.sendFileMessage(sender_id, "fbbot/test.txt")
        elif message_text == 'button':
            self.sendButtonMessage(sender_id)
        elif message_text == 'generic':
            self.sendGenericMessage(sender_id)
        elif message_text == 'receipt':
            self.sendReceiptMessage(sender_id)
        elif message_text == 'quick reply':
            self.sendQuickReply(sender_id)
        elif message_text == 'read receipt':
            self.sendReadReceipt(sender_id)
        elif message_text == 'typing on':
            self.sendTypingOn(sender_id)
        elif message_text == 'typing off':
            self.sendTypingOff(sender_id)
        elif message_text == 'account linking':
            self.sendAccountLinking(sender_id)
        else:
            self.sendTextMessage(sender_id, message_text)

    def receivedDeliveryConfirmation(self, message):
        pprint(message)
#        senderID = message['sender']['id']
#        recipientID = message['recipient']['id']
#        secuenceNumber = delivery['seq']
        delivery = message['delivery']
        message_ids = delivery['mids']
        watermark = delivery['watermark']
        if message_ids:
            for messageID in message_ids:
                pprint("Received delivery confirmation for message ID: " +
                       messageID)
        pprint("All message before " + repr(watermark) + " were delivered.")

    def receivedPostback(self, message):
        sender_id = message['sender']['id']
        recipient_id = message['recipient']['id']
        time_of_postback = message['timestamp']
        payload = message['postback']['payload']
        pprint("Received postback for user " + sender_id + " and page " +
               recipient_id + " with payload '" + payload + "' " + "at " +
               repr(time_of_postback))
        self.sendTextMessage(sender_id, "Postback called")

    def receivedMessageRead(self, message):
        pprint(message)
#        senderID = message['sender']['id']
#        recipientID = message['recipient']['id']
        watermark = message['read']['watermark']
        sequence_number = message['read']['seq']
        pprint("Received message read event for watermark " + watermark +
               " and sequence number " + sequence_number)

    def receivedAccountLink(self, message):
        sender_id = message['sender']['id']
#        recipientID = message['recipient']['id']
        status = message['account_linking']['status']
        auth_code = message['account_linking']['authorization_code']
        pprint("Received account link event with for user " + sender_id +
               " with status " + status + " and auth code " + auth_code)

    def sendImageMessage(self, recipient_id, static_img_url):
        msg_data = element.media(recipient_id, "image", static_img_url)
        self.callSendAPI(msg_data)

    def sendGifMessage(self, recipient_id, static_img_url):
        msg_data = element.media(recipient_id, "image", static_img_url)
        self.callSendAPI(msg_data)

    def sendAudioMessage(self, recipient_id, static_audio_url):
        msg_data = element.media(recipient_id, "audio", static_audio_url)
        self.callSendAPI(msg_data)

    def sendVideoMessage(self, recipient_id, static_video_url):
        msg_data = element.media(recipient_id, "video", static_video_url)
        self.callSendAPI(msg_data)

    def sendFileMessage(self, recipient_id, static_file_url):
        msg_data = element.media(recipient_id, "file", static_file_url)
        self.callSendAPI(msg_data)

    def sendTextMessage(self, recipient_id, message_text,
                        metadata="DEVELOPER_DEFINED_METADATA"):
        msg_data = {
            'recipient': {
                'id': recipient_id
            },
            'message': {
                'text': message_text,
                'metadata': metadata
            }
        }
        self.callSendAPI(msg_data)

    def sendButtonMessage(self, recipient_id):
        text = "This is test text"
        buttons = [
            element.button("web_url", "Open Web URL",
                           "https://www.oculus.com/en-us/rift/"),
            element.button("postback", "Trigger Postback",
                           "DEVELOPER_DEFINED_PAYLOAD"),
            element.button("phone_number", "Call Phone Number", "+55555555555")
        ]
        template = ButtonTemplate(recipient_id, text, buttons)
        msg_data = template.get_data()
        self.callSendAPI(msg_data)

    def sendGenericMessage(self, recipient_id):
#       make button for first element in template
        btns1 = [
            element.button("web_url", "Open Web URL",
                           "https://en.wikipedia.org/wiki/The_Hitchhiker%27s_Guide_to_the_Galaxy"),
            element.button("postback", "Call Postback",
                           "Payload for first bubble"),
        ]
#       make first element for template with btns1
        elmnt1 = element.element("42", "Next-generation guides",
                                 "https://en.wikipedia.org/wiki/The_Hitchhiker%27s_Guide_to_the_Galaxy",
                                 "https://localhost/static/fbbot/falling_down.gif",
                                 btns1)
#       make template with elements list
        template = GenericTemplate(recipient_id, [elmnt1])
#       adding a new element for template
        elmnt2 = template.add_element("books", "books collection",
                                      "https://www.books.com/",
                                      "https://localhost/fbbot/books.png")
#       adding buttons for elmnt2
        template.add_button_to(elmnt2, "web_url", "Open Web URL",
                               "https://www.oculus.com/en-us/touch/")
        template.add_button_to(elmnt2, "postback", "Call Postback",
                               "Payload for second bubble")
#       get data in template for callSendAPI
        msg_data = template.get_data()
        self.callSendAPI(msg_data)

    def sendReceiptMessage(self, recipient_id):
        receipt_id = uuid.uuid4().hex.upper()
        msg_data = {
            'recipient': {
                'id': recipient_id
            },
            'message': {
                'attachment': {
                    'type': "template",
                    'payload': {
                        'template_type': "receipt",
                        'recipient_name': "Peter Chang",
                        'order_number': receipt_id,
                        'currency': "USD",
                        'payment_method': "Visa 1234",
                        'timestamp': "1428444852",
                        'elements': [{
                            'title': "Surprise package",
                            'subtitle': "Includes: mistery item1, item2, item3",
                            'quantity': 1,
                            'price': 599.00,
                            'currency': "USD",
                            'image_url': self.BASE_URL + static("fbbot/surprise_pkg.png")
                        }, {
                            'title': "Books collection",
                            'subtitle': "Paper version",
                            'quantity': 1,
                            'price': 99.99,
                            'currency': "USD",
                            'image_url': self.BASE_URL + static("fbbot/books.png")
                        }],
                        'address': {
                            'street_1': "1 Hacker Way",
                            'street_2': "",
                            'city': "Menlo Park",
                            'postal_code': "94025",
                            'state': "CA",
                            'country': "US"
                        },
                        'summary': {
                            'subtotal': 698.99,
                            'shipping_cost': 20.00,
                            'total_tax': 57.67,
                            'total_cost': 626.66
                        },
                        'adjustments': [{
                            'name': "New Customer Discount",
                            'amount': -50
                        }, {
                            'name': "$100 Off Coupon",
                            'amount': -100
                        }]
                    }
                }
            }
        }
        self.callSendAPI(msg_data)

    def sendQuickReply(self, recipient_id):
        msg_data = {
            'recipient': {
                'id': recipient_id
            },
            'message': {
                'text': "What's your favorite movie genre?",
                'quick_replies': [
                    {
                        "content_type": "text",
                        "title": "Action",
                        "payload": "DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_ACTION"
                    },
                    {
                        "content_type": "text",
                        "title": "Comedy",
                        "payload": "DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_COMEDY"
                    },
                    {
                        "content_type": "text",
                        "title": "Drama",
                        "payload": "DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_DRAMA"
                    }
                ]
            }
        }
        self.callSendAPI(msg_data)

    def sendReadReceipt(self, recipient_id):
        msg_data = {
            'recipient': {
                'id': recipient_id
            },
            'sender_action': "mark_seen"
        }
        self.callSendAPI(msg_data)

    def sendTypingOn(self, recipient_id):
        msg_data = {
            'recipient': {
                'id': recipient_id
            },
            'sender_action': "typing_on"
        }
        self.callSendAPI(msg_data)

    def sendTypingOff(self, recipient_id):
        msg_data = {
            'recipient': {
                'id': recipient_id
            },
            'sender_action': "typing_off"
        }
        self.callSendAPI(msg_data)

    def sendAccountLinking(self, recipient_id):
        msg_data = {
            'recipient': {
                'id': recipient_id
            },
            'message': {
                'attachment': {
                    'type': "template",
                    'payload': {
                        'template_type': "button",
                        'text': "Welcome. Link your account.",
                        'buttons': [{
                            'type': "account_link",
                            'url': self.BASE_URL + "/admin"
                        }]
                    }
                }
            }
        }
        self.callSendAPI(msg_data)
