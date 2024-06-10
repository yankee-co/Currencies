import requests
import json
import sendgrid
import os
from sendgrid.helpers.mail import *

def load_data():
    URL = "https://api.privatbank.ua/p24api/exchange_rates?json&date=10.06.2024"

    response = requests.get(URL)  # Получаем данные от Приватбанка

    data = json.loads(response.text)  # Преобразовываем строку в словарь

    exchange_rates = data['exchangeRate']

    return '\n'.join(
        [
            "{}    {}    {}".format(
            rate['currency'],  # код валюты
            str(rate.get('purchaseRate', '-')).ljust(5, ' '),  # курс покупки
            str(rate.get('saleRate', '-')).ljust(5, ' '),  # курс продажи
            )
            for rate in exchange_rates
        ]
    )


    """
    CZK   12.599  13.5999
    CZK   12.599  13.5999
    CZK   12.599  13.5999
    """

if __name__ == '__main__':
    data = load_data()

    sg = sendgrid.SendGridAPIClient(api_key="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")
    from_email = Email("teacher@skillup.com.ua")
    to_email = To("zimae.9525@gmail.com")
    subject = "Our first email LOL"
    content = Content("text/plain", data)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body = mail.get())
