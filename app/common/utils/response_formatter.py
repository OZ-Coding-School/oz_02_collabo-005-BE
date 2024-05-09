class JSONDataFormatter:
    def __init__(self, status):
        self.status = status
        self.message = ""
        self.additional_datas = []

    def add_response_data(self, *datas):
        for data in datas:
            self.additional_datas.append(data)

    def get_response_data(self):
        data = {
            "message": self.message,
        }
        for additional_data in self.additional_datas:
            data.update(additional_data)
        return data