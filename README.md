xdt99: TI 99 Cross-Development Tools
====================================

The **TI 99 Cross-Development Tools** (xdt99) are a small suite of programs that
facilitate the development of programs for the TI 99 family of home computers on
modern computer systems:

 * `xas99`: A TMS9900 cross-assembler
 * `xga99`: A GPL cross-assembler
 * `xbas99`: A TI BASIC and TI Extended BASIC lister and encoder
 * `xdm99`: A disk manager for sector-based TI disk images
 * `xvm99`: A volume manager for nanoPEB/CF7A Compact Flash cards
 * `xdt99-mode`: A major mode for the GNU Emacs text editor
 * `xdt99 IDEA`: A plugin for the IntelliJ IDEA development environment

The `xas99` cross-assembler supports all documented TMS9900 opcodes and should
assemble any existing assembly code for the TI 99 without modification.  Object
code generated by `xas99` is identical to compressed or uncompressed object code
produced by the original TI Editor/Assembler package.  Modern extensions such as
local labels and macro support simplify the writing of assembly programs on
modern hardware.

The `xga99` GPL cross-assembler generates GROM image files for TI's proprietary
Graphics Programming Language (GPL).  The GPL assembler is a quick way to
translate self-written GPL programs into RPK cartridge files that can be run
with the MESS emulator.

The `xbas99` BASIC tool encodes TI BASIC and TI Extended BASIC programs into
their internal format that can be loaded by the BASIC interpreter using
the `OLD` command.  Conversely, the tool also lists BASIC program files
similarly to the `LIST` command. 

The `xdm99` disk manager works with sector-based TI disk images used by most
emulators, including MESS.  `xdm99` also supports disk-less files in TIFiles and
V9T9 format.  The `xvm99` volume manager extends the `xdm99` functionality to CF
cards used by the nanoPEB/CF7A devices.

The `xdt99-mode` and `xdt99 IDEA` plugins provide editor support for writing
assembly and TI Extended BASIC programs using the GNU Emacs and the IntelliJ
IDEA development environments, respectively.  Plugin features include syntax
highlighting, navigation, and semantic renaming, among others.

For additional information, please refer to the [xdt99 homepage][1] or the
[xdt99 manual][4].  Windows users unfamiliar with working with the command line
will find some platform-specific information in the [Windows tutorial][5].

**Latest version: 1.5.0**

The latest binary distribution of xdt99 is available on the project
[releases page][2] on GitHub.  xdt99 requires [Python 2.7.x][6] and runs on any
platform that Python supports, including Linux, Windows, and OS X.

xdt99 is released under the GNU GPLv2.  All sources are available on
[GitHub][3].


Download and Installation
-------------------------

Download the latest [binary release][2] from GitHub.  Alternatively, clone the
entire xdt99 GitHub [repository][3].

All tools -- `xas99` cross-assembler, `xga99` GPL cross-assembler, `xbas99`
BASIC tool, `xdm99` disk manager, and `xvm99` volume manager -- are standalone
self-contained Python programs (but `xvm99` requires `xdm99`).  Simply place the
files `xas99.py`, `xga99.py`, `xbas99.py`, `xdm99.py`, and `xvm99.py` somewhere
into your `$PATH` or wherever your Python installation will find them.

The `xdt99-mode` and `xdt99 IDEA` plugins provide editor support and may be used
independently of the other xdt99 tools.  Likewise, `xas99` and others may be
used without these plugins.

First-time xdt99 users running Windows will find additional information about
installation and some tips on getting started in the [Windows tutorial][5].
Users of other platforms who are unfamiliar with the command line may also find
some tips in there.


Basic Usage: `xas99`
--------------------

This is just a brief overview of the most common usages for `xas99`.  For
detailed information, please refer to the [xdt99 homepage][1] or the [manual][4]
included with xdt99.

Generate object code for the Editor/Assembler cartridge, option 3:

    $ xas99.py [-R] [-C] <source file>
    
Generate program image for the Editor/Assembler cartridge, option 5:

    $ xas99.py -i [-R] <source file>

Generate cartridge file for the MESS emulator:

    $ xas99.py -c [-R] <source file>

Generate program image embedded in Extended BASIC loader:

    $ xas99.py --embed [-R] <source file>

Generate list file diagnostic output:

    $ xas99.py [-R] <source file> -L <list file>

Generate jumpstart image for fast code, assemble, run cycles:

    $ xas99.py --jumpstart [-R] <source file>
    $ mess64 ti99_4ae -cart lib/jumpstart.rpk -flop1 <js disk> <MESS options>
 
For a complete overview of the available command-line options, see `xas99.py
-h`.

`xas99` offers various language extensions to the original Editor/Assembler
module:

 * Relaxed syntax (e.g., labels, comments, whitespace, case insensitivity)
 * Improved expressions (e.g., Boolean operators, binary numbers, parentheses)
 * Label continuations and local labels (e.g., `! dec r0; jne -!`)
 * New directives (e.g., `BCOPY` for binary includes)
 * Conditional assembly (e.g., `.ifdef`)
 * Macros (`.defm`)

