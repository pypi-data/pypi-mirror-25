# airtight

If you're going to ```import antigravity```, you'd better make sure the hatch is closed.

The **airtight** package is written for Python 3.6+. It provides idiosyncratic code that somewhat simplifies the creation and debugging of command-line python scripts.

## simpler than a template

Instead of copying some 50-line template for your python script and then writing a bunch of calls to [argparse](https://docs.python.org/3/library/argparse.html) and [logging](https://docs.python.org/3/library/logging.html) just build some lists describing the arguments and logging level you want and invoke ```artight.cli.configure_commandline()```:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example script template using the airtight module
"""

from airtight.cli import configure_commandline
import logging

DEFAULT_LOG_LEVEL = logging.WARNING
OPTIONAL_ARGUMENTS = [
    # each argument is a list: short option, long option, default value, 
    # help string, required?
    ['-l', '--loglevel', 'NOTSET',
        'desired logging level (' +
        'case-insensitive string: DEBUG, INFO, WARNING, or ERROR',
        False],
    ['-v', '--verbose', False, 'verbose output (logging level == INFO)',
        False],
    ['-w', '--veryverbose', False,
        'very verbose output (logging level == DEBUG)', False],
    ['-x', '--custom', 7, 'your custom argument', False]
]
POSITIONAL_ARGUMENTS = [
    # each argument is a list with 3 elements: name, type, help
    ['foovar', str, 'some input value that you want']
]


def main(**kwargs):
    """Main function of your script.

    kwargs -- keyword arguments as parsed from the command line
    """
    # your additional code here


if __name__ == "__main__":
    main(**configure_commandline(
            OPTIONAL_ARGUMENTS, POSITIONAL_ARGUMENTS, DEFAULT_LOG_LEVEL))
```


## make debug logging just a wee bit easier

The ```airtight.logging``` module provides two methods: ```configure_logging()```, which is used by ```airtight.cli.configure_commandline()```, and ```flog()```, which reduces typing when you want to log a variable's name and value.

So, you can write:

```python
> from airtight.logging import flog
> fish = 'salmon'
> flog(fish)
DEBUG:foo_script: fish: 'salmon'
```

```flog()``` logs to DEBUG by default, but an optional keyword argument ```level``` may be used to specify another standard level, e.g.:

```python
> from airtight.logging import flog
> import logging
> fish = 'salmon'
> flog(fish, level=logging.WARNING)
WARNING:foo_script: fish: 'salmon'
```

Another optional keyword argument (```comment```) may be specified. A string value supplied via this argument will be postfixed to the logged variable name and value, thus:

```python
> from airtight.logging import flog
> fish = 'salmon'
> flog(fish, comment='I like this fish!')
DEBUG:foo_script: fish: 'salmon' I like this fish!
```

## etc.

Bug reports and feature requests are welcome, but really I'd prefer pull requests. 

## todo

 - docstrings






