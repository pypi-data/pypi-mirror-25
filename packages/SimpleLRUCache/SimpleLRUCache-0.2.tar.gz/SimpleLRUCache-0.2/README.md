# Introduction

It's often useful to have an in-memory cache. Of course, it's also desirable not to have the cache grow too large, and cache expiration is often desirable.

This module provides such a cache. It has limited memory and always removes the least-recently accessed element.

## Usage

```python
from simplelrucache import LRUCache

d = LRUCache(max_size=3)
d['a'] = 1
d['b'] = 1
d['c'] = 1
print d['a'] # KeyError
```

## Installation

```bash
pip install simplelrucache
```

