from django.core.exceptions import ValidationError
from django.utils import timezone as tz


class Payment:
    def __init__(self, amount: int):
        if amount <= 1000:
            raise ValidationError("مقدار پرداختی باید بیشتر یا مساوی 1000 تومان باشد.")

        # save value in تومان
        self.amount = amount * 10

    def request(self):
        authority = 104534
        return {"authority": authority}

    def verify(self):
        success = True
        reference_id = 2342034
        paid_at = tz.now()
        return {
            "success": success,
            "reference_id": reference_id,
            "paid_at": paid_at,
        }
