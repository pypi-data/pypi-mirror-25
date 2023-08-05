from binascii import unhexlify
from hashlib import sha1
from struct import unpack

from .base import Packet, Opcode


class ResetErrorCountRequest(Packet):
    def __init__(self):
        super().__init__()
        self.opcode = Opcode.ResetErrorCount
        # self.shared_key = self.generate_shared_key()

    @classmethod
    def _encode_payload(cls, data: dict) -> bytes:
        ver1, ver2 = data['version']

        """
        hasher = sha1()
        hasher.update(unhexlify(user_hash))
        hasher.update(token.encode())
        """

        return f"{data['mno']: <3}" \
               f"{data['oid']: <11}" \
               f"{data['hw_model']: <16}" \
               f"{data['hw_id']: <4}" \
               f"{ver1:0>4}" \
               f"{ver2:0>4}" \
               f"{data['token']:0>7} " \
            .encode()

    @classmethod
    def _decode_payload(cls, payload: bytes) -> dict:
        token, = unpack('!8s', payload)

        return {
            'token': token.strip(),
        }
