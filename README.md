# Bossy

Bossy is a tool for writing and running shell commands in Python.


## Example

Create a file called 'Bossfile' in the current directory with these contents:

```python
from bossy import *

@command
def hello():
    print "Hello, World!"

@command
@argument('-r', '--repetitions', default=1, help="Number of times to print")
def hello_n(repetitions):
    for i in xrange(repetitions):
        print "Hello, World!"
```

Run your commands via the `bossy` executable:

```bash
$ bossy --help
usage: bossy [-h|-v|-f BOSSFILE] <command> ...

Run commands from a Bossfile.

global options:
  -f BOSSFILE, --file BOSSFILE
                        Location of an alternative Bossfile to use. By
                        default, bossy will look for a file called 'Bossfile'
                        in the current directory.
  --pdb                 Launch the Python Debugger on uncaught exceptions.
  -v, --version         show program's version number and exit
  -h, --help            show this help message and exit

sub-commands:
  <command>
    hello_n             Print something to the console several times.
    hello               Print something to the console.

$ bossy hello
Hello, World!

$ bossy hello_n -h
usage: bossy hello_n [-h] [-r REPETITIONS]

Print something to the console several times.

optional arguments:
  -h, --help            show this help message and exit
  -r REPETITIONS, --repetitions REPETITIONS
                        Number of times to print

$ bossy hello_n -r 3
Hello, World!
Hello, World!
Hello, World!
```


## (Un)license

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this
software, either in source code form or as a compiled binary, for any purpose,
commercial or non-commercial, and by any means.

In jurisdictions that recognize copyright laws, the author or authors of this
software dedicate any and all copyright interest in the software to the public
domain. We make this dedication for the benefit of the public at large and to
the detriment of our heirs and successors. We intend this dedication to be an
overt act of relinquishment in perpetuity of all present and future rights to
this software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
