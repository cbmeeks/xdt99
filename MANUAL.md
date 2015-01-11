xdt99: TI 99 Cross-Development Tools
====================================

The **TI 99 Cross-Development Tools** (xdt99) are a small suite of programs that
facilitate the development of programs for the TI 99 family of home computers on
modern computer systems.

As of this release, the cross-development tools comprise

 * `xas99`, a TMS9900 cross-assembler, and
 * `xdm99`, a command-line disk manager for sector-based TI disk images.

Both programs are written in Python and thus run on any platform
that Python supports, including Linux, Windows, and Mac OS X.

The [xdt99 homepage][1] is hosted on GitHub.  You can download the latest
[binary release][2] of xdt99 or clone the entire source code [repository][3].

The xdt99 tools complement similar projects such as the excellent [TI Image
Tool][5] or the [TI 99/Sim emulator][6] by offering slightly different
approaches or extending their platform availability.


Installation
------------

Download the latest [binary release][2] from GitHub (recommended) or clone the
[xdt99 repository][3].  Please note that the big download buttons on top of the
xdt99 homepage on GitHub will include the entire repository; this is probably
*not* what you want.

You will also need a working copy of [Python 2.x][4] installed on your computer.
`xdt99` has been developed using Python 2.7, but other versions may work as
well.  Note, however, that compatibility with Python 3 has be postponed to a
later release for now.

Both the `xas99` cross-assembler and the `xdm99` disk manager are self-contained
Python programs.  Simply place the files `xas99.py` and `xdm99.py` somewhere
into your `$PATH` or where your command-line interpreter will find them.

The `example` directory of the binary distribution contains some sample files
that are referenced throughout this manual.


xas99 Cross-Assembler
---------------------

The `xas99` cross-assembler translates TMS9900 assembly code into executable
programs for the TI 99 home computer equipped with the Editor/Assembler module
or the Mini Memory module.

Invoking `xas99` in standard mode will assemble a TMS9900 assembly source code
file into an object code file that may be loaded using the Editor/Assembler
module option 3.

    $ xas99.py -OR ashello.asm

`xas99` can also produce program images files for the Editor/Assembler module
option 5 or RPK cartridge files for the MESS emulator:

	$ xas99.py -OR -i ashello.asm
	$ xas99.py -OR -c ashello.asm

All existing assembly code for the TI 99, e.g., the Tombstone City source code
shipped with the Editor/Assembler module, should cross-assemble using `xas99`
without requiring any source code modifications.

The object code generated by `xas99` is identical to uncompressed object code
produced by the original TI Editor/Assembler package.  This includes all of its
quirks, such as shortened object code lines or excessive address specifications,
but hopefully none of its bugs, such as invalid tags for certain `DEF`s.

For a detailed step-by-step example on how to cross-assemble and run an assembly
program using the xdt99 tools and the MESS emulator please refer to the Example
Usage section below.

Finally, please note that even though the object code format of the TI 99 home
computer shares many similarities with that of other TMS9900-based systems, most
notably the TI 990 mini computer, `xas99` currently targets the TI 99 only.


### Assembling Source Code

The `xas99` cross-assembler reads an assembly source code file and generates an
uncompressed object code file that is suitable for the original TI 99
Editor/Assembler loader.

	$ xas99.py -OR ashello.asm
	$ xas99.py -OR ashello.asm -o HELLO-O

The output parameter `-o` may be used to override the default output file name.

The assembly options parameter `-O` tells `xas99` which Editor/Assembler options
it should apply during assembly.  Currently, only option `R` (register symbols)
is supported; options `S` (symbol table), `L` (generate listing), and `C`
(compress object code) are ignored.

You will need to add `-OR` if you prefer to write `MOV R0,*R1+` etc. instead of
`MOV 0,*1+` in your source code.

`xas99` will report any errors to `stderr` during assembly.  Note that the
generated object code may differ from the code generated by the Editor/Assembler
package in the case of errors.  `xas99` is slightly more permissive than the
Editor/Assembler, but it should be able to assemble any source that the
Editor/Assembler package can assemble.


### Creating Program Images

The image parameter `-i` tells `xas99` to generate an image file that can be
loaded using Editor/Assembler option 5.

	$ xas99.py -OR -i ashello.asm

The `-i` parameter eliminates the need for the `SAVE` utility program shipped
with the Editor/Assembler package.  Just like `SAVE`, `xas99` will honor the
symbols `SLOAD`, `SFIRST`, and `SLAST` to generate the image.  If those symbols
are missing, `xas99` will relocate the relocatable program code to memory
location `>A000` and include the resulting parts above `>A000` into the image.

