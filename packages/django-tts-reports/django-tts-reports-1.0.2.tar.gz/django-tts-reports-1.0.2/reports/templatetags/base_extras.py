import json

from decimal import Decimal
from django import template

register = template.Library()


@register.simple_tag(name='middle_cost')
def middle_cost(units, rate, *args, **kwargs):
    mc = units * rate
    dmc = "{:.1f}".format(Decimal(mc))
    return dmc


@register.filter(name='load_json')
def load_json(arg):
    return json.loads(arg)


@register.simple_tag(name='role')
def role(dic, rle, ret, *args, **kwargs):
    com = list()
    total = list()

    if rle == "agent":
        for agent in dic:
            r = agent['role']
            if r == 'agent':
                com.append(agent['commission'])
                total.append(agent['pay_out'])
    elif rle == "NM":
        for agent in dic:
            r = agent['role']
            if r == 'network manager':
                com.append(agent['commission'])
                total.append(agent['pay_out'])
    elif rle == "TruTrade":
        for agent in dic:
            r = agent['role']
            if r == 'TruTrade':
                com.append(agent['commission'])
                total.append(agent['pay_out'])

    if ret == "perc":
        v = "{:.1f}".format(Decimal(sum(com)))  # to  one decimal place
    elif ret == "tt":
        v = "{:.1f}".format(Decimal(sum(total)))  # to  one decimal place

    return v


@register.simple_tag(name='total_bonus')
def total_bonus(amf, mcob, bonus, *args, **kwargs):
    x = amf/mcob  # number of kg
    y = x * bonus  # Total bonus
    tt_bonus = "{:.1f}".format(Decimal(y))  # to  one decimal place
    return tt_bonus


@register.simple_tag(name='total_bonus_share')
def total_bonus_share(value, *args, **kwargs):
    tt_bonus_share = value * 0.5
    return tt_bonus_share
