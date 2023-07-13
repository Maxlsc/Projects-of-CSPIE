# MPT树

本MD文件即为MPT-research-report

MPT（Merkle Patricia Trie）树，即默克尔前缀树，是默克尔树和前缀树的结合。是一种基于哈希的树形结构，在以太坊区块链中被广泛应用，用于存储账户的状态和交易数据。它能够高效地处理大量的数据，并提供了高度的安全性和完整性验证能力。

MPT树有以下几个作用：

- 存储任意长度的key-value键值对数据，符合以太坊的state模型；
- 提供了快速计算所维护数据集哈希标识的机制；
- 提供了快速状态回滚的机制；
- 提供了称为默克尔证明的证明方法，可以进行轻节点的扩展，实现简单支付验证。

由于MPT结合了Radix trie和Merkle两种树结构的特点与优势 ，因此首先分析前两者的特点和结构。

## Radix trie

Trie树，又称为前缀树或字典树，是一种在保存关联数组时使用的有序树。通常情况下，其中的键是字符串类型。

与二叉查找树不同的，Trie树中的节点并不直接保存键，而是通过节点在树中的位置来决定键的值。每个节点及其子孙都有相同的前缀，也就是该节点对应的字符串，而根节点对应的是空字符串。

一般而言，并非所有的节点都具有相关的值，只有叶子节点和部分内部节点才会对应具体的键值。实际上，Trie树中的每个节点都是一个确定长度的数组，数组中的每个元素是一个指向子节点的指针。此外，还有一个标志域用于标识该位置是否是一个完整的字符串。

相比于哈希表，使用前缀树来进行查询拥有共同前缀key的数据时效率更高，哈希表的时间复杂度为O(N)，但是前缀树可以根据前缀快速定位所求值得位置。

但是对于最差的情况（前缀为空串)，前缀树时间效率为O(N)，这代表着仍然需要遍历整棵树，此时效率与哈希表相同。不过此时仍然存在优势，即前缀树由于是树形结构，不会存在哈希表哈希冲突的问题。

不过同时，前缀树也存在诸多问题，其中一个主要问题为开销，当存储key值较大得节点时，若此时树中没相同前缀得节点，就需要创建许多非叶子节点，造成开销浪费

##  Merkle tree

Merkle tree是一种树，大多数是二叉树，也可以多叉树，无论是几叉树，它都具有树结构的所有特点。其叶子节点的value是数据项的内容，或者是数据项的哈希值，非叶子节点的value根据其子节点的信息，然后按照Hash算法计算而得出的。

将相邻两个同级节点的哈希值合并成一个字符串，然后计算这个字符串的哈希，得到的就是这两个节点的父节点的哈希值。

如果该层的树节点个数是单数，那么对于最后剩下的树节点，这种情况就直接对它进行哈希运算，其父节点的哈希就是其哈希值的哈希值（对于单数个叶子节点，有着不同的处理方法，也可以采用复制最后一个叶子节点凑齐偶数个叶子节点的方式）。循环重复上述计算过程，最后计算得到最后一个节点的哈希值，将该节点的哈希值作为整棵树的哈希。若两棵树的根哈希一致，则这两棵树的结构、节点的内容相同。

Merkle tree的特点之一就是当树节点内容发生变化时，能够在前一次哈希计算的基础上，仅仅将被修改的树节点进行哈希重计算，便能得到一个新的根哈希用来代表整棵树的状态。

不过其劣势和 Radix trie相同，即空间开销较大。

## MPT

下面分析MPT树的结构，功能和特点。

### MPT树的节点

Trie节点： Merkle Patricia Trie使用字节流来表示键值对数据。每个键值对都存储在一个Trie节点中。Trie节点有四种类型：扩展节点（Extension node）、分支节点（Branch node）、叶子节点（Leaf node）和空节点（Null node）。

```go
type (
	fullNode struct {
		Children [17]node // 分支节点
		flags    nodeFlag
	}
	shortNode struct { //扩展节点
		Key   []byte
		Val   node //可能指向叶子节点，也可能指向分支节点。
		flags nodeFlag
	}
	hashNode  []byte
	valueNode []byte // 叶子节点值，但是该叶子节点最终还是会包装在shortNode中
)
```