All the usual restrictions for program images apply.  In particular, the first
word of the image must be an executable instruction.


### Creating MESS Cartridges

The cartridge parameter `-c` tells `xas99` to create an RPK cartridge file that
can be used by the MESS emulator.

	$ xas99.py -OR -c ascart.asm -n "HELLO WORLD"

The optional name parameter `-n` overrides the default name of the program that
shows up in the TI 99 menu selection screen.

The resulting RPK archive is a ZIP file containing the actual program code plus
various information for the MESS emulator on how to execute the program.
Typically, RPK files are passed as arguments to the MESS executable, or they may
be mounted while running MESS using the emulator on-screen menu.

    $ mess64 ti99_4ae -cart ascart.rpk

When the `-c` option is given, `xas99` will automatically generate suitable GPL
header information and relocate the program to address `>6030`, but it will not
process the source code any further.  In particular, the usual restrictions on
using VDP memory access routines apply.

Note that cartridge file generation is still an experimental hack that may not
work without specific adaptions to your assembly source code.


### TMS9900 Assembly Support

The `xas99` is a complete TMS9900 assembler supporting all documented TMS9900
opcodes.  TMS9995 opcodes such as `MPYS` and `DIVS` are currently not supported
but may be added in a future release.

`xas99` understands all assembler directives described in the Editor/Assembler
manual that are supported by both TI 99 assembler and loader, i.e.,

	DEF REF EQU DATA BYTE TEXT BSS BES AORG RORG DORG EVEN
	IDT DXOP COPY END

Note that the `DORG` directive *is* supported, even though the TI assembler does
not do so.

The following directives are not supported by the TI 99 loader and are thus
ignored by `xas99`:

    PSEG PEND CSEG CEND DSEG DEND LOAD SREF

Listing generation is currently not supported, so directives

	LIST UNL PAGE TITL

are also ignored.


#### Source Code Organization

The `COPY` directive is used to break large assembly sources into individual
files.

`xas99` will search the current source directory for appropriately named source
files.  For example, assembling

	$ xas99.py src/file1.asm

where `file1.asm` contains the instruction `COPY "DSK1.FILE2"` will search for
include files

	src/FILE2
	src/FILE2.ASM
	src/FILE2.S

and its corresponding lower-case variants.  `COPY` also supports native file
paths, e.g., `COPY "/home/ralph/ti/src/file2.asm"`.


xdm99 Disk Manager
------------------

`xdm99` is a command-line tool for cataloging and manipulating sector-based TI
disk images used by most emulators, including MESS.  `xdm99` also supports the
TIFiles file format that retains TI-specific meta data for files that originate
from TI disk images.


### Cataloging Disks

The default operation of `xdm99` when invoked without any options is to print
the file catalog of the disk image to `stdout`:

	$ xdm99.py ed-asm.dsk
	ED-ASSM   :     97 used  263 free   90 KB  1S/1D  40 TpS
	----------------------------------------------------------------------------
	ASSM1         33  PROGRAM       8192 B
	ASSM2         18  PROGRAM       4102 B
	EDIT1         25  PROGRAM       5894 B
	SAVE          13  DIS/FIX 80    3072 B   36 recs
	SFIRST/O       3  DIS/FIX 80     512 B    5 recs
	SLAST/O        3  DIS/FIX 80     512 B    4 recs

The top line shows the name of the disk, the number of used and free sectors as
well as the disk geometry.  For each file, the number of used sectors, the file
type, the file length, and the actual number of records is shown.  If present,
the file modification time is also shown.

`xdm99` will warn about any inconsistencies it may find, e.g., blocks claimed by
files but not allocated in the allocation map.  When assembling programs
natively these inconsistencies happen more frequently than one would assume.
Files affected by inconsistencies are flagged with `ERR` in the catalog.  You
can try the `-R` option to automatically repair disks with inconsistencies.


### Extracting Files

The extract parameter `-e` extracts one or more files from a disk image to the
local file system.

	$ xdm99.py work.dsk -e HELLO-S CART-S

The local output file name is derived automatically from the TI file name but
may be overridden with the `-o` parameter.

	$ xdm99.py work.dsk -e HELLO-S -o hello.asm

To print the contents of a file to `stdout`, the print parameter `-p` may also
be used:

	$ xdm99.py work.dsk -p HELLO-S

In general, printing files only makes sense for files in DIS/FIX or DIS/VAR
format.  Following Unix conventions, `-p` is equivalent to combining parameters
`-e` and `-o "-"`.

Note that extracting files will yield the file contents only.  In order to
retain file meta data about file type and record length, use the TIFiles format
described below.


