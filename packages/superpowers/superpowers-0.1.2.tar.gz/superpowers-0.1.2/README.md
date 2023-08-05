# Superpowers
Sane map() for lists for unsane people.

## Usage

The following is valid code after using this library:

````python
from superpowers import patch, _
patch()

[1, 2, 3].map(_ * 3 + 3).map(lambda x: print(x))
# 6
# 9
# 12
print(['Hello', 'World'].map(_.upper).mkString(', '))
# HELLO, WORLD
[1, 2, 3, 4, 5].filter(_ > 3).map(print)
# 4
# 5
````
