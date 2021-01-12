from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

import requests
from datetime import date, timedelta

class HomePage(TemplateView):
    def get(self, *args, **kwargs):

        class Rate:
            def __init__(self, currency, value, date):
                self.currency = currency
                self.value = value
                self.date = date

        def AutomaticRating(dictionary):
            instance = Rate(
                currency = dictionary["cc"],
                value = round(dictionary["rate"], 2),
                date = dictionary["exchangedate"]
            )
            return instance

        today = date.today()
        request_date = ''.join(str(today).split('-'))
        request = requests.get(f'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?date={request_date}&json')
        data = [AutomaticRating(dictionary) for dictionary in request.json()]

        return render(
        request = self.request,
        template_name = 'home.html',
        context = {
        'data': data,
        'today':today,
        })
