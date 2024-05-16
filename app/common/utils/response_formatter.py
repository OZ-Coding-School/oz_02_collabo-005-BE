class JSONDataFormatter:
    def __init__(self, status=200):
        self.status = status
        self.message = ""
        self.additional_datas = []

    def set_status_and_message(self, status, message):
        self.status = status
        self.message = message

    def add_response_data(self, *datas):
        for data in datas:
            self.additional_datas.append(data)

    def get_response_data(self):
        data = {
            "status": self.status,
            "message": self.message,
        }
        for additional_data in self.additional_datas:
            data.update(additional_data)
        return data