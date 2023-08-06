import time
import random
import hashlib
import warnings

import rsa


class MBillsBase(object):
    def __init__(self, api_key, shared_secret, mbills_rsa_pub_key, nonce_length=15):
        self.api_key = api_key
        self.shared_secret = shared_secret

        self._pub_key = rsa.PublicKey.load_pkcs1_openssl_pem(mbills_rsa_pub_key) if mbills_rsa_pub_key else None

        assert 8 <= nonce_length <= 15, "Nonce must be of length between 8-15."
        self._nonce_length = nonce_length

    def _get_nonce(self):
        """
        Generate nonce per API specification. A random number of lenght 8-15
        :return: integer of specified length (int)
        """
        return random.randint(10**(self._nonce_length-1), (10**self._nonce_length)-1)

    def get_username(self):
        """
        Construct username as api_key.nonce.timestamp
        :return: username (string)
        """
        return "%s.%d.%d" % (self.api_key, self._get_nonce(), int(time.time()))

    def get_password(self, username, request_url):
        """
        Calculate the password as per the API specification.
        :param username: 
        :param request_url:
        :return: password (string)
        """
        content = "%s%s%s" % (username, self.shared_secret, request_url)
        return hashlib.sha256(content.encode('utf8')).hexdigest()

    def verify_signature(self, signature, nonce, timestamp, signed_id):
        """
        Verify the server response signature. 
        
        :param signature: 
        :param nonce: 
        :param timestamp: 
        :param signed_id: either transactionid, documentid or marketplacemerchantid
        :return: true of false
        """
        message = "%s%s%s%s" % (self.api_key, nonce, timestamp, signed_id)

        if self._pub_key is None:
            warnings.warn("Skipping RSA signature verification. Please pass public key on class initialization to ensure highest level of security!")
            return True

        try:
            rsa.verify(message, signature, self._pub_key)
        except rsa.VerificationError:
            return False

        return True

    def verify_response(self, response_json, signed_id_name='transactionid'):
        """
        Verify the response message.

        :param response_json: 
        :param signed_id_name: 
        :return: 
        """
        auth_json = response_json.get('auth', {})

        nonce = auth_json.get('nonce', '')
        timestamp = auth_json.get('timestamp', '')
        signature = auth_json.get('signature', '')

        signed_id = response_json.get(signed_id_name, '')

        return self.verify_signature(signature=signature, nonce=nonce, timestamp=timestamp, signed_id=signed_id)
