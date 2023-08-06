# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your views here.
from decimal import Decimal

from django.shortcuts import get_object_or_404
from easy_pdf.views import PDFTemplateView
import services
import json

from models import ApiDomain


class HelloPDFView(PDFTemplateView):
    template_name = 'buyer-report.html'

    def get_context_data(self, **kwargs):

        deal_id = kwargs['uuid']

        host = get_object_or_404(ApiDomain, status=True)

        deal_object = services.get_deal_object(deal_id, host)
        souring = services.get_sourcing(deal_id, host)
        buyer = services.get_buyer(deal_id, host)
        middle_cost = services.get_middle_cost(deal_id, host)
        analysis = services.get_analysis(deal_id, host)

        df = json.loads(analysis['deal_defaults'])

        com = json.dumps(analysis['commodity_values'])
        cm = json.loads(com)

        mcost = list()

        for m in middle_cost:
            x = m['number_of_units'] * m['cost_per_unit']
            mcost.append(x)

        total_mcost = "{:.1f}".format(Decimal(sum(mcost)))

        seller_currency = ''
        for c in souring:
            currency = c['currency']
            seller_currency = currency['unit']
            break

        return super(HelloPDFView, self).get_context_data(
            pagesize="A4",
            title="Noah Kusaasira",
            deal_object=deal_object,
            commodity=souring,
            buyers=buyer,
            mc=middle_cost,
            serial=deal_id,
            analy=analysis,
            contingency=df['contingency'],
            tru_trade_commission=df['tru_trade_commission'],
            trade_and_insurance_fee=df['trade_and_insurance_fee'],
            total_mcost=total_mcost,
            seller_currency=seller_currency,
            agent_commissions=analysis['agent_commissions'],
            x=cm,
            **kwargs
        )
