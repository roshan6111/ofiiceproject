import json

from flask import Flask, request, make_response

from src.CreditScore import CreditEngine
from src.Service import Auth, InputValidation
from src.Utils import api_utils, Encryption, bsr_utils
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_object('config.BaseConfig')

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

@app.route('/Verification', methods=['POST'])
def matching():
    """
    Main API
    :return: Status and callback with pdf details.
    """
    auth_value = request.headers.get('Authorization')
    ip = str(request.remote_addr)
    if Auth.auth(auth_value, ip):
        verification_input = request.json
        verification_response = InputValidation.verification_input(verification_input)
        if verification_response is not None:
            response = {
                'errorCode': 222,
                '_id': '',
                'xpressId': '',
                'taskId': '',
                'error': verification_response
            }
            return json.dumps(response)
        else:
            response = api_utils.get_verification(verification_input)
            return response
    else:
        return make_response('UnAuthorize User:', 401)


@app.route('/VerificationCallBack', methods=['POST'])
def callback():
    """
    API to get details using taskid
    :return: all pdf information of particular taskid
    """
    auth_value = request.headers.get('Authorization')
    ip = str(request.remote_addr)
    error_response = {}
    if Auth.auth(auth_value, ip):

        verification_input = request.json
        verification_response = InputValidation.verificationCallBack_input(verification_input)
        if verification_response is not None:
            response = {
                'errorCode': 222,
                '_id': '',
                'xpressId': '',
                'taskId': '',
                'error': verification_response
            }
            return json.dumps(response)
        else:
            error_response['taskId'] = taskid = request.json['taskId']
            error_response['xpressId'] = xpressid = request.json['xpressId']
            error_response['_id'] = ''
            error_response['resultBusiness'] = ''
            error_response['resultPersonal'] = ''
            if taskid == "" or xpressid == "":
                error_response['errorCode'] = 120
                error_response['error'] = bsr_utils.get_error_description("120")
                return json.dumps(error_response)
            user_details = api_utils.verification_call_back(taskid, xpressid)
            if user_details == 0:
                error_response['errorCode'] = 205
                error_response['error'] = bsr_utils.get_error_description("205")
                return json.dumps(error_response)
            user_details['_id'] = str(user_details['_id'])
            return json.dumps(user_details)
    else:
        return make_response('UnAuthorize User:', 401)
# @app.route('/VerificationCallBack', methods=['POST'])
# def callback():
#     """
#     API to get details using taskid
#     :return: all pdf information of particular taskid
#     """
#     auth_value = request.headers.get('Authorization')
#     ip = str(request.remote_addr)
#     error_response = {}
#     if Auth.auth(auth_value, ip):
#         error_response['taskId'] = taskid = request.form['taskId']
#         error_response['xpressId'] = xpressid = request.form['xpressId']
#         error_response['_id'] = ''
#         error_response['resultBusiness'] = ''
#         error_response['resultPersonal'] = ''
#         if taskid == "" or xpressid == "":
#             error_response['errorCode'] = 120
#             error_response['error'] = bsr_utils.get_error_description("120")
#             return json.dumps(error_response)
#         user_details = api_utils.verification_call_back(taskid, xpressid)
#         if user_details == 0:
#             error_response['errorCode'] = 205
#             error_response['error'] = bsr_utils.get_error_description("205")
#             return json.dumps(error_response)
#         user_details['_id'] = str(user_details['_id'])
#         return json.dumps(user_details)
#     else:
#         return make_response('UnAuthorize User:', 401)


@app.route('/creditScore', methods=['POST'])
def credit_engine():
    auth_value = request.headers.get('Authorization')
    ip = str(request.remote_addr)
    if Auth.auth(auth_value, ip):
        credit_score_data = request.json
        # this is not used any where if want to remove (remove from both form and api)
        verification_response = InputValidation.credit_score_input(credit_score_data)
        if verification_response is not None:
            response = {
                'errorCode': 222,
                '_id': '',
                'xpressId': '',
                'taskId': '',
                'error': verification_response,
                "interest": "",
                "creditScore": 0,
                "amount": 0,
                "_id": "",
                "creditDecision": False
            }
            return json.dumps(response)
        else:
            credit_score_data['totalLoansNumberPersonal'] = 0.0
            credit_result = CreditEngine.credit_engine(credit_score_data)
            return json.dumps(credit_result)
    else:
        return make_response('UnAuthorize User:', 401)


@app.errorhandler(404)
def page_not_found(e):
    return app.register_error_handler(404, page_not_found)


if __name__ == '__main__':
    app.run(debug=True)
