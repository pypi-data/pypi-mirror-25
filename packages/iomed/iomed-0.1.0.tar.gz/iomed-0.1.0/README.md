IOMED Medical Language CLI
==========================

# Instructions

1. Obtain a key to the IOMED Medical Language API visiting [https://dev.iomed.es](https://dev.iomed.es).
2. Export your key in your `~/.bashrc`:

```bash
export IOMED_MEL_KEY="your-key-here"
```

3. Install `iomed-cli`:

```bash
pip3 install iomed-cli
```

4. Run!

```bash
text=$(cat text)
iomed "$text"
```


