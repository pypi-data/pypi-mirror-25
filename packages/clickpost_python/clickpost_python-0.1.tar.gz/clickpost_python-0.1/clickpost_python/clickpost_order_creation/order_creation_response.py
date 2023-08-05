class OrderCreationResponse:
    success = None
    status = None
    message = None
    waybill = None
    label = None
    reference_number = None

    def __init__(self, success, status, message, waybill, label, reference_number):
        self.success = success
        self.status = status
        self.message = message
        self.waybill = waybill
        self.label = label
        self.reference_number = reference_number

    def get_status_code(self):
        return self.status

    def is_success(self):
        return self.success

    def get_message(self):
        return self.message

    def get_waybill(self):
        return self.waybill

    def get_reference_number(self):
        return self.reference_number

    def get_label(self):
        return self.label
