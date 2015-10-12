#!/bin/zsh

rm **/*.pyc

ipython tests/trie/NodeTest.py
ipython tests/trie/TreeTest.py

ipython tests/veb_normal_test.py

ipython tests/xfast/static/TreeTest.py

ipython tests/deferred_test.py

ipython tests/mufast/static/TreeTest.py

ipython tests/deltafast/static/TreeTest.py

ipython tests/zfast/static/NodeTest.py
ipython tests/zfast/static/TreeTest.py

ipython tests/zfast/dynamic/NodeTest.py
ipython tests/zfast/dynamic/TreeTest.py

ipython tests/word_test.py
ipython tests/compare_word_test.py
