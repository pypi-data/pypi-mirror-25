import json

import requests

from clickpost_python.clickpost_order_creation.order_creation_response import OrderCreationResponse
from clickpost_python.constants import CLICKPOST_OC_URL


class OrderCreation:
    def __init__(self, order_creation_data, api_key, username):
        self.order_creation_data = order_creation_data
        self.api_key = api_key
        self.username = username

    def create_order(self):
        success = None
        status = None
        message = None
        waybill = None
        label = None
        reference_number = None
        try:
            oc_url = CLICKPOST_OC_URL + "?key=" + str(self.api_key) + "&username=" + str(self.username)
            payload = json.dumps(self.order_creation_data)
            request_post_object = requests.post(url=oc_url, data=payload,
                                                headers={'Content-Type': 'application/json'})
            status = request_post_object.status_code
            if request_post_object.status_code == 200:
                final_result = json.loads(request_post_object.text)
                message = final_result['meta']['message']
                status = final_result['meta']['status']
                success = final_result['meta']['success']
                if final_result['meta']['success']:
                    waybill = final_result['result']['waybill']
                    label = final_result['result']['label']
                    reference_number = final_result['result']['reference_number']
            else:
                raise Exception("Internal Server error in clickpost_python!")
        except Exception as e:
            success = False
            message = str(e)
        finally:
            return OrderCreationResponse(success, status, message, waybill, label, reference_number)
