from importlib import import_module
from .Connector import Connector

# formatters for making life easier, don't you want it that way?
fmt_params = '{}&api_action={}&api_output={}&{}'.format
fmt_noparams = '{}&api_action={}&api_output={}'.format


def get_mod(cls, parent):
    source_module = import_module(".{}".format(cls), parent)
    class1 = getattr(source_module, cls)  # get Subscriber
    return class1


class ActiveCampaign(Connector):

    def __init__(self, url, api_key, api_user='', api_pass=''):
        self.url = url
        self.api_key = api_key
        self.URL = url
        self.APIKEY = api_key
        Connector.__init__(self, url, api_key, api_user, api_pass)

    def api(self, path, post_data={}):
        # IE: "contact/view"
        components = path.split('/')
        component = components[0]

        if '?' in components[1]:
            # query params appended to method
            # IE: contact/edit?overwrite=0
            method_arr = components[1].split('?')
            method = method_arr[0]
            params = method_arr[1]
        else:
            # just a method provided
            # IE: "contact/view
            if components[1]:
                method = components[1]
                params = ''
            else:
                return 'Invalid method.'

        # adjustments
        if component == 'branding':
            # reserved word
            component = 'design'
        elif component == 'sync':
            component = 'contact'
            method = 'sync'
        elif component == 'singlesignon':
            component = 'auth'

        # "contact" becomes "Contact"
        class1 = '{}'.format(component.capitalize())
        class1 = get_mod(class1, 'activecampaign')
        class1 = class1(self.URL, self.APIKEY)  # Subscriber()

        if method == 'list':
            # reserved word
            method = 'list_'

        if method in dir(class1):
            return getattr(class1, method)(params, post_data)
        return None