* 扩展节点: 扩展节点存储了一个字符片段，用于在Trie中查找下一个节点。
* 分支节点: 分支节点包含16个指针和一个value，每个指针指向一个孩子节点。这些指针分别对应16进制字符集中的0到F字符。
* 叶子节点: 叶子节点存储了一个键的值，即value。
* 空节点: 空节点表示一个空路径或者一个已删除的节点。

其中，Key只在扩展节点和叶子节点中存在，分支节点中没有Key。Value用来存储节点数值，不同的节点类型对应的Value值不同，主要如下几种情况：

​    1.若节点类型是叶子节点，Value值存储的是一个数据项的内容。

​    2.若节点类型是扩展节点，Value值存储的是子节点的哈希值。

​    3.若节点类型是分支节点，Value值存储的是刚好在分支节点结束时的值，若没有节点在分支节点中结束时，Value值没有存储数据。

计算key所用到 Twox128 <sup>[1]</sup>是一种非加密的哈希算法，计算速度非常快，但去除了一些严格的要求，如不会碰撞、很小的输入改变导致极大的输出改变等，从而无法保证安全性，适用于输入固定且数量有限的场景中。`module_prefix`通常是模块的实例名称；`storage_prefix`通常是存储单元的名称；原始的key通过SCALE编码器进行编码，再进行哈希运算，这里的哈希算法是可配置的，如果输入来源不可信如用户输入，则使用`Blake2`（也是默认的哈希算法），否则可以使用Twox。

需要注意的是：Key-value关系中，value存储的是key，key存储在路径上，具体解释为叶子节点表示为[key,value]的一个键值对，其中key是key的一种特殊十六进制编码。扩展节点也是[key，value]的一个键值对，但是这里的value是其他节点的hash值，这个hash可以被用来查询数据库中的节点。也就是说通过hash链接到其他节点。因为MPT树中的key被编码成一种特殊的16进制的表示，再加上最后的value，所以分支节点是一个长度为17的list，前16个元素对应着key中的16个可能的十六进制字符，如果有一个[key,value]对在这个分支节点终止，最后一个元素代表一个值，即分支节点既可以搜索路径的终止也可以是路径的中间节点。



### MPT中的Merkle属性<sup>[2]</sup>

在MPT中，指向下一级节点的指针是使用节点的确定性加密hash，而不是传统意义上下一级节点地址的指针，如果给定的trie的根哈希是公开的，则任何人都可以通过给出给定path上的所有节点, 来证明在给定path上存在一个给定值 ，对于攻击者,不可能提供一个不存在的（key，value）对的证明, 因为根哈希最终基于它下面的所有哈希，所以任何修改都会改变根哈希。

