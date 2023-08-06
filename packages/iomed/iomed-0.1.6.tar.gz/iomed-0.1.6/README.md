IOMED Medical Language API
==========================

# Instructions

1. Obtain a key to the IOMED Medical Language API visiting [https://dev.iomed.es](https://dev.iomed.es).
2. Export your key in your `~/.bashrc`:

```bash
export IOMED_MEL_KEY="your-key-here"
```

3. Install `iomed`:

```bash
pip3 install iomed
```

### Usage as cli

4. Run!

```bash
text=$(cat text)
iomed "$text"
```

### Usage as python library

```python
from iomed import MEL
mel = MEL('your-api-key')
result = mel.parse('dolor en el pecho desde hace dos horas')
```

There is a [limitation](/pricing/#limits) of a certain amount of characters per request. If you want to annotate a big text, you will have to split it. We will provide a way to do it automatically with this library in the future.
