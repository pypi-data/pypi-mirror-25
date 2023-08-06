from .ActiveCampaign import (
    ActiveCampaign,
    fmt_params,
    fmt_noparams
)
import requests as rq


class Contact(ActiveCampaign):

    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key
        ActiveCampaign.__init__(self, url, api_key)

    def add(self, params, post_data={}):
        if params:
            rq_url = fmt_params(self.url, 'contact_add', self.output, params)
        else:
            rq_url = fmt_noparams(self.url, 'contact_add',
                                  self.output)
        response = rq.post(rq_url, data=post_data)
        return response

    def automation_list(self, params):
        rq_url = fmt_params(self.url, 'contact_add',
                            self.output, params)
        response = rq.post(rq_url)
        return response

    def delete_list(self, params):
        rq_url = fmt_params(self.url, 'contact_delete_list',
                            self.output, params)
        response = rq.get(rq_url)
        return response

    def delete(self, params):
        rq_url = fmt_params(self.url, 'contact_delete',
                            self.output, params)
        response = rq.get(rq_url)
        return response

    def edit(self, params, post_data={}):
        rq_url = fmt_noparams(self.url, 'contact_edit', self.output)
        response = rq.post(rq_url, data=post_data)
        return response

    def list_(self, params):
        rq_url = fmt_params(self.url, 'contact_list',
                            self.output, params)
        response = rq.get(rq_url)
        return response

    def note_add(self, params, post_data={}):
        rq_url = fmt_params(self.url, 'contact_note_add',
                            self.output, params)
        response = rq.post(rq_url, data=post_data)
        return response

    def note_edit(self, params, post_data={}):
        rq_url = fmt_params(self.url, 'contact_note_edit',
                            self.output, params)
        response = rq.post(rq_url, data=post_data)
        return response

    def note_delete(self, params):
        rq_url = fmt_noparams(self.url, 'contact_note_delete', self.output)
        response = rq.post(rq_url)
        return response

    def paginator(self, params):
        rq_url = fmt_params(self.url, 'contact_paginator',
                            self.output, params)
        response = rq.get(rq_url)
        return response

    def sync(self, params, post_data):
        if params:
            rq_url = fmt_params(self.url, 'contact_sync',
                                self.output, params)
        else:
            rq_url = fmt_noparams(self.url, 'contact_sync', self.output)
        response = rq.post(rq_url, data=post_data)
        return response

    def tag_add(self, params, post_data={}):
        if params:
            rq_url = fmt_params(self.url, 'contact_tag_add',
                                self.output, params)
        else:
            rq_url = fmt_noparams(self.url, 'contact_tag_add', self.output)
        response = rq.post(rq_url, data=post_data)
        return response

    def tag_remove(self, params, post_data={}):
        if params:
            rq_url = fmt_params(self.url, 'contact_tag_remove',
                                self.output, params)
        else:
            rq_url = fmt_noparams(self.url, 'contact_tag_remove', self.output)
        response = rq.post(rq_url, data=post_data)
        return response

    def view(self, params, post_data={}):
        if params.startswith('email='):
            action = 'contact_view_email'
        elif params.startswith('hash='):
            action = 'contact_view_hash'
        elif params.startswith('id='):
            action = 'contact_view'
        else:
            action = 'contact_view'
        rq_url = fmt_params(self.url, action,
                            self.output, params)
        response = rq.get(rq_url)
        return response

        ## extra methods I created for shorthand scripting
        # get
        def _get_contact_by_id(self, cid=None):
            """Get a contact by ID

            Arguments:
                cid:str     contact/subscriber ID
            """
            response = self.api('contact/view?id={}'.format(cid))
            return response

        def _get_contact_by_email(self, email=None):
            """Get a contact by email

            Arguments:
                email:str     contact/company Email
            """
            response = self.api('contact/view?email={}'.format(email))
            return response

        # delete
        def _delete_contact_by_id(self, cid=None):
            """Delete a contact/company

            Arguments:
                cid:str     contact/susbscriber ID
            """
            response = self.api('contact/delete?id={}'.format(cid))
            return response

        # create
        def _create_contact(self, data=None):
            """Create a contact/company

            Arguments:
                data:dict   proper definition of a contact dict
            """
            response = self.api('contact/ad', post_data=data)
            return response
        ## end contact section

        # create
        def _add_tags_by_id(self, cid=None, tags=None):
            """ Add tags by id for company/contact

            Arguments:
                cid:str         contact/susbscriber ID
                tags:list(str)  list of tags as strings
            """
            if not isinstance(tags, list):
                raise AttributeError("tags must be a list of strings")
            response = self.api('contact/tag_add?id={}'.format(cid),
                                post_data={'tags':tags})
            return self._response

        # delete
        def _delete_tags_by_id(self, cid=None, tags=None):
            """ Delete a tag by a contact/susbscriber ID

            Arguments:
                cid:str         contact/susbscriber ID
                tags:list(str)  list of tags as strings
            """
            if not isinstance(tags, list):
                raise AttributeError("tags must be a list of strings")
            response = self.api('contact/tag_remove?id={}'.format(cid),
                                post_data={'tags':tags})
            return self._response

        def _add_note_by_id(self, cid=None, note=""):
            """ Add a Note for a contact/company

            Arguments:
                cid:str     contact/susbscriber ID
                note:str    a note
            """
            data = {"id": cid, "note":note}
            response = self.api('contact/note_add?id={}'.format(cid),
                                post_data=data)
            return response

        # delete
        def _delete_note_by_id(self, nid=None):
            """ Delete a note by a note ID

            Arguments:
                nid:str     note ID to delete
            """
            response = self.api('contact/note_delete?noteid={}'.format(nid))
            return response
        ## end contact components (properties, tags...)


"""
if __name__ == '__main__':
    ac = ActiveCampaign(ACTIVECAMPAIGN_URL,  ACTIVECAMPAIGN_API_KEY)

    ## add
##    user = {
##        'username': 'johnsmith',
##        'first_name': 'John',
##        'last_name': 'Smith',
##        'password': 'mypwd',
##        'password_r': 'mypwd',
##        'email': 'person@example.com',
##        'group[3]' : 3
##    }
##    print ac.api('user/add', user)

    ## delete_list
##    print ac.api('user/delete_list?ids=3,4')

    ## delete
##    print ac.api('user/delete?id=5')

    ## edit
##    user = {
##        'username': 'johnsmith',
##        'first_name': 'John',
##        'last_name': 'Smyth',
##        'password': 'mynwqpwd',
##        'password_r': 'mynewpwd',
##        'email': 'person@example.com',
##        'group[3]' : 3,
##        'id' : 6
##    }
##    print ac.api('user/edit', user)

    ## list
##    print ac.api('user/list?ids=1,6')

    ## me
##    print ac.api('user/me')

    ## view email
##    print ac.api('user/view?email=person@example.com')

    ## view username
##    print ac.api('user/view?username=johnsmith')

    ## view id
##    print ac.api('user/view?id=1')

    ## sync
##    contact = {
##        'email': 'person@example.com',
##        'first_name': 'John',
##        'last_name': 'Smith',
##        'p[1]': 1,
##        'status[1]': 1,
##    }
##    print ac.api('contact/sync', contact)

"""
