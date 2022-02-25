"""
    Simple Flask-based API for scraping data and sending emails.
    Author: Anda Mchako.
    Note:
    ---------------------------------------------------------------------
    Please follow the instructions provided within the README.md file
    located within this directory for guidance on how to use this script
    correctly.
    ---------------------------------------------------------------------
    Description: This file instantiates a Flask webserver
    as a means to create a simple API used to send emails to defecting clients.
"""

# importing libraries
from flask import Flask, request, make_response  # pylint: disable=import-error
# import pandas as pd  # pylint: disable=import-error
from flask_mail import Mail, Message  # pylint: disable=import-error
import pandas as pd
# import model  # pylint: disable=import-error
import model
from utils import config


app = Flask(__name__)

mail = Mail(app)  # instantiate the mail class


@app.route('/data', methods=['POST'])
def get_data():
    """

    Returns:

    """
    url = request.get_json(force=True)
    product_info = model.get_products(url.get('url'))
    clean_data = model.process_data(product_info)

    clean_data.to_csv('utils/data/clean_data.csv')
    return make_response({'response': 'Data downloaded!'}), 200


# message object mapped to a particular URL ‘/’
@app.route("/mail", methods=['GET'])
def send_mail():
    """

    Returns:

    """
    data = pd.read_csv('utils/data/clean_data.csv')
    data = data[data['SubStatus'] == 'Flag']

    msg = Message(
        'Your account status',
        sender=config.MAIL_USERNAME,
        recipients=[data['CustomerMail'].values.tolist()[0], '****@gmail.com']
    )

    msg.body = "Due to missed payments, your device has been locked. Please contact Rentoza for a resolution."
    mail.send(msg)

    return make_response({'response': 'Email sent!'}), 200


if __name__ == '__main__':
    app.run(debug=True)
