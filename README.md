# screeps.python.com

Python AI for [Screeps](https://screeps.com/). Source files in `src/` are
transpiled to JavaScript with Transcrypt and uploaded to the `python-dev`
Screeps branch.

## Build

Requires Python 3.11 and Node.js.

```bash
/opt/homebrew/bin/python3.11 build.py --build-only
```

Create `config.json` from `config.default.json`, add a Screeps auth token, then
deploy with:

```bash
/opt/homebrew/bin/python3.11 build.py
```

`config.json`, virtual environments, dependencies, and generated output are
excluded from Git.

## License

MIT. Based on Dabo Ross's `screeps-starter-python`; the original copyright and
license notice are retained in [LICENSE](LICENSE).
