from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/info', methods=['GET'])
def info():
    number = request.args.get('number')

    if not number:
        return jsonify({'error': 'Missing number parameter'}), 400

    A = 'true'
    url = 'https://api.eyecon-app.com/app/getnames.jsp'

    params = {
        'cli': number,
        'lang': 'en',
        'is_callerid': A,
        'is_ic': A,
        'cv': 'vc_672_vn_4.2025.10.17.1932_a',
        'requestApi': 'URLconnection',
        'source': 'MenifaFragment'
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/87.0.4280.88 Safari/537.36',
        'accept': 'application/json',
        'e-auth-v': 'e1',
        'e-auth': 'c5f7d3f2-e7b0-4b42-aac0-07746f095d38',
        'e-auth-c': '40',
        'e-auth-k': 'PgdtSBeR0MumR7fO',
        'accept-charset': 'UTF-8',
        'content-type': 'application/x-www-form-urlencoded; charset=utf-8',
        'Host': 'api.eyecon-app.com',
        'Connection': 'Keep-Alive'
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=20)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({'error': f'API request failed: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
