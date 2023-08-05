# flask-notifyAll

A Flask extension to access sending *sms/emails/test emails*, providers such as: Twilio, Mailtrap.

[![Build Status](https://travis-ci.org/MichaelYusko/flask-notifyAll.svg?branch=master)](https://travis-ci.org/MichaelYusko/flask-notifyAll)

Installation
=================================
```
pip install flask_notifyAll
```

Examples
========
Your TestConfig class, with test credentials of application
Also you able to create any config file, it's no matter
```python
class TestConfig:
    TWILIO_SID = 'YOUR_TWILIO_SID'
    TWILIO_TOKEN = 'YOUR_TWILIO_TOKEN'
    TWILIO_NUMBER = 'YOUR_TWILIO_NUMBER'
    MAILTRAP_USER = 'YOUR_MAILTRAP_USER'
    MAILTRAP_PASSWORD = 'YOUR_MAILTRAP_PASSWORD'
    TEST_EMAIL = 'YOUR_NAME_OF_TEST_EMAIL'
```

File with your application
```python
from flask import Flask, request, jsonify
from flask_notifyAll import FlaskNotify, generate_verification_code

app = Flask(__name__)
app.config.from_object('conf.TestConfig')
flask_notify = FlaskNotify(app)


@app.route('/send-verification-code', methods=['POST'])
def send_verification_code():
    phone_number = request.json.get('phone_number')
    code = generate_verification_code()
    flask_notify.send_verification_code(phone_number, code)
    return jsonify(
        {'data': {'message': 'verification code sent successfully', 'verification_code': code}}
    )


@app.route('/send-emails', methods=['POST'])
def send_emails():
    emails = request.json.get('emails')
    subject = 'Hello'
    body = 'Hello from FlaskNotify'
    flask_notify.send_mailtrap_email(emails, subject, body)
    return jsonify({'data': {'message': 'emails sent successfully'}})


@app.route('/send-sms-notification', methods=['POST'])
def send_sms_notification():
    phone_number = request.json.get('phone_number')
    message = 'Hello world'
    flask_notify.send_sms_notification(phone_number, message)
    return jsonify({'data': {'message': 'notification sent successfully'}})


if __name__ == '__main__':
    app.run(debug=True)


```
ToDo
====
* **Add mandrill support**

Contribution
=================================
1. Fork the repo
2. Feel free to make a PR;)