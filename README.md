# Cyberspace Security Practice of Innovation and Entrepreneurship Course

山东大学网络空间安全学院（研究院） 2023年

网络空间安全创新创业实践课程   相关project报告汇总

------

**组号：100**

## 小组成员：

| 小组成员姓名 |                Github账户名称                | 学号         | 负责project(包括独立完成/合作完成) |
| :----------: | :------------------------------------------: | ------------ | ---------------------------------- |
|    刘舒畅    |     [Maxlsc ](https://github.com/Maxlsc)     | 202122460175 | 1,2,3,4,5,6,7,11,12,13,14,15,16,18 |
|     李昕     | [xin-li-sdu ](https://github.com/xin-li-sdu) | 202100460065 | 1,2,3,8,9,10,12,17,21,22           |
|    王子瑞    |       [skqf ](https://github.com/skqf)       | 202100460088 | 1,3,4,5,7,12,19                    |

## 项目完成进度及实现效果

本组完成全部21个project，同时完成信安赛作品，[实现基于格密码和密钥复用的后量子邮件加密系统](https://github.com/Maxlsc/Projects-of-CSPIE/tree/main/Email%20encryption%20system%20based%20on%20post%20quantum%20cryptography%20and%20key%20reuse)。

（注：各Project文件夹下有对应项目的详细报告，此处仅为效果汇总，**✔️** 为全部由一人完成）

| 项目名                                                       | 效果                                                         | 刘舒畅                           | 李昕               | 王子瑞             |
| ------------------------------------------------------------ | ------------------------------------------------------------ | -------------------------------- | ------------------ | ------------------ |
| [1 implement the naïve birthday attack of reduced SM3](https://github.com/Maxlsc/Projects-of-CSPIE/tree/main/Project1) | 碰撞结果48bit/17302ms（AMD Ryzen 7 6800H with Radeon Graphics） | python/自有库C++版本             | 基于gmsslC++版本   | 基于opensslC++版本 |
| [2 implement the Rho method of reduced SM3](https://github.com/Maxlsc/Projects-of-CSPIE/tree/main/Project2) | 碰撞结果48bit/11583ms（Intel(R) Core(TM) i7-12700H）         | python/自有库C++版本             | 基于opensslC++版本 |                    |
| [3 implement length extension attack for SM3, SHA256, etc](https://github.com/Maxlsc/Projects-of-CSPIE/tree/main/Project3) | 实现对sha256与sm3的长度扩展攻击                              | SM3python版本                    | SHA256python版本   |     sm3c++版本               |
| [4 do your best to optimize SM3 implementation(software)](https://github.com/Maxlsc/Projects-of-CSPIE/tree/main/Project4) | 1GB文件hash时间4092ms（AMD Ryzen 7 6800H with Radeon Graphics），接近openssl | 代码编写                         |                    |           gmssl与OpenSSL部分编写         |
| [5 Impl Merkle Tree following RFC6962](https://github.com/Maxlsc/Projects-of-CSPIE/tree/main/Project5) | 在RFC6962标准下实现Merkle Tree的建立和存在性证明             | **✔️**                            |                    |   Python代码编写                 |
| [6 impl this protocol with actual network communication](https://github.com/Maxlsc/Projects-of-CSPIE/tree/main/Project6) | python实现网络环境中的范围证明                               | **✔️**                            |                    |                    |
| [7 Try to Implement this scheme](https://github.com/Maxlsc/Projects-of-CSPIE/tree/main/Project7) | 实现Hash Wire证据生成，证明与验证全过程                      | 论文分析，基本函数与证据生成编写 |                    |      证明与验证部分编写              |
| [8 AES impl with ARM instruction](https://github.com/Maxlsc/Projects-of-CSPIE/tree/main/Project8) | 利用ARM指令集NEON实现AES128/192/256三个版本加速： 128bit版本在**PhytiumFT-2000/4处理器**下计算1000GB数据耗时11s，相同配置下较普通AES128计算1000GB数据45s约加速4倍 |                                  | **✔️**              |                    |
| [9 AES / SM4 software implementation](https://github.com/Maxlsc/Projects-of-CSPIE/tree/main/Project9) | 利用查找表优化/利用SIMD AVX2指令集优化/利用AES-NI指令集优化三种方法加速SM4， **AMD Ryzen 7 6800H with Radeon Graphics**下加密1024bit信息分别耗时0.0129ms/0.0041ms/0.0069ms  |                                  | **✔️**              |                    |
| [10 report on the application of this deduce technique in Ethereum with ECDSA](https://github.com/Maxlsc/Projects-of-CSPIE/tree/main/Project10) | 撰写关于ECDSA由签名值推导出公钥的原理方法/编写代码实现该过程 |                                  | **✔️**              |                    |
| [11 impl sm2 with RFC6979](https://github.com/Maxlsc/Projects-of-CSPIE/tree/main/Project11) | 在RFC6979标准下实现签名与加密                                | ✔️                                |                    |                    |
| [12 verify the above pitfalls with proof-of-concept code](https://github.com/Maxlsc/Projects-of-CSPIE/tree/main/Project12) | 实现文章中对于ECDSA,Schnorr与SM2的攻击                     | ECDSA部分                        | Schnorr部分 |           sm2部分         |
| [13 Implement the above ECMH scheme](https://github.com/Maxlsc/Projects-of-CSPIE/tree/main/Project13) | 实现两种不同散列到椭圆曲线点群散列方法的ECMH                 | ✔️                                |                    |                    |
| [14 Implement a PGP scheme with SM2](https://github.com/Maxlsc/Projects-of-CSPIE/tree/main/Project14) | 实现PGP，并加入签密功能                                      | ✔️                                |                    |                    |
| [15 implement sm2 2P sign with real network communication](https://github.com/Maxlsc/Projects-of-CSPIE/tree/main/Project15) | python实现网络环境中的sm2双签名                              | ✔️                                |                    |                    |
| [16 implement sm2 2P decrypt with real network communication](https://github.com/Maxlsc/Projects-of-CSPIE/tree/main/Project16) | python实现网络环境中的sm2双解密                              | ✔️                                |                    |                    |
| [17 比较Firefox和谷歌的记住密码插件的实现区别](https://github.com/Maxlsc/Projects-of-CSPIE/tree/main/Project17) | 阅读并分析两种密码插件的源代码，编写比较Firefox和谷歌的记住密码插件实现区别报告/编写代码实现谷歌密码破解 |                                  | **✔️**              |                    |
| [18 send a tx on Bitcoin testnet, and parse the tx data down to every bit, better write script yourself](https://github.com/Maxlsc/Projects-of-CSPIE/tree/main/Project18) | 获得tx，使用自编脚本分析tx内容与script内容                   | ✔️                                |                    |                    |
| [19  forge a signature to pretend that you are Satoshi](https://github.com/Maxlsc/Projects-of-CSPIE/tree/main/Project19) |   编写伪造ECDSA签名代码以伪造中本聪身份                                                           |                                  |                    |           **✔️**          |
| [21 Schnorr Bacth](https://github.com/Maxlsc/Projects-of-CSPIE/tree/main/Project21) | 实现Schnorr签名的批量验证功能                                |                                  | **✔️**              |                    |
| [22 research report on MPT](https://github.com/Maxlsc/Projects-of-CSPIE/tree/main/Project22) | 编写MPT（Merkle Patricia Trie）树报告，并分析部分MPT树代码   |                                  | **✔️**              |                    |
| *[信安赛项目](https://github.com/Maxlsc/Projects-of-CSPIE/tree/main/Email%20encryption%20system%20based%20on%20post%20quantum%20cryptography%20and%20key%20reuse) | 基于格密码和密钥复用实现的后量子邮件加密签名系统             | 本部分由三人共同完成。           | ✔️                  | ✔️                  |

附：所需外部库一览表

- C++

  部分需要链接[OpenSSL](https://github.com/openssl/openssl/releases/tag/OpenSSL_1_1_1s)和[GMSSL](https://github.com/guanzhi/GmSSL)两个密码学库（在各project的readme中已标识）

  链接方法：以VS2022为例，在项目属性页包含目录设置include文件夹，库目录设置静态键连接bin文件夹，附加依赖项设置libssl.lib和libcrypto.lib文件。

- python：

| 库名称 | 下载方法                            |
| ------ | ----------------------------------- |
| Crypto | `pip install pycryptodome`          |
| gmssl  | `pip install gmssl`                 |
| pysmx  | `pip install snowland-smx==0.3.2a1` |
| smt    | `pip install sparse-merkle-tree`    |
| sympy  | `pip install sympy`                 |

