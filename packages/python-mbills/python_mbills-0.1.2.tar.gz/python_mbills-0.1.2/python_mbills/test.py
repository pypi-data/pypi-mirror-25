from base import MBillsBase
from python_mbills.api import MBillsAPI
from python_mbills.exceptions import SignatureValidationException

pub_key = """-----BEGIN PUBLIC KEY-----
 MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA94CbbAspiut6qnC1iLzS
 JY4kmEgW/euPenOvMCB0EbbjSBVncx1Vi6UvbY86bu/3ZMgDBdhcq9fvqrdL2WLv
 acPWnHgIGCRV/8tlGs7oAcKei9V6OcyRjh0jD4TwBGqDUbQEfBXkLL1kJB8nPsLc
 UVrhmwGKM3qKTchSutpnDipRRSufswM2b8ScGLMX8O5J/54o85UiSP/ZZYcx4UDE
 polN0k31Xa3fDw3tYn9KlIahALzgOqksF9jbv7jKS/DzpJAmQptuoL3t/0kj9J3t
 ujh1NBpMoac7cCBiVCc+LVHga1Okn0R/1RotceYbkl6TaLW4O56XF5QorlHlkBWY
 5wIDAQAB
 -----END PUBLIC KEY-----"""


api = MBillsAPI(api_key='22a71a85-3807-4e0b-93ea-f450c4d8981a', shared_secret='9335be75-90c4-41e2-af6f-fefb8028f424', mbills_rsa_pub_key=pub_key, nonce_length=8,
                api_endpoint="https://demo3.halcom.com/MBillsWS")


try:
    success = api.test_api_parameters_and_signature_verification()
    print("Success: %s" % success)
except SignatureValidationException:
    print("Failed to verify signature")


try:
    transaction_id, payment_token_number, status = api.create_new_sale(100, 'Some purpose here')
    print("Payment token number: %s" % payment_token_number)

    transaction = api.fetch_transaction_status(transaction_id)

    print(transaction)

except SignatureValidationException:
    print("Failed to verify signature")
