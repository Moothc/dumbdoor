# dumbdoor 

The script follows the idea of server-client, where the client (dumb) can 
update the server (door), just implement a "plugin" and send it through 
the dumb to the door.

## Example

```python
plugins/plugin.py

print("Hello world, here is the dumb.")

def foo():
  s = 77 + 33
  return s - 10
```
```
terminal tab 1
$ python3.8 src/door.py

terminal tab 2
$ python3.8 src/dumb.py
```
