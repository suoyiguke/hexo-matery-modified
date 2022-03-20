---
title: deque-队列-线程安全集合.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: python
categories: python
---
---
title: deque-队列-线程安全集合.md
top: false
cover: false
toc: true
mathjax: true
date: 2022-03-20 18:16:49
password:
summary:
tags: python
categories: python
---
deque objects
class collections.deque([iterable[, maxlen]])
Returns a new deque object initialized left-to-right (using append()) with data from iterable. If iterable is not specified, the new deque is empty.

Deques are a generalization of stacks and queues (the name is pronounced “deck” and is short for “double-ended queue”). Deques support thread-safe, memory efficient appends and pops from either side of the deque with approximately the same O(1) performance in either direction.

Though list objects support similar operations, they are optimized for fast fixed-length operations and incur O(n) memory movement costs for pop(0) and insert(0, v) operations which change both the size and position of the underlying data representation.

If maxlen is not specified or is None, deques may grow to an arbitrary length. Otherwise, the deque is bounded to the specified maximum length. Once a bounded length deque is full, when new items are added, a corresponding number of items are discarded from the opposite end. Bounded length deques provide functionality similar to the tail filter in Unix. They are also useful for tracking transactions and other pools of data where only the most recent activity is of interest.

Deque objects support the following methods:

https://docs.python.org/release/3.10.2/library/collections.html?highlight=thread%20safe#collections.UserString
~~~
from collections import deque

d = deque(['f', 'g', 'h', 'i', 'j'])
for elem in d:  # iterate over the deque's elements
    print(elem.upper())
~~~



转json，先得转list。否则报错
~~~
import json
from collections import deque

if __name__ == '__main__':
    d = deque([1,2,3,4])
    z= list(d)
    print(json.dumps(z))

~~~
