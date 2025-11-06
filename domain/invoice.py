import datetime
from repositories.invoice_repository import InvoiceRepository

class Invoice:
    def __init__(self, order_id, total_amount, payment_status):
        self.order_id = order_id
        self.total_amount = total_amount
        self.payment_status = payment_status
        self.invoice_repo = InvoiceRepository()

    def generate_invoice(self):
        # grab existing invoices before generating new invoice ID
        existing_invoices = self.invoice_repo.get_data()
        invoice_id = len(existing_invoices) + 1
        
        invoice_data = {
            "invoice_id": invoice_id,
            "order_id": self.order_id,
            "total_amount": self.total_amount,
            "payment_status": self.payment_status,
            "issued_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return self.invoice_repo.save(invoice_data)
