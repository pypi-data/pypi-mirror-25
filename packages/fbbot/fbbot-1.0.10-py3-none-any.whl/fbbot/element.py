def action(recipient_id, action_type):
    return {
        'recipient': {
            'id': recipient_id
        },
        'sender_action': action_type
    }


def media(recipient_id, media_type, static_url):
    return {
        'recipient': {
            'id': recipient_id
        },
        'message': {
            'attachment': {
                'type': media_type,
                'payload': {
                    'url': static_url
                }
            }
        }
    }


def template(recipient_id, payload):
    return {
        'recipient': {
            'id': recipient_id
        },
        'message': {
            'attachment': {
                'type': "template",
                'payload': payload
            }
        }
    }


def button(button_type, title, metadata):
    btn_data = {
        'type': button_type,
        'title': title,
    }
    if button_type == 'web_url':
        btn_data['url'] = metadata
    else:
        btn_data['payload'] = metadata
    return btn_data


def element(title, subtitle, item_url, image_url, buttons):
    return {
        'title': title,
        'subtitle': subtitle,
        'item_url': item_url,
        'image_url': image_url,
        'buttons': buttons
    }
