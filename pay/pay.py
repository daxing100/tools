import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# API URL mapping
API_URLS = {
    'qa': 'https://api-global-qa.moretickets.com/tool/auto_pay',
    'stage': 'https://api-global-stage.moretickets.com/tool/auto_pay'
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api_request', methods=['POST'])
def api_request():
    environment = request.json.get('environment')
    url = API_URLS.get(environment)

    trade_no = request.json.get('tradeNo')
    out_trade_no = request.json.get('outTradeNo')

    params = {
        'tradeNo': trade_no,
        'outTradeNo': out_trade_no
    }

    try:
        response = requests.get(url, params=params, verify=False)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='192.168.94.39', debug=True)
