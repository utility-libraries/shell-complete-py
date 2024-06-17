[![CodeQL](https://github.com/utility-libraries/shell-complete-py/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/utility-libraries/shell-complete-py/actions/workflows/github-code-scanning/codeql)
[![Python Testing](https://github.com/utility-libraries/shell-complete-py/actions/workflows/python-testing.yml/badge.svg)](https://github.com/utility-libraries/shell-complete-py/actions/workflows/python-testing.yml)

# shell-complete-py
python package to generate shell-completion for your CLI

## Installation

[![PyPI - Version](https://img.shields.io/pypi/v/shell-complete)](https://pypi.org/project/shell-complete/)

```bash
pip3 install shell-complete
```

## Usage

Either import and use the `generate(parser: ArgumentParser)` function or directly the `ActionGenerate`

```python
from argparse import ArgumentParser
from shell_complete import ActionShellComplete, types

parser = ArgumentParser()
...
# creates the --completion argument that's similar to --help or --version
# --completion print : prints the script for the user to handle it himself or use with eval
# --completion install : creates script in ~/.bash_completion.d/ and `source <script>` in ~/.bashrc
# --completion uninstall : removes script in ~/.bash_completion.d/ and `source <script>` in ~/.bashrc
parser.add_argument('--completion', action=ActionShellComplete,
                    help="Generate a bash-completion-script")
...
# smart autocompletion
parser.add_argument('--source', type=types.file)
parser.add_argument('--bind', type=types.ip_address)
parser.add_argument('--database', type=types.known_hosts)
```

> The following usages are not supported yet

You can also execute the module itself

```bash
python3 -m shell_complete [args...]
```

Or run the console-script

```bash
shell-complete [args...]
```
