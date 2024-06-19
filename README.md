[![CodeQL](https://github.com/utility-libraries/shell-complete-py/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/utility-libraries/shell-complete-py/actions/workflows/github-code-scanning/codeql)
[![Python Testing](https://github.com/utility-libraries/shell-complete-py/actions/workflows/python-testing.yml/badge.svg)](https://github.com/utility-libraries/shell-complete-py/actions/workflows/python-testing.yml)

# shell-complete-py
python package to generate shell-completion for your CLI

<!-- TOC -->
* [shell-complete-py](#shell-complete-py)
  * [Installation](#installation)
  * [Quick-Start](#quick-start)
    * [Installation](#installation-1)
    * [Testing if everything works](#testing-if-everything-works)
  * [Usage](#usage)
  * [Support completion types](#support-completion-types)
<!-- TOC -->

## Installation

[![PyPI - Version](https://img.shields.io/pypi/v/shell-complete)](https://pypi.org/project/shell-complete/)

```bash
pip3 install shell-complete
```

## Quick-Start

### Installation

```shell
pip3 install shell-complete
```

### Testing if everything works

To test if the package was installed successfully

```shell
$ eval "$(shell-complete shell_complete.__main__:parser)"  # via CLI
$ eval "$(shell-complete --completion)"  # via ShellCompleteAction
$ shell-complete <tab><tab>
--completion  --help        --root        --version
$ shell-complete --root <tab><tab>
dir/ .git/ .venv/  # example. this part will look different on your machine
```

or pipe it into a file and source that

```shell
$ shell-complete --completion > ./shell-complete.completion.bash
$ source ./shell-complete.completion.bash
```

## Usage

Either import and use the `generate(parser: ArgumentParser)` function directly or add the `ShellCompleteAction` to your argparse.

```python
import pathlib
from argparse import ArgumentParser
from shell_complete import ShellCompleteAction, types, associate


parser = ArgumentParser(prog="myprog")
...
# creates the --completion argument that's similar to --help or --version
# --completion print : prints the script for the user to handle it himself or use with eval
# --completion install : creates script in ~/.bash_completion.d/ and `source <script>` in ~/.bashrc
# --completion uninstall : removes script in ~/.bash_completion.d/ and `source <script>` in ~/.bashrc
parser.add_argument('--completion', action=ShellCompleteAction,
                    help="Generate a bash-completion-script")

# add custom type converter that can still auto-complete
@associate(types.directory)
def dirtype(value: str) -> pathlib.Path:
    return pathlib.Path(value)

# smart autocompletion
parser.add_argument('--dest', type=dirtype)  # the custom type
parser.add_argument('--source', type=types.file)  # or the builtins
parser.add_argument('--bind', type=types.ip_address)
parser.add_argument('--database', type=types.known_hosts)

# subparsers are also supported
subparsers = parser.add_subparsers()
subcommand = subparsers.add_parser("sub")
# Completion is only suggested after typing `myprog sub`
subcommand.add_argument('--hidden', types=types.ip_address)
```

You can also execute the module itself

```bash
python3 -m shell_complete [--root ROOT] parser
```

Or run the console-script

```bash
shell-complete [--root ROOT] parser
```

## Support completion types

Basic completion types can be imported via

```python
from shell_complete import types
from shell_complete.argparse import types  # both are the same
```

| type                      | info                                    |
|---------------------------|-----------------------------------------|
| `types.path`              | any type of path (file and directories) |
| `types.file`              | completion for files                    |
| `types.directory`         | completion for directories              |
| `types.mac_address`       | mac addresses                           |
| `types.ip_address`        | ip addresses                            |
| `types.ipv4_address`      | ipv4 addresses                          |
| `types.ipv6_address`      | ipv6 addresses                          |
| `types.network_interface` | names of network interfaces             |
| `types.inet_services`     | names of inet services                  |
| `types.uid`               | available user id's                     |
| `types.gid`               | available group id's                    |
| `types.service`           | available systemctl services            |
| `types.user_group`        | user:group pair                         |
| `types.user_at_host`      | user@host pair                          |
| `types.known_hosts`       | name of known hosts                     |
