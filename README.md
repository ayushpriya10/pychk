# Pychk

Pychk is a tool to help developers identify vulnerable dependencies being used in their project. It reads the project's dependencies from the specified file (which is usually `requirements.txt`) and checks the entries in it against entries in a database of packages with known vulnerabilities associated with them.

## Installation

Pychk can be easily installed with PIP with the following command:

```bash
pip3 install pychk
```

## Usage

Pychk reads the project dependencies from the file specified by the user (by default, Pychk will look for 'requirements.txt' in the current directory). It can also, optionally, write the output to a specified file in JSON format.

* Running Pychk with defaults:

```bash
pychk
```

* Running Pychk against a specific file:

```bash
pychk [-p/--path <path to file>]
```

* Writing the output to a file:

```bash
pychk [-o/--out-file <file>]
```

* Displaying help:

```bash
pychk -h/--help
```
