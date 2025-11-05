import datetime
from utils.db_handler import read_json, write_json

class Invoice:
    def __init__(self, order_id, total_amount, payment_status):
        self.order_id = order_id
        self.total_amount = total_amount
        self.payment_status = payment_status

    def generate_invoice(self):
        invoices = read_json('data/invoices.json')

        invoice_id = len(invoices) + 1
        invoice_data = {
            "invoice_id": invoice_id,
            "order_id": self.order_id,
            "total_amount": self.total_amount,
            "payment_status": self.payment_status,
            "issued_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        invoices.append(invoice_data)
        write_json('data/invoices.json', invoices)

        return invoice_data
