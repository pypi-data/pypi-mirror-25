# Installation

```zsh
pip pyshaun
```

# How to use quickly

```python
import pyshaun

raw = pyshaun.load('{ hello : "world" }')
from_file = pyshaun.load_file('myfile.sn')

print(raw['hello'])
print(from_file)
```

