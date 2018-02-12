"""
This is the client script that gets uploaded to the clients machine and executed.
This file also contains the class used for encryptiona and decryption.  It was added
here so that only one file can be uploaded to the server instead of multiple.
If required the AES class can be extracted to its own file and imported here.

When this file is executed it will print out the encrypted value of the statistics
JSON string.
"""
import time
import psutil
import json

from Crypto.Cipher import AES
from Crypto import Random


key = "140b41b22a29beb4061bda66b6747e14"

class StatisticsCollector(object):
    def get(self):
        """
        Print encrypted and hex encoded string of 
        the machine's statistics
        """
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory()[2]
        disk = psutil.disk_usage('/')[3]

        statistics = {
            'cpu': cpu,
            'memory': memory,
            'disk': disk,
            'uptime': self.get_uptime()
        }

        return statistics


    def get_uptime(self):
        """
        Determine the uptime of the machine
        :return: string formated as days hours minutes and seconds of the uptime of the machine
        """
        minute = 60
        hour = minute * 60
        day = hour * 24

        d = h = m = 0

        s = int(time.time()) - int(psutil.boot_time())

        d = s / day
        s -= d * day
        h = s / hour
        s -= h * hour
        m = s / minute
        s -= m * minute

        uptime = ""
        if d > 1:
            uptime = "%d days, "%d
        elif d == 1:
            uptime = "1 day, "

        #return uptime + "%dh%02d:%02d"%(h,m,s)
        return '{0} {1}h {2}m {3}s'.format(uptime, h, m, s)
    

class AESCipher(object):
    def __init__(self, key):
        self.key = key.decode('hex')

    
    def encrypt(self, raw):
        """
        Decrypt AES encrypted and hex encoded String

        :param raw: string to be encrypted and hex encoded
        :return: encrypted and hex encoded string
        """
        raw = self.pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return (iv + cipher.encrypt(raw)).encode('hex')


    def decrypt(self, enc):
        """
        Decrypt AES encrypted and hex encoded String

        :param enc: AES encrypted and hex encoded string
        :return: decoded and decrypted string
        """
        enc = enc.decode('hex')
        iv = enc[:16]
        enc= enc[16:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self.unpad(cipher.decrypt(enc))


    def pad(self, s): 
        return s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size) 
    
    
    def unpad(self, s):
        return s[0:-ord(s[-1])]


if __name__ == '__main__':
    encryptor = AESCipher(key)
    statistics = StatisticsCollector().get()
    print(encryptor.encrypt(json.dumps(statistics, separators=(',', ':'))))
    