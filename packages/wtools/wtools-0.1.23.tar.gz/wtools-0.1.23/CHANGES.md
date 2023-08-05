History
-------
Following lists the changes per released version.


**v0.1.23**, 2017-09-06:

- *eclipse_waf*; use replace() instead of lstrip() when parsing home directory with ${HOME} variable


**v0.1.22**, 2017-08-30:

- *eclipse_waf*; python3 fix, use decode('utf-8') on subprocess result


**v0.1.21**, 2017-08-30:

- *wtools*; use portable (python2/3) octal number specifier (mode=0o755)


**v0.1.20**, 2017-08-30:

- *eclipse_waf*; added preprocessor defines from compiler


**v0.1.19**, 2017-08-24:

- *eclipse_waf*; improved export of GNU C project files, added support for specifying project dependencies. Project dependencies must be a simple name of the project. This name must also be the directory name of that project and must reside in the same workspace and with the same nesting level.


**v0.1.18**, 2017-05-17:

- *wtools*; added utility function *install_dirs* for installation of empty directories
- *wtools*; added utility function *get_rpath* for creating a list of library search path to be used when debugging


**v0.1.17**, 2017-04-22:

- *wcc*; use SYSROOT environment variable when defined and not using sysroot command line option
- *tree*; added tree command for displaying task dependencies
- *wcc*; autoload *indent*, *tree* tools
- *eclipse_make*; rename eclipse module for exporting eclipse makefile projects from _weclipse_ into *eclipse_make*

**v0.1.16**, 2017-04-02:

- *eclipse_waf*; improved detection of CPPPATH when cross-compiling
- *eclipse_waf*; removed duplicate workspace includes
- *eclipse_waf*; use top level directory name for workspace include instead of appname
- *wcc*; fixed bug in sysroot command line option

**v0.1.15**, 2017-04-01:

- *eclipse_waf*; added eclipse-waf supporting cross-compile toolchains (clone of  **waflib/tools/extras/eclipse.py**)
- *eclipse_waf*; added command line option for using _install_ build command
- *eclipse_waf*; added command line option to preserve existing project files (.project, .cproject, .pydevproject)
- *eclipse_waf*; added exlcude patterns for _out/_ and _ext/out_ when searching for binaries 

**v0.1.14**, 2017-03-25:

- *wcc*; prevent exception in post build when creating symlinks

**v0.1.13**, 2017-03-23:

- added missing README.md file

**v0.1.12**, 2017-03-23:

- *wcc*; removed logic to detect and add include and library search paths; not needed as it is detected by waf itself.

- *wcc*; added optional **--sysroot** command line argument. Can be used add include and libary paths of (cross) compile toolchain.

- *wcc*; added **--eroot** command line argument. Can be used to add include and libary paths of local external dependencies.

**v0.1.11**, 2017-03-20:

- *wcc*; removed fixes from versions 0.1.9 and 0.1.10; not compatible with openwrt-mips-toolchain

**v0.1.10**, 2017-03-18:

- *wcc*; only add path to compiler to environment path when cross compiling

**v0.1.9**, 2017-03-18:

- *wcc*; added path to (cross-compile) gcc to environment path variable

**v0.1.8**, 2017-03-05:

- *wmake*; added command line option **--make-install** to use *make install* as default command on *make all*

**v0.1.7**, 2017-03-02:

- *wmake*; install files, symlinks for **install task** only

**v0.1.6**, 2017-03-02:

- *wmake*; added generic support for installing files and creating symlinks

**v0.1.5**, 2017-03-02:

- *wmake*; install configuration files if _etc_ directory exists

**v0.1.4**, 2017-02-27:

- *wmake*; improved export of shared libary search paths, vnum, symlinks

**v0.1.2**, 2017-02-21:

- *wcc*; prepend libary and include paths

**v0.1.1**, 2017-02-06:

- *general*; added changelog

**v0.1.0**, 2017-02-06:

- *general*; initial release

