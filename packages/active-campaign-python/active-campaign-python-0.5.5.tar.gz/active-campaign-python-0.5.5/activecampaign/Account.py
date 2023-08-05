from .ActiveCampaign import (
    ActiveCampaign,
    fmt_params,
    fmt_noparams
)
import requests as rq


class Account(ActiveCampaign):

    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key
        ActiveCampaign.__init__(self, url, api_key)

    def add(self, params, post_data={}):
        rq_url = fmt_noparams(
            self.url,
            'account_add',
            self.output
        )
        response = rq.post(rq_url, data=post_data)
        return response.json()

    def cancel(self, params, post_data={}):
        rq_url = fmt_params(
            self.url,
            'account_cancel',
            self.output,
            params
        )
        response = rq.get(rq_url)
        return response.json()

    def edit(self, params, post_data={}):
        rq_url = fmt_noparams(
            self.url,
            'account_edit',
            self.output
        )
        response = rq.get(rq_url)
        return response.json()

    def list_(self, params, post_data={}):
        rq_url = fmt_params(
            self.url,
            'account_list',
            self.output,
            params
        )
        response = rq.get(rq_url)
        return response.json()

    def name_check(self, params, post_data={}):
        rq_url = fmt_params(
            self.url,
            'account_name_check',
            self.output,
            params
        )
        response = rq.get(rq_url)
        return response.json()

    def plans(self, params, post_data={}):
        rq_url = fmt_params(
            self.url,
            'account_plans',
            self.output,
            params
        )
        response = rq.get(rq_url)
        return response.json()

    def status(self, params, post_data={}):
        rq_url = fmt_params(
            self.url,
            'account_status',
            self.output,
            params
        )
        response = rq.get(rq_url)
        return response.json()

    def status_set(self, params, post_data={}):
        rq_url = fmt_params(
            self.url,
            'account_status_set',
            self.output,
            params
        )
        response = rq.get(rq_url)
        return response.json()

    def view(self, params, post_data={}):
        rq_url = fmt_noparams(
            self.url,
            'account_view',
            self.output
        )
        response = rq.get(rq_url)
        return response.json()


"""
    ## view
    #print ac.api('account/view')
"""