### Manipulating Disks

The add parameter `-a` adds local files to the disk image.  `xdm99` will infer a
suitable TI file name from the local file name unless an explicit file name is
given by the `-n` parameter.  If the file is not of type `PROGRAM`, the file
type must be given using the `-f` parameter.

	$ xdm99.py work.dsk -a ashello.asm -n HELLO-S -f DIS/VAR80

The syntax for `-f` is fairly permissible, e.g., `DIS/FIX 80`, `DISFIX80`, or
`DF80` all work.

The delete parameter `-d` deletes one or more files on the disk.

	$ xdm99.py work.dsk -d HELLO-I

Note that the current implementation of `xdm99` does not perform a "secure
erase", i.e., parts of the file contents may remain hidden in the sectors of the
disk image.

File operations do not retain the overall sector structure of the disk.  In
particular, all files will be defragmented whenever files are added or deleted
with `-a` or `-d`, respectively, or when the disk is repaired with `-R`.  Simply
cataloging the disk, however, will *not* modify the disk image.

By default, all modifying disk operations will change the disk image directly.
To create an independent copy of the original disk image with the changes
applied, the `-o` parameter may be used.


### TIFiles

Extracting files from a TI disk image to the local file system will lose certain
TI-specific file information, such as the file type or the record length.  In
order to retain this meta information along with the file contents, the TIFiles
format was created.

`xdm99` supports the TIFiles format for files by using the `-t` option.  To
extract a file in TIFiles format, simply add `-t` to the extract operation:

	$ xdm99.py work.disk -t -e HELLO-S

