from __future__ import unicode_literals

import requests


x = '18e1bd6052df1a1d62c428f862c942bed6a12726'
headers = {'Authorization': 'token %s' % x}


def get_deal_object(deal_id, host):
    r = requests.get('{}{}{}'.format(host, '/api.micro/deal/', deal_id), headers=headers)
    deal_object = r.json()
    return deal_object


def get_sourcing(deal_id, host):
    params = {'deal_id': deal_id}
    r = requests.get('{}{}'.format(host, '/api/deal-commodities'), params=params, headers=headers)
    sourcing_information = r.json()
    return sourcing_information


def get_buyer(deal_id, host):
    params = {'deal_id': deal_id}
    r = requests.get('{}{}'.format(host, '/api/deal-buyers'), params=params, headers=headers)
    buyer_information = r.json()
    return buyer_information


def get_middle_cost(deal_id, host):
    params = {'deal_id': deal_id}
    r = requests.get('{}{}'.format(host, '/api/deal-middle-costs'), params=params, headers=headers)
    middle_cost_information = r.json()
    return middle_cost_information


def get_analysis(deal_id, host):
    params = {'raw': 1}
    url = '{}/{}'.format('{}{}'.format(host, '/analysis'), deal_id)
    r = requests.get(url, params=params, headers=headers)
    deal_analysis = r.json()
    return deal_analysis

