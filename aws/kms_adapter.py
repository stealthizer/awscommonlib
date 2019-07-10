import base64

class AwsKms:

    def __init__(self, kmssession):
        self.kmssession = kmssession

    def encrypt(self, key_arn, text_blob):
        stuff = self.kmssession.encrypt(KeyId=key_arn, Plaintext=text_blob)
        binary_encrypted = stuff[u'CiphertextBlob']
        encrypted_password = base64.b64encode(binary_encrypted)
        return encrypted_password.decode()

    def decrypt(self, encrypted_blob):
        binary_data = base64.b64decode(encrypted_blob)
        meta = self.kmssession.decrypt(CiphertextBlob=binary_data)
        plaintext = meta[u'Plaintext']
        return plaintext.decode()


