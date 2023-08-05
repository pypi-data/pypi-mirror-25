from fbbot import element


class ButtonTemplate:
    """docstring for ButtonTemplate"""
    def __init__(self, recipient_id, text, buttons=[]):
        self.recipient_id = recipient_id
        self.text = text
        self.buttons = buttons

    def add_button(self, button_type, title, metadata):
        self.buttons.append(
            element.button(button_type, title, metadata))

    def get_data(self):
        payload = {
            'template_type': "button",
            'text': self.text,
            'buttons': self.buttons
        }
        return element.template(self.recipient_id, payload)


class GenericTemplate:
    """docstring for GenericTemplate"""
    def __init__(self, recipient_id, elements=[]):
        self.recipient_id = recipient_id
        self.elements = elements

    def add_element(self, title, subtitle, item_url, image_url, buttons=[]):
        self.elements.append(
            element.element(title, subtitle, item_url, image_url, buttons))
        return self.elements[-1]

    def add_button_to(self, element_ref, button_type, title, metadata):
        index = self.elements.index(element_ref)
        self.elements[index]['buttons'].append(
            element.button(button_type, title, metadata))
        return self.elements[index]['buttons'][-1]

    def add_button_by_element_index(self, index, button_type, title, metadata):
        self.elements[index]['buttons'].append(
            element.button(button_type, title, metadata))
        return self.elements[index]['buttons'][-1]

    def get_data(self):
        payload = {
            'template_type': "generic",
            'elements': self.elements
        }
        return element.template(self.recipient_id, payload)
