import json
from pprint import pprint
import requests

from fbbot import element
from fbbot.wrappers import require_media_in


class Bot:
    def __init__(self, fb_page_token):
        self.FB_PAGE_TOKEN = fb_page_token
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
            self.receivedMessageAttachments(message_attachments, sender_id)

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
        if message_text == 'read receipt':
            self.sendReadReceipt(sender_id)
        elif message_text == 'typing on':
            self.sendTypingOn(sender_id)
        elif message_text == 'typing off':
            self.sendTypingOff(sender_id)
        else:
            self.sendTextMessage(sender_id, message_text)

    def receivedDeliveryConfirmation(self, message):
        pprint(message)
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
        watermark = message['read']['watermark']
        sequence_number = message['read']['seq']
        pprint("Received message read event for watermark " + watermark +
               " and sequence number " + sequence_number)

    def receivedAccountLink(self, message):
        sender_id = message['sender']['id']
        status = message['account_linking']['status']
        auth_code = message['account_linking']['authorization_code']
        pprint("Received account link event with for user " + sender_id +
               " with status " + status + " and auth code " + auth_code)

    # the index of media_type is 2 in sednMediaMessage function
    @require_media_in(2)
    def sendMediaMessage(self, recipient_id, media_type, static_media_url):
        msg_data = element.media(recipient_id, media_type, static_media_url)
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

    def sendReadReceipt(self, recipient_id):
        msg_data = element.action(recipient_id, "mark_seen")
        self.callSendAPI(msg_data)

    def sendTypingOn(self, recipient_id):
        msg_data = element.action(recipient_id, "typing_on")
        self.callSendAPI(msg_data)

    def sendTypingOff(self, recipient_id):
        msg_data = element.action(recipient_id, "typing_off")
        self.callSendAPI(msg_data)