![image]([Projects-of-CSPIE/Project22/picture/1.png at main · xin-li-sdu/Projects-of-CSPIE · GitHub](https://github.com/xin-li-sdu/Projects-of-CSPIE/blob/main/Project22/picture/1.png))

### MPT操作<sup>[3]</sup>

#### Init

要初始化一个空的MPT树，要完成以下各步：

1. 创建一个空的根节点root：这个根节点没有键和值，它仅作为MPT树的起始节点。
2. 分配一个唯一标识（使用哈希值）给这个根节点。
3. 将这个唯一标识设置为MPT树的根哈希。

接下来，向MPT树中插入键值对、更新现有键值对或从MPT树中删除键值对。这些操作会涉及到对MPT树的节点进行读取、修改和重组。

需要注意的是，MPT树的初始化只涉及到创建一个空的根节点并设置根哈希，实际的数据和操作都发生在根节点以及其下的子节点上。因此，在初始化之后，可以通过对根节点的操作来构建和管理整个MPT树。

```go
func New(root common.Hash, db *Database) (*Trie, error) {
	if db == nil {
		panic("trie.New called without a database")
	}
	trie := &Trie{
		db: db,
	}
	if root != (common.Hash{}) && root != emptyRoot {
		rootnode, err := trie.resolveHash(root[:], nil)
		if err != nil {
			return nil, err
		}
		trie.root = rootnode
	}
	return trie, nil
}

```

#### Get

将需要查找Key的Raw编码转换成Hex编码，得到的内容称之为搜索路径；

从根节点开始搜寻与搜索路径内容一致的路径：

1. 若当前节点为叶子节点，并且存储的内容是数据项的内容，同时搜索路径与叶子节点的键完全一致，则表示已经找到该节点；反之则表示该节点在树中不存在。

2. 若当前节点为扩展节点，并且存储的内容是哈希索引，可以利用该哈希索引从数据库中加载相应的节点。然后将搜索路径作为参数，对新加载的节点进行递归调用查找函数。

3. 若当前节点为扩展节点，并且存储的内容是另外一个节点的引用，同时当前节点的键是搜索路径的前缀，那么可以将搜索路径减去当前节点的键，将剩余的搜索路径作为参数，对当前节点的子节点进行递归调用查找函数。如果当前节点的键不是搜索路径的前缀，表示该节点在树中不存在。

4. 若当前节点为分支节点，如果搜索路径为空，则返回分支节点的存储内容。否则，根据搜索路径的第一个字节选择分支节点的相应子节点，并将剩余的搜索路径作为参数继续递归调用查找函数。

```go
func (t *Trie) tryGet(origNode node, key []byte, pos int) (value []byte, newnode node, didResolve bool, err error) {
	switch n := (origNode).(type) {
	case nil: //表示当前trie是空树
		return nil, nil, false, nil
	case valueNode: ////这就是我们要查找的叶子节点对应的数据
		return n, n, false, nil
	case *shortNode: ////在叶子节点或者扩展节点匹配
		if len(key)-pos < len(n.Key) || !bytes.Equal(n.Key, key[pos:pos+len(n.Key)]) {
			return nil, n, false, nil
		}
		value, newnode, didResolve, err = t.tryGet(n.Val, key, pos+len(n.Key))
		if err == nil && didResolve {
			n = n.copy()
			n.Val = newnode
		}
		return value, n, didResolve, err
	case *fullNode://在分支节点匹配
		value, newnode, didResolve, err = t.tryGet(n.Children[key[pos]], key, pos+1)
		if err == nil && didResolve {
			n = n.copy()
			n.Children[key[pos]] = newnode
		}
		return value, n, didResolve, err
	case hashNode: //说明当前节点是轻节点，需要从db中获取
		child, err := t.resolveHash(n, key[:pos])
		if err != nil {
			return nil, n, true, err
		}
		value, newnode, _, err := t.tryGet(child, key, pos)
		return value, newnode, true, err
...
}
```

#### Insert

插入操作也是基于查找过程完成的，一个插入过程为：

首先，根据要插入节点的路径，从MPT的根节点开始进行查找，直到找到与新插入节点拥有最长相同路径前缀的节点（Node）为止。

```go
func (t *Trie) insert(n node, prefix, key []byte, value node) (bool, node, error)

```

如果Node是一个分支节点：

1. 如果剩余的搜索路径不为空，将新节点作为一个叶子节点插入到Node的对应的孩子列表中。
2. 如果剩余的搜索路径为空（完全匹配），将新节点的内容存储在Node的第17个孩子节点项中（Value）。

```go
dirty, nn, err := t.insert(n.Children[key[0]], append(prefix, key[0]), key[1:], value)
		if !dirty || err != nil {
			return false, n, err
		}
		n = n.copy()
		n.flags = t.newFlag()
		n.Children[key[0]] = nn
		return true, n, nil

```

如果Node是一个叶子节点或扩展节点：

1. 如果剩余的搜索路径与当前节点的key完全一致，更新当前节点的值（Val）即可。
2. 如果剩余的搜索路径与当前节点的key不完全一致，创建一个分支节点，并以新节点与当前节点key的共同前缀作为新的key。将新节点与当前节点的孩子节点作为两个孩子插入到分支节点的孩子列表中。然后将分支节点替换当前节点，使其成为新的扩展节点。如果新节点与当前节点没有共同前缀，则直接用生成的分支节点替换当前节点。

```go
matchlen := prefixLen(key, n.Key)
		if matchlen == len(n.Key) {
			dirty, nn, err := t.insert(n.Val, append(prefix, key[:matchlen]...), key[matchlen:], value)
			if !dirty || err != nil {
				return false, n, err
			}
			return true, &shortNode{n.Key, nn, t.newFlag()}, nil
		}
		branch := &fullNode{flags: t.newFlag()}
		var err error
		_, branch.Children[n.Key[matchlen]], err = t.insert(nil, append(prefix, n.Key[:matchlen+1]...), n.Key[matchlen+1:], n.Val)
		if err != nil {
			return false, nil, err
		}
		_, branch.Children[key[matchlen]], err = t.insert(nil, append(prefix, key[:matchlen+1]...), key[matchlen+1:], value)
		if err != nil {
			return false, nil, err
		}
		if matchlen == 0 {
			return true, branch, nil
    }
		return true, &shortNode{key[:matchlen], branch, t.newFlag()}, nil

```

如果插入成功，被修改节点的dirty标志将被置为true，hash标志会被置空（之前的哈希结果不再有效），并更新节点的诞生标记为当前时间。

以上步骤确保了插入操作的正确性和一致性，并且利用MPT的特性来实现高效的插入过程。

#### Delete

删除操作也需要找到与目标节点具有最长相同路径前缀的节点，记为Node。

如果Node是一个叶子节点或扩展节点：

1. 如果剩余的搜索路径与Node的key完全匹配，将整个Node删除。
2. 如果剩余的搜索路径与Node的key不匹配，表示需要删除的节点不在树中，删除失败。
3. 如果Node的key是剩余搜索路径的前缀，则对该节点的Val进行递归的删除调用。

如果Node是一个分支节点：

1. 删除Node的孩子列表中相应下标位置的节点。
2. 删除结束后，如果Node的孩子个数只剩下一个，那么将分支节点替换成一个叶子节点或扩展节点。

如果删除成功，被修改节点的dirty标志将被置为true，hash标志会被置空（之前的哈希结果不再有效），并更新节点的诞生标记为当前时间。

## MPT的主要特点

MPT（Merkle Patricia Tree）具有快速状态回滚的特点。在区块链公链环境下，由于可能发生分叉，导致区块链状态需要进行回滚的情况经常发生，特别是在以太坊等具有较短出块时间的链上。

状态回滚主要表现为两种情况：

1. 区块链内容发生了重组织，链头发生切换。
2. 区块链的世界状态（账户信息）需要进行回滚，即对之前的操作进行撤销。

MPT提供了一种机制，可以在发生碰撞时，零延迟地完成世界状态（即区块链系统中的全局状态）的回滚。这种优势的代价是需要浪费存储空间来冗余存储每个节点的历史状态。尽管每生成一个新的区块就会有一棵新的状态树，但它与前一区块的大部分节点是共享的。

在MPT中，每个节点在数据库中的存储都是值驱动的。当一个节点的内容发生变化时，其哈希也相应改变。MPT使用哈希作为数据库中的索引，确保每个值都有一条确定的记录。节点之间通过哈希值关联，因此当一个节点的内容发生变化时，对于父节点来说，只是哈希索引值发生了改变；然后父节点的内容也发生变化，产生一个新的父节点。这种影响递归传递到根节点，最终一次改变对应创建了一条从被改节点到根节点的新路径，而旧节点仍然可以通过旧根节点和旧路径访问。

通过这种方式，MPT实现了快速的状态回滚，旧的世界状态可以在需要时重新恢复，同时保持了历史状态的有效性和一致性。这为区块链的可靠性和安全性提供了重要保障。



参考文献：

[1] [Twox128](https://cyan4973.github.io/xxHash/) 

[2] [理解Substrate数据存储的底层实现Merkle Patricia Trie](https://blog.csdn.net/shangsongwww/article/details/119272573)

[3] [Merkle Patricia Trie详解 ](https://zhuanlan.zhihu.com/p/32924994)

[4] [死磕以太坊源码分析之MPT树](https://juejin.cn/post/6914506863375548429)