By default, files extracted in TIFiles format will have extension ``.tfi`.

To add a file in TIFiles format, add `-t` to the add operation:

	$ xdm99.py work.disk -t -a hello-s.tfi

As all information about the TI file name and the TI file format is retrieved
from the TIFiles meta data, parameters `-n` and `-f` are ignored when used in
combination with `-t`.

The info parameter `-I` displays the meta file information contained in a
TIFiles file, while the print parameter `-P` dumps the file contents to
`stdout`:

	$ xdm99.py -I hello-s.tfi
	$ xdm99.py -P hello-s.tfi

`xdm99` can also convert from TIFiles files to plain files and vice versa
without relying on disk images:

	$ xdm99.py -F hello-s.tfi
	$ xdm99.py -T hello.asm -f DIS/VAR80 -n HELLO-S -o hello-s.tfi

Note that creating a TIFiles file using the `-T` option usually requires
information about the TI file name and the TI file type, similar to adding files
to a disk image by using `-a` without the `-t` option.


### Analyzing Disks

The check parameter `-c` analyzes a disk image for errors and prints a summary
to `stderr`.  While all disk operations, including cataloging, also check and
report any disk errors found, the `-c` parameter restricts the output of `xdm99`
to those errors only.

	$ xdm99.py -c work.dsk

The `-c` parameter also causes `xdm99` to set its return value to non-zero for
warnings, making it simple to write shell scripts for batch processing bad disk
images.

The repair option `-R` tries to fix any disk errors, mostly by deleting
erroneous files from it.

	$ xdm99.py -R work.dsk

The repair operation is likely to cause data loss, so it's best to extract
erroneous files beforehand or to specify an alternative output file with `-o`.

The sector dump parameter `-s` prints the hexadecimal contents of individual
sectors to `stdout`.  This can be used to further analyze disk errors or to save
fragments of corrupted files.

	$ xdm99.py work.dsk -s 1
	$ xdm99.py work.dsk -s 0x22 -o first-file-sector
	
For convenience, the sector number may be specified in either decimal or
hexadecimal notation.


Example Usage
-------------

This section gives an example on how to assemble a TI 99 assembly program and
run it on the MESS emulator.  The commands entered and the responses shown here
originate from a Linux system, but they should look very similar on Windows and
Mac OS X machines.

The binary distribution of xdt99 contains an `example` folder with some sample
files that we're going to use.  For the source distribution available on Github
these files are located under the `test` folder.

	$ cd example/
	$ ls -l
	-rw-rw---- 1 ralph ralph  1822 Jan 10 12:51 ascart.asm
	-rw-rw---- 1 ralph ralph   925 Jan 10 12:32 ashello.asm
	-rw-rw---- 1 ralph ralph 92160 Jan 10 12:33 work.dsk
	
The file `ashello.asm` contains a simple assembly program that we want to
assemble and run.  Since the program uses register symbols like `R0` to refer to
registers, we need to specify the `-OR` option for assembly.

	$ xas99.py -OR ashello.asm

This should yield an object code file `ashello.obj` that looks like
this:

	0007EASHELLO A0000B100DB4845B4C4CB4F20B574FB524CB4420B2020B68697F19FF       0001
	A0012B7420B616EB7920B6B65B7921B0300B0000B02E0B8300B04C0B02017F2F9F          0002
	A0028B2A20B0202B0300B0420B0000B0580B0602B16FBB0200B0043B02017F336F          0003
	A003EC0002B0202B001AB0420B0000B0208BFF00B04C9B0300B0002B10007F31FF          0004
	A0054B0300B0000BD809B837CBD809B8374B0420B0000B9220B8375B13F97F2D4F          0005
	A006ABD020B8375B0980B0240B000FB0260B0700B0420B0000B10E87F410F               0006
	50000SLOAD 50000SFIRST5007ESLAST 5001CSTART 30030VSBW  7F28AF               0007
	30046VMBW  3007AVWTR  30062KSCAN 7F827F                                     0008
	:       99/4 AS                                                             0009

This file can be loaded with the Editor/Assembler module using option 3.  But
before we start MESS, we'll also generate an image file for option 5:

	$ xas99.py -OR -i ashello.asm

This time we should get a binary file `ashello.img` of 132 bytes.

	$ ls -l ashello.img
	-rw-rw---- 1 ralph ralph   132 Jan 10 13:11 ashello.img

We now need to transfer these files to a TI disk image so that the TI 99
emulated by MESS can load it.  We'll use the SS/SD disk image `work.dsk` that is
included in the example folder of xdt99 for convenience:

	$ xdm99.py work.dsk -a ashello.obj -n HELLO-O -f DIS/FIX80
	$ xdm99.py work.dsk -a ashello.img -n HELLO-I
	$ xdm99.py work.dsk
	WORK      :     8 used  352 free   90 KB  1S/1D  40 TpS
	----------------------------------------------------------------------------
	HELLO-I        2  PROGRAM        132 B            2015-01-10 13:15:18
	HELLO-O        4  DIS/VAR 80     755 B    9 recs  2015-01-10 13:15:10

We start MESS with our work disk inserted in floppy drive 1:

	$ mess64 ti99_4ae -peb:slot2 32kmem -peb:slot8 hfdc -cart EA.rpk -flop1 work.dsk

You may have to adjust the command for starting MESS based on the location of
your Editor/Assembler cartridge file.  When using a graphical frontend to launch
MESS, use your GUI to select the Editor/Assembler module and the disk image
previously created.

On the TI 99/4A startup screen, we hit any key, then select the Editor/Assembler
module.  We select option 3, `LOAD AND RUN`, then enter the name of the object
code file at the `FILE NAME?` prompt:

	DSK1.HELLO-O

Once the loader finishes, we hit `ENTER` to advance to the `PROGRAM NAME?`
prompt, and type `START` to start the program.  The words "HELLO WORLD" should
appear on screen, and hitting any key will change the color of the screen
border.

When done, we quit the program by hitting `FCTN =`.  Again we select the
Editor/Assembler module, but now we select option 5, `RUN PROGRAM FILE`.  We
enter the name of the image file:

	DSK1.HELLO-I

The program will start automatically once loading has completed.

To run assembly programs without the Editor/Assembler module, we finally
generate our own self-contained cartridge.

First we need to assemble our source code using the `-c` option.

	$ xas99.py -OR -c ascart.asm -n "HELLO CART"

Note that we cannot run the `ashello.asm` program as a cartridge, since we call
`VSBW` and other VDP subroutines, which are unavailable without Editor/Assembler
module and memory expansion.  The `ascart.asm` program thus uses the VDP
registers directly to write to VDP memory.

We don't have to transfer the resulting RPK file to a disk image but can plug
the cartridge directly into the MESS emulator:

	$ mess64 ti99_4ae -cart ascart.rpk

After pressing any key on the TI 99 startup screen you should now see "HELLO
CART" as the second option on the menu screen.  Pressing 2 will run the sample
program.


Feedback and Bug Reports
------------------------

The xdt99 tools are released under the GNU GPL, in the hope that TI 99
enthusiasts may find them useful.

For feedback, bug reports, and feature requests the developer can be reached at
<xdt99@endlos.net>.


[1]: https://endlos99.github.io/xdt99
[2]: https://github.com/endlos99/xdt99/releases
[3]: https://github.com/endlos99/xdt99
[4]: https://www.python.org/downloads/
[5]: http://www.mizapf.de/ti99/tiimagetool.html
[6]: http://www.mrousseau.org/programs/ti99sim/