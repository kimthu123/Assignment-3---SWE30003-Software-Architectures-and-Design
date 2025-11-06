from utils.db_handler import read_json, write_json

class InvoiceRepository:
    def __init__(self):
        self.file_path = 'data/invoices.json'

    def save(self, invoice_data):
        invoices = read_json(self.file_path)
        invoices.append(invoice_data)
        write_json(self.file_path, invoices)
        return invoice_data

    def get_data(self):
        return read_json(self.file_path)

    def get_id(self, invoice_id):
        invoices = read_json(self.file_path)
        return next((inv for inv in invoices if inv['invoice_id'] == invoice_id), None)

    def get_by_order_id(self, order_id):
        invoices = read_json(self.file_path)
        return next((inv for inv in invoices if inv['order_id'] == order_id), None)

