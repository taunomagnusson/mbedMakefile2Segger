# mbedMakefile2Segger
Converts an ARM Mbed OS Makefile Project into a Segger Embedded Studio Project.

This allows you to use Segger Embedded Studio to Develop/Edit/Compile/Debug your ARM Mbed OS projects.

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
- Small Failures are usually easy to fix manually. Edit "make2segger.py" and set "DEBUG = True". This will dump out the any linenumbers in the Makefile that failed to parse. Check the Makefile text on that line number, it might be easy to manually add it later in Segger Embedded Studio.
- You should now have a newly created Segger .emProject file

3: Open and compile the project in Segger Embedded Studio
- Open the newly created "segger-helloworld.emProject" in Segger Embedded Studio
- Manually add the "main.cpp" file to the project by right clicking on the Project and choosing "Add Existing File"
- Build the Project and you should be presented with a compiled binary (.elf), which can be downloaded onto your embedded board and will blink a LED.
