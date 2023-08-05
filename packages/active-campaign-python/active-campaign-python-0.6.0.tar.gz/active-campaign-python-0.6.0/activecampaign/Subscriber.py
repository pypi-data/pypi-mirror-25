from .ActiveCampaign import (
    ActiveCampaign,
    fmt_params,
)
import requests as rq


class Subscriber(ActiveCampaign):

    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key
        ActiveCampaign.__init__(self, url, api_key)

    def add(self, params, post_data):
        rq_url = fmt_params(
            self.url,
            'subscriber_add',
            self.output,
            params
        )
        response = rq.get(rq_url, data=post_data)
        return response.json()

    def delete(self, params, post_data={}):
        rq_url = fmt_params(
            self.url,
            'subscriber_delete',
            self.output,
            params
        )
        response = rq.get(rq_url)
        return response.json()

    def delete_list(self, params, post_data={}):
        rq_url = fmt_params(
            self.url,
            'subscriber_delete_list',
            self.output,
            params
        )
        response = rq.get(rq_url)
        return response.json()

    def edit(self, params, post_data):
        rq_url = fmt_params(
            self.url,
            'subscriber_edit',
            self.output,
            params
        )
        response = rq.get(rq_url, data=post_data)
        return response.json()

    def list_(self, params, post_data={}):
        rq_url = fmt_params(
            self.url,
            'subscriber_list',
            self.output,
            params
        )
        response = rq.get(rq_url)
        return response.json()

    def paginator(self, params, post_data={}):
        rq_url = fmt_params(
            self.url,
            'subscriber_paginator',
            self.output,
            params
        )
        response = rq.get(rq_url)
        return response.json()

    def sync(self, params, post_data):
        rq_url = fmt_params(
            self.url,
            'subscriber_sync',
            self.output,
            params
        )
        response = rq.get(rq_url, data=post_data)
        return response.json()

    def view(self, params, post_data={}):
        if params.startswith('email='):
            action = 'subscriber_view_email'
        elif params.startswith('hash='):
            action = 'subscriber_view_hash'
        elif params.startswith('id='):
            action = 'subscriber_view'
        else:
            action = 'subscriber_view'
        rq_url = fmt_params(
            self.url,
            action,
            self.output,
            params
        )
        response = rq.get(rq_url)
        return response.json()


"""
if __name__ == '__main__':
    ac = ActiveCampaign(ACTIVECAMPAIGN_URL,  ACTIVECAMPAIGN_API_KEY)

    ## add
##    subscriber = {
##        'email': 'person@example.com',
##        'first_name': 'John',
##        'last_name': 'Smith',
##        'p[1]': 1,
##        'status[1]': 1,
##    }
##    print ac.api('subscriber/add', subscriber)

    ## delete
##    print ac.api('subscriber/delete?id=10')

    ## delete_list
##    print ac.api('subscriber/delete_list?ids=9,11')

    ## edit
##    subscriber = {
##        'id': 12,
##        'email': 'person@example.com',
##        'first_name': 'Johnny',
##        'last_name': 'Smith',
##        'p[1]': 1,
##        'status[1]': 1
##    }
##    print ac.api('subscriber/edit', subscriber)

    ## list
##    print ac.api('subscriber/list?ids=1,12')

    ## paginator
##    print ac.api('subscriber/paginator?sort=&offset=0&limit=20&filter=0')

    ## sync
##    subscriber = {
##        'email': 'person@example.com',
##        'first_name': 'John',
##        'last_name': 'Smith',
##        'p[1]': 1,
##        'status[1]': 1,
##    }
##    print ac.api('subscriber/sync', subscriber)

    ## view id
##    print ac.api('subscriber/view?id=12')

    ## view email
##    print ac.api('subscriber/view?email=person@example.com')

    ## view hash
##    print ac.api('subscriber/view?hash=3eeda4735e93f5407fced5ed45ddae82')

"""
