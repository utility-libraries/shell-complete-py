# shell-complete-py
python package to generate shell-completion for your CLI

> Warning: This project is in the earliest phase possible

## Installation

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
# --completion print : prints the script for the user to handle it himself
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

You can also execute the module itself

```bash
python3 -m shell_complete [args...]
```

Or run the console-script

```bash
shell-complete [args...]
```
