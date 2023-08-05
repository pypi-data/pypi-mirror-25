from . import BaseLINEPayAPI, LINEPayException

class LINEPayPayment(BaseLINEPayAPI):
    def inquire(self, transaction_ids=None, order_ids=None):
        transaction_ids_string = None if transaction_ids is None else \
            ','.join(map(lambda x: str(x), transaction_ids))
        order_ids_string = None if order_ids is None else ','.join(order_ids)
        if transaction_ids_string is None:
            return self._get('/v2/payments?orderId=%s' \
            % (order_ids_string))
        if order_ids_string is None:
            return self._get('/v2/payments?transactionId=%s' \
            % (transaction_ids_string))
        return self._get('/v2/payments?transactionId=%s&orderId=%s' \
            % (transaction_ids_string, order_ids_string))

    def request(self,
        order_id,
        product_name,
        amount,
        currency, 
        confirm_url,
        product_image_url=None,
        confirm_url_type="CLIENT",
        cancel_url=None,
        ):
        data = {
            'orderId': order_id,
            'productName': product_name,
            'amount': amount,
            'currency': currency,
            'confirmUrl': confirm_url,
            'productImageUrl': product_image_url,
            'confirmUrlType': confirm_url_type,
            'cancelUrl': cancel_url,
        }
        return self._post('/v2/payments/request', data=data)

    def confirm(
        self,
        transaction_id,
        amount,
        currency,
    ):
        data = {
            'amount': amount,
            'currency': currency,
        }
        return self._post('/v2/payments/%s/confirm' % transaction_id, data=data)

    def refund(
        self,
        transaction_id,
        refund_amount=None,
    ):
        data = {
            'refundAmount': refund_amount,
        }
        return self._post('/v2/payments/%s/refund' % transaction_id, data=data)
