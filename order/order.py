from flask import Flask, request, render_template, redirect, url_for
import requests

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        access_token = request.form['access_token']

        headers = {
            'user-agent': 'Dart/3.4 (dart:io)',
            'content-type': 'application/json; charset=utf-8',
            'cc': 'HKD',
            'oc': 'MTS',
            'lan': 'zh-HK',
            'code': 'NATIVE',
            'src': 'IOS',
            'access_token': access_token,
            'host': 'api-global-qa.moretickets.com',
            'locationid': '663b19ccfdd9dc0001f56043',
            'lc': 'SG',
        }

        json_data = {
            'showId': '670496e7940c4c0001d49776',
            'sessionId': '6705ee24863a4700013a111e',
            'inventoryId': '67063d9cfa8a750001a56a64',
            'qty': 1,
            'consecutive': False,
            'delivery': {
                'addressId': '66c2bbdae20bd4000157f186',
                'email': 'hanxing@morefungroup.com',
                'receiver': '',
                'phoneCode': '',
                'cellphone': '',
                'postalCode': '',
                'countryCode': 'SG',
                'countryName': '',
                'cityName': '',
                'address': '',
                'addressOptional': '',
                'deliverMethod': 'SELF_PICKUP',
            },
            'tradeAmount': {
                'payableAmount': 23.0,
                'ticketAmount': 11.0,
                'serviceFee': 12.0,
                'vat': 0.0,
                'discountAmount': 0.0,
                'transactionCurrency': 'HKD',
            },
            'displayAmount': {
                'payableAmount': 23.0,
                'ticketAmount': 11.0,
                'serviceFee': 12.0,
                'vat': 0.0,
                'exchangeRate': 1.0,
                'discountAmount': 0.0,
                'transactionCurrency': 'HKD',
            },
            'sectorId': '6705ee24863a4700013a1121',
            'zoneId': '6705ee24863a4700013a1122',
        }

        response = requests.post('https://api-global-qa.moretickets.com/user/order/v1/create', headers=headers,
                                 json=json_data)
        orderId = response.json().get('data', {}).get('orderId')

        json_data = {'orderId': orderId}
        response = requests.post('https://api-global-qa.moretickets.com/user/order/v1/pay_fees', headers=headers,
                                 json=json_data)
        payMethod = response.json().get('data', {}).get('payMethods', [{}])[0].get('payMethod')
        tradId = response.json().get('data', {}).get('tradeId')

        json_data = {
            'orderId': orderId,
            'tradeId': tradId,
            'payMethod': payMethod
        }
        response = requests.post('https://api-global-qa.moretickets.com/user/order/v1/prepay', headers=headers,
                                 json=json_data)
        paymentOrderNo = response.json().get('data', {}).get('paymentOrderNo')

        params = {
            'tradeNo': paymentOrderNo,
            'outTradeNo': paymentOrderNo
        }

        response = requests.get('https://api-global-qa.moretickets.com/tool/auto_pay', params=params)

        return response.json()

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='192.168.94.39',port='50001', debug=True)
