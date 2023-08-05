Summary
-------
This package contains a collection of tools for the [waf](https://waf.io) build environment intended for both native- as well cross compilation of C/C++ based projects.

Following provides a non-exhausting list of functions provided:

- C/C++ setup gcc (cross-compile) toolchains (**wtools.wcc**)
- C/C++ export to makefiles (**wtools.wmake**)
- C/C++ export to Eclipse projects (**wtools.weclipse**)
- C/C++ code formatting (**wtools.indent**)

Take a look at the [wafbook](https://waf.io/book/) For a detailed description of the _waf_ build system.


Installation
------------
The *wtools* package can be installed using pip:

    pip install wtools --upgrade --no-cache-dir --user

As alternative you can also clone the repository and install the latest
revision:

    cd ~
    git clone https://bitbucket.org/Moo7/wtools.git wtools
    pip install -e ~/wtools --user


Support
-------
If you have any suggestions for improvements and/or enhancements, please feel free to drop me a note by creating an [issue](https://bitbucket.org/Moo7/wtools/issues) at the [wtools](https://bitbucket.org/Moo7/wtools) projects page.

