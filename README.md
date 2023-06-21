# Parallel Walk
This is a simple multiprocessing version of python os.walk.

## How to install

```bash
$ pip install para_walk
```

## How to use

```python
from para_walk import pwalk


for root, directories, files in pwalk(TARGET_DIR, PARALLEL, **kargs):
	# **kargs is kargs pass to os.walk
	continue
```
