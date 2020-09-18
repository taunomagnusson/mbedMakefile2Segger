# mbedMakefile2Segger
Converts an ARM Mbed OS Makefile Project into a Segger Embedded Studio Project.

This allows you to use Segger Embedded Studio to Develop/Edit/Compile/Debug your ARM Mbed OS projects.

It has been tested with:
ARM MBed OS 6.2 and 6.3
Segger Embedded Studio 5.10

The converter is written in Python, and verified with Python 3.8.x (but should work for other versions out-of-the-box).

Both the Makefile and the Segger emProject files are simple text files, so it's quite easy and straightforward to do the conversion.
Segger Embedded Studio is also a very nice lightweight IDE - I'm a bit surprised that Mbed doesn't support exporting to Segger by default.

# Prerequisites for Example

Installed on your development computer:
- Python (https://www.python.org/downloads/) (If you have no preference, pick Python 3.8.x)
- MBED CLI Command line tools (https://os.mbed.com/docs/mbed-os/v6.3/quick-start/build-with-mbed-cli.html)
- GNU ARM Embedded Toolchain Compiler (https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads)
- Segger Embedded Studio (https://www.segger.com/downloads/embedded-studio)

- For this example, we are using a NUCLEO-F303K8 board. You'll need to adjust in Step 1 below according to your target board.

# Example

1: Create the Makefile based Mbed OS Project
- In your bash/cmd/powershell, do:
- mbed new segger-helloworld
- cd segger-helloworld
- mbed update mbed-os-6.3.0
- mbed export -i make_gcc_arm -m NUCLEO_F303K8

2: Install and execute the make2segger.py converter script
- Download (directly from GitHub or using git) and Copy the "make2segger.py" and "main.cpp" files into the newly created "segger-helloworld" directory.
- Open the "make2segger.py" script in a texteditor and update "gnu_toolchain_directory" to point to the "bin" directory of your installed GNU ARM Embedded toolchain.
- Run "python3 make2segger.py". Review the statistics, did you have any "Failure" in the statistics?
- WARNING: You will currently see 2 Failures (for Include Directories) in the statistics. You can ignore these Failures.
- Failures can be fixed manually. Edit "make2segger.py" and set "DEBUG = True". This will dump out the any linenumbers in the Makefile that failed to parse. Check the Makefile text on that line number, it might be easy to manually add it later in Segger Embedded Studio. Or update the make2segger.py script.
- You should now have a newly created Segger .emProject file

3: Open and compile the project in Segger Embedded Studio
- Open the newly created "segger-helloworld.emProject" in Segger Embedded Studio
- Manually add the "main.cpp" file to the project by right clicking on the Project and choosing "Add Existing File"
- Build the Project and you should be presented with a compiled binary (.elf), which can be downloaded onto your embedded board and will blink a LED.
- WARNING: There is currently an open issue the first time you build. You will get an error from the linker. Just "Build" again and it should work (see below in Open Issues)

# Open Issues, Caveats, Workarounds
- The make2segger.py script statistics currently shows 2 Failures (For Include Directories). You can ignore these Failures.
- There is currently an issue the first time you build: The Linker will give you a "cannot open linker script file $(RelLinkerScriptPath): No such file or directory" Error. Just "Build" one more time and it will work.
- There is  no "Build/Clean" command generated. To clean the project, you can manually delete the "Output" directory (or a "rm -rf" command in the Segger Embedded Studio options for the Project). Note that you MUST create a new Output/Debug/Exe directory for the linker to work (mkdir Output; mkdir Output/Debug; mkdir Output/Debug/Exe)
- If you get Pre-Link Command Error "opening output file Output/Debug/Exe/segger-helloworld.link_script.ld: No such file or directory" you probably forgot to create the Output/Debug/Exe directory before trying to build.
- If you get Linker Error "mbed_boot_gcc_arm.o/undefined reference to main" you forgot to manually add the "main.cpp" file in Segger Embedded Studio (See Step #3 above)
