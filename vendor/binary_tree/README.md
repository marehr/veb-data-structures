Self-Balancing Binary Tree
=============

Python [binary tree] module that is [self-balancing].

Note: There are probably better libraries that do what you want. Python "bisect" library performs binary search on lists. Additionaly, the "blist" package is awesome and includes "sortedlist" and "sorteddict" among others.

What Problem This Solves
------------------------

* Small space,  Ave: O(n), Max: O(n)
* Fast search,  Ave: O(log n), Max: O(log n)
* Fast insert,  Ave: O(log n), Max: O(log n)
* Fast delete,  Ave: O(log n), Max: O(log n)

How This Solves It
------------------
Uses [AVL trees].

Usage
-----
New tree

`tree = BinaryTree()`

Insert Entity into the tree

`tree.insert(5)`

The Tree can't deal with duplicate Elements, but you can solve this by using
tuples, where the second argument is unique.

```python
tree.insert(5)
tree.insert((5,1))
tree.insert((5,2))
```

[self-balancing]: https://en.wikipedia.org/wiki/Self-balancing_binary_search_tree
[binary tree]: https://en.wikipedia.org/wiki/Binary_tree
[AVL trees]: http://en.wikipedia.org/wiki/AVL_tree
