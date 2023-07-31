# Cyberspace Security Practice of Innovation and Entrepreneurship Course

山东大学网络空间安全学院（研究院） 2023年

网络空间安全创新创业实践课程   相关project Group X 报告汇总

------

## 小组成员：

| 小组成员姓名 |                Github账户名称                | 学号         |
| :----------: | :------------------------------------------: | ------------ |
|    刘舒畅    |     [Maxlsc ](https://github.com/Maxlsc)     | 202122460175 |
|     李昕     | [xin-li-sdu ](https://github.com/xin-li-sdu) | 202100460065 |
|    王子瑞    |       [skqf ](https://github.com/skqf)       | 202100460088 |

## 项目完成进度及实现效果

（注：各Project文件夹下有对应项目的详细报告，此处仅为效果汇总，**✔️** 为全部由一人完成）

| 项目名 | 效果                                             | 刘舒畅                           | 李昕 | 王子瑞 |
| ------ | ------------------------------------------------ | -------------------------------- | ---- | ------ |
| 1 implement the naïve birthday attack of reduced SM3 | 碰撞结果48bit/17302ms                            | python/自有库C++                        |      |        |
| 2 implement the Rho method of reduced SM3 | 碰撞结果48bit/11583ms                            | python/自有库C++                 |   基于opwnsslC++   |        |
| 3      | 实现对sha256与sm3的长度扩展攻击                  | SM3python                           |   SHA256python   |        |
| 4      | 1GB文件hash时间4092ms                            | 代码编写                         |      |        |
| 5      | 在RFC6962标准下实现Merkle Tree的建立和存在性证明 | **✔️**                            |      |        |
| 6      | python实现网络环境中的范围证明                   | **✔️**                            |      |        |
| 7      | 实现Hash Wire证据生成，证明与验证全过程          | 论文分析，基本函数与证据生成编写 |      |        |
| 8      | 利用ARM的SIMD指令集NEON实现AES128/192/256三个版本的实现和加速，并于普通版本在ARM环境下进行速度比较 |         |   **✔️**    |        |
| 9      | 利用常见的查找表/利用SIMD AVX2指令/利用AES-NI指令集加速SM4  |           |    **✔️**   |        |
| 10     | 撰写关于ECDSA由签名值推导出公钥的原理方法/编写代码实现该过程       |                   |    **✔️**    |        |
| 11     | 在RFC6979标准下实现签名与加密                    | ✔️                                |      |        |
| 12     | 实现文章中对于ECDSA与sm2的攻击                   | ECDSA部分                        |      |        |
| 13     | 实现两种不同散列到椭圆曲线点群散列方法的ECMH     | ✔️                                |      |        |
| 14     | 实现PGP，并加入签密功能                          | ✔️                                |      |        |
| 15     | python实现网络环境中的sm2双签名                  | ✔️                                |      |        |
| 16     | python实现网络环境中的sm2双解密                  | ✔️                                |      |        |
| 17     | 编写比较Firefox和谷歌的记住密码插件实现区别报告/编写代码实现谷歌密码破解             |               |   **✔️**   |        |
| 18     | 获得tx，使用自编脚本分析tx内容与script内容       | ✔️                                |      |        |
| 19     |                                                  |                                  |      |        |
| 21     | 实现Schnorr签名的批量验证功能          |                  |    **✔️**    |        |
| 22     |  编写MPT（Merkle Patricia Trie）树报告，并分析部分MPT树代码      |                   |    **✔️**   |        |