Please refer to the [xdt99 manual][4] for a detailed description of these
features.


Basic Usage: `xga99`
--------------------

This is just a brief overview of the most common usages for `xga99`.  For
detailed information, please refer to the [xdt99 homepage][1] or the manual
included with xdt99.

Assemble GPL source file into GPL byte code:

    $ xga99.py <source file>

Generate image file for GROM/GRAM device:

    $ xga99.py -i <source file>

Generate cartridge file for the MESS emulator:

    $ xga99.py -c <source file>

Assemble source file using "RAG GPL Assembler" syntax style:

    $ xga99.py <source file> -s rag

For a complete overview of the available command-line options, see `xga99.py
-h`.


Basic Usage: `xbas99`
---------------------

This is just a brief overview of the most common usages for `xbas99`.  For
detailed information, please refer to the [xdt99 homepage][1] or the manual
included with xdt99.

List TI BASIC or TI Extended BASIC program on screen:

    $ xbas99.py -l <program file>

Decode BASIC program to source format (i.e., list to file):

    $ xbas99.py -d <program file> [-o <output file>]

Create BASIC program in internal format for BASIC interpreter:

    $ xbas99.py [-c] <source file> [-o <output file>]

List BASIC program stored on disk image (advanced use):

	$ xdm99.py <disk image> -p <prog name> | xbas99.py -l -

For a complete overview of the available command-line options, see `xbas99.py
-h`.


Basic Usage: `xdm99`
--------------------

This is just a brief overview of the most common usages for `xdm99`.  For
detailed information, please refer to the [xdt99 homepage][1] or the manual
included with xdt99.

Print disk catalog on screen:

    $ xdm99.py <disk image>

Extract one or more files from disk image to local file system:

    $ xdm99.py <disk image> -e <file> ...

Extract files in TIFiles or v9t9 format:

    $ xdm99.py <disk image> -t -e <file> ...
    $ xdm99.py <disk image> -9 -e <file> ...

Print file contents to screen:

    $ xdm99.py <disk image> -p <file> ...

Add local files to disk image:

    $ xdm99.py <disk image> -a <file> ... [-f <format>] [-n <name>]

Rename file on disk image:

    $ xdm99.py <disk image> -r <old name>:<new name> ...

Delete file on disk image:

    $ xdm99.py <disk image> -d <file> ...

Convert TIFiles files or v9t9 files to plain files:

    $ xdm99.py -F <TIFiles file> ...
    $ xdm99.py -F <TIFiles file> ... -9

Convert plain files to TIFiles files or v9t9 files:

    $ xdm99.py -T <plain file> ... [-f <format>] [-n <name>]
    $ xdm99.py -T <plain file> ... -9 [-f <format>] [-n <name>]

Print contents of TIFiles file:

    $ xdm99.py -P <TIFiles file>

Initialize blank disk:

    $ xdm99.py <disk image> --initialize <size> [-n <name>]

Resize disk image:

    $ xdm99.py <disk image> -Z <sectors>

Repair disk image with corrupt files or other inconsistencies:

    $ xdm99.py -R <disk image>

Override disk geometry:

    $ xdm99.py <filename> --set-geometry <geometry>

Print sector dump:

    $ xdm99.py <disk image> -S <sector>

For a complete overview of the available command-line options, see `xdm99.py
-h`.


Basic Usage: `xvm99`
--------------------

This is just a brief overview of the most common usages for `xvm99`.  For
detailed information, please refer to the [xdt99 homepage][1] or the manual
included with xdt99.

Show information about volumes:

    $ xvm99.py <device> <volumes>

Read disk images from volumes:

    $ xvm99.py <device> <volumes> -r <filename> [--keep-size]

Write disk image to volumes:

    $ xvm99.py <device> <volumes> -w <disk image> [--keep-size]

`<device>` is the platform-specific name of the Compact Flash card drive, e.g.,
`/dev/sd<X>` on Linux, `/dev/Disk<X>` on Mac OS X, or `\\.\PHYSICALDRIVE<X>` on
Windows.

`<volumes>` is a single value or a combination of values and ranges, e.g.,
`1,3-4,6-10`.  If more than one volume is supplied, the same command is applied
to *all* volumes.

Additionally, `xvm99` extends most of the functionality of `xdm99` to disk
volumes.

Print disk catalog of one or more volumes:

    $ xvm99.py <device> <volumes> -i

Add file to one or more volumes:

    $ xvm99.py <device> <volumes> -a <file> [-n <name>] [-f <format>]

For a complete overview of the available command-line options, see `xvm99.py
-h`.


Contact Information
-------------------

The xdt99 tools are released under the GNU GPL, in the hope that TI 99
enthusiasts may find them useful.

Please email all feedback and bug reports to the developer at
<xdt99dev@gmail.com>.


[1]: https://endlos99.github.io/xdt99
[2]: https://github.com/endlos99/xdt99/releases
[3]: https://github.com/endlos99/xdt99
[4]: https://github.com/endlos99/xdt99/blob/master/MANUAL.md
[5]: https://github.com/endlos99/xdt99/blob/master/WINDOWS.md
[6]: https://www.python.org/downloads/
