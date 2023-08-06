# This class was generated on Tue, 18 Jul 2017 12:56:42 PDT by version 0.01 of Braintree SDK Generator
# invoice_delete_external_payment_request.py
# DO NOT EDIT
# @type request
# @json {"Name":"invoice.delete_external_payment","Description":"Deletes an external payment, by invoice ID and transaction ID.","Parameters":[{"Type":"string","VariableName":"invoice_id","Description":"The ID of the invoice from which to delete a payment transaction.","IsArray":false,"ReadOnly":false,"Required":true,"Properties":null,"Location":"path"},{"Type":"string","VariableName":"transaction_id","Description":"The ID of the payment transaction to delete.","IsArray":false,"ReadOnly":false,"Required":true,"Properties":null,"Location":"path"}],"RequestType":null,"ResponseType":null,"ContentType":"application/json","HttpMethod":"DELETE","Path":"/v1/invoicing/invoices/{invoice_id}/payment-records/{transaction_id}","ExpectedStatusCode":200}



class InvoiceDeleteExternalPaymentRequest:
    """
    Deletes an external payment, by invoice ID and transaction ID.
    """

    def __init__(self, invoice_id, transaction_id):
        self.verb = "DELETE"
        self.path = "/v1/invoicing/invoices/{invoice_id}/payment-records/{transaction_id}?".replace("{invoice_id}", str(invoice_id)).replace("{transaction_id}", str(transaction_id))
        self.headers = {}
        self.headers["Content-Type"] = "application/json"

    
