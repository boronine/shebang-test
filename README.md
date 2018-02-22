[![Build Status](https://travis-ci.org/boronine/shebang-test.svg?branch=master)](https://travis-ci.org/boronine/shebang-test)

# Maximum shebang length test

Use this script to test maximum shebang length on your platform. Works with Python 2 and 3.

```bash
python shebang.py
```

See also this [definitive shebang resource](https://www.in-ulm.de/~mascheck/various/shebang/).

## Findings

| Platform      | Maximum shebang length |
| ------------- | ---------------------- |
| MacOS 10.13.3 | 512                    |
| Linux 4.9.46  | greater than 1MB       |

Submit your findings with PR.
