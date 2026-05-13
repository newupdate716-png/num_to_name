from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/info', methods=['GET'])
def info():
    # ইউজার থেকে নম্বর নেওয়া
    number = request.args.get('number')

    if not number:
        return jsonify({
            'status': 'error',
            'message': 'Missing number parameter'
        }), 400

    # নম্বর ফরম্যাট ক্লিন করা (প্লাস চিহ্ন থাকলে হ্যান্ডেল করা)
    target_number = number.replace(' ', '').replace('+', '')

    url = 'https://api.eyecon-app.com/app/getnames.jsp'

    params = {
        'cli': target_number,
        'lang': 'en',
        'is_callerid': 'true',
        'is_ic': 'true',
        'cv': 'vc_672_vn_4.2025.10.17.1932_a',
        'requestApi': 'URLconnection',
        'source': 'MenifaFragment'
    }

    # আপডেট করা হেডার্স (অবশ্যই চেক করবেন আপনার সেশন কী সচল কি না)
    headers = {
        'User-Agent': 'Eyecon/4.0.511 (Android/10; SM-A505F)',
        'accept': 'application/json',
        'e-auth-v': 'e1',
        'e-auth': 'c5f7d3f2-e7b0-4b42-aac0-07746f095d38', # এটি পরিবর্তন করার প্রয়োজন হতে পারে
        'e-auth-c': '40',
        'e-auth-k': 'PgdtSBeR0MumR7fO',
        'accept-charset': 'UTF-8',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        'Host': 'api.eyecon-app.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'
    }

    try:
        # রিকোয়েস্ট পাঠানো হচ্ছে
        response = requests.get(url, headers=headers, params=params, timeout=15)
        
        # যদি ৪০১ এরর আসে তবে কাস্টম মেসেজ
        if response.status_code == 401:
            return jsonify({
                'status': 'failed',
                'message': 'Auth Token Expired or Invalid. Please update e-auth keys.',
                'dev': 'SB Sakib'
            }), 401
            
        response.raise_for_status()
        return jsonify(response.json())

    except requests.exceptions.HTTPError as errh:
        return jsonify({'error': 'HTTP Error', 'details': str(errh)}), response.status_code
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Connection Error. Please check your internet or IP block.'}), 502
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

if __name__ == '__main__':
    # লোকাল হোস্টে চালানোর জন্য
    app.run(host='0.0.0.0', port=5000, debug=True)
