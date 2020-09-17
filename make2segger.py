import os;
import sys;
import glob;
import time;

# General Settings

gnu_toolchain_directory = "C:\\Program Files (x86)\\GNU Tools Arm Embedded\\9 2019-q4-major\\bin";

# Debug Settings

DEBUG = False
VERBOSE = False

# BEGIN HELPER FUNCTIONS

def dmsg(s):
    if DEBUG:
        print(s)



# BEGIN PARSER SECTION

print("=======> PARSING Makefile")
linesSuccess = [];
linesFailed  = [];

# Find Projectname
ifd = open('Makefile');
sys.stdout.write ("Looking for PROJECT Name:                  ");
lineno = 1;
for line in ifd:
	lsp = line.split(" ");
	if lsp[0] == "PROJECT":
		projectname = lsp[2].rstrip();
		linesSuccess.append(lineno);
		break;
	lineno = lineno + 1;
print("\t[Found]  Line: " + str(lineno) + ", Name: \"" + projectname );

# Parse and identify SourceCode Files (.c .cpp .s)
ifd = open('Makefile')
sys.stdout.write ("Looking for Source files (.c .cpp .s)    ");
lineno  = 1;
failed  = 0;
sourceFiles = [];
for line in ifd:
	lsp = line.split(" ");
	if lsp[0] == "OBJECTS":
		objfile = lsp[2].rstrip();
		dmsg(str(lineno) + ":Found objfile on line " + str(lineno) + ": \"" + objfile + "\"");
		sfile = objfile[2:-2];
		if( os.path.exists(sfile + ".c") ):
			sourcefile = sfile + ".c";
		elif( os.path.exists(sfile + ".cpp") ):
			sourcefile = sfile + ".cpp";
		elif( os.path.exists(sfile + ".s") ):
			sourcefile = sfile + ".s";
		elif( os.path.exists(sfile + ".S") ):
			sourcefile = sfile + ".S";
		else:
			failed = failed + 1;
			linesFailed.append(lineno);
			dmsg(str(lineno) + " ERROR: Could not find source file for object file: " + objfile);
			break;
		dmsg(str(lineno) + ": Found sourcefile matching .o file: " + sourcefile);
		linesSuccess.append(lineno);
		sourceFiles.append(sourcefile);
	lineno = lineno + 1;
print("\t[Found]  Success: " + str(len(sourceFiles)) + " Failed: " + str(failed) );


# Parse and identify Include Directories
ifd = open('Makefile')
sys.stdout.write("Looking for Include directories             ");
includes = "";
lineno = 1;
failed  = 0;
includeDirs = [];
for line in ifd:
	lsp = line.split(" ");
	if lsp[0] == "INCLUDE_PATHS":
		idir = lsp[2].rstrip();
		if( idir[0:7] == "-I.././"):
			incdir = idir[7:];
			dmsg(str(lineno) + ": Found include directory : \"" + incdir + "\"");
			linesSuccess.append(lineno);
			includeDirs.append(incdir);
		elif( idir[0:8] == "-I../C:/"):
			incdir = idir[5:];
			dmsg(str(lineno) + ": Absolute path include directory: " + incdir);
			# Need to convert this to a relative path. Just ignore for now.
			failed += 1;
			linesFailed.append(lineno);
		else:
			dmsg(str(lineno) + ": UNPARSEABLE directory: ");
			failed += 1;
			linesFailed.append(lineno);
			# Do nothing for now, just ignore it
	lineno = lineno + 1;
print("\t[Found]  Success: " + str(len(includeDirs)) + " Failed: " + str(failed) );

# Find Linker Script file (?.ld)
ifd = open('Makefile')
sys.stdout.write("Looking for Linker Script                   ");
lineno = 1;
for line in ifd:
	lsp = line.split(" ");
	if lsp[0] == "LINKER_SCRIPT":
		linker_script1 = lsp[2][5:].rstrip();
		linesSuccess.append(lineno);
		break;
	lineno = lineno + 1;
print("\t[Found]  Line: " + str(lineno));

# Find PREPROC directives
ifd = open('Makefile')
sys.stdout.write("Looking for PREPROC directives             ");
lineno = 1;
for line in ifd:
	lsp = line.split(" ");
	if lsp[0] == "PREPROC":
		preproc = line.split("PREPROC = ")[1].rstrip();
		linesSuccess.append(lineno);
		break;
	lineno = lineno + 1;
print("\t[Found]  Line: " + str(lineno) );

# Find C_FLAGS
ifd = open('Makefile')
sys.stdout.write("Looking for C_FLAGS                        ");
c_flags = "";
lineno  = 1;
success = 0;
failed  = 0;
for line in ifd:
	lsp = line.split(" ");
	if lsp[0] == "C_FLAGS":
		c_flag = lsp[2].rstrip();
		c_flags += " " + c_flag;
		dmsg(str(lineno) + ": Found C_FLAG: " + c_flag);
		success += 1;
		linesSuccess.append(lineno);
	lineno = lineno + 1;
print("\t[Found]  Success: " + str(success) + " Failed: " + str(failed) );

# Find CXX_FLAGS
ifd = open('Makefile')
sys.stdout.write("Looking for CXX_FLAGS                      ");
cxx_flags = "";
lineno  = 1;
success = 0;
failed  = 0;
for line in ifd:
	lsp = line.split(" ");
	if lsp[0] == "CXX_FLAGS":
		cxx_flag = lsp[2].rstrip();
		cxx_flags += " " + cxx_flag;
		dmsg(str(lineno) + ": Found CXX_FLAG: " + cxx_flag);
		success += 1;
		linesSuccess.append(lineno);
	lineno = lineno + 1;
print("\t[Found]  Success: " + str(success) + " Failed: " + str(failed) );

# Find ASM_FLAGS
ifd = open('Makefile')
sys.stdout.write("Looking for ASM_FLAGS                      ");
asm_flags = "";
lineno  = 1;
success = 0;
failed  = 0;
for line in ifd:
	lsp = line.split(" ");
	if lsp[0] == "ASM_FLAGS":
		asm_flag = lsp[2].rstrip();
		if asm_flag.startswith("-I"):
			asm_flag = asm_flag.replace('\\', '/');
			if(asm_flag.startswith("-I..")):
				asm_flags += " -I" + asm_flag[5:];
			else:
				asm_flags += " " + asm_flag;
		if asm_flag.startswith(".\\mbed_config.h"):
			asm_flags += asm_flag.replace('\\', '/');
		else:
			asm_flags += " " + asm_flag;
		success += 1;
		linesSuccess.append(lineno);
	lineno = lineno + 1;
print("\t[Found]  Success: " + str(success) + " Failed: " + str(failed) );

ifd = open('Makefile')
sys.stdout.write("Looking for LDFLAGS                        ");
lineno = 1;
for line in ifd:
	lsp = line.split(":=");
	if lsp[0].rstrip() == "LD_FLAGS":
		ld_flags = lsp[1].rstrip();
		linesSuccess.append(lineno);
		break;
	lineno = lineno + 1;
print("\t[Found]  Line: " + str(lineno) );

ifd = open('Makefile')
sys.stdout.write("Looking for LD_SYS_LIBS                    ");
lineno = 1;
for line in ifd:
	lsp = line.split(":=");
	if lsp[0].rstrip() == "LD_SYS_LIBS":
		ld_sys_libs = lsp[1].rstrip();
		linesSuccess.append(lineno);
		break;
	lineno = lineno + 1;
print("\t[Found]  Line: " + str(lineno) );

# Scan all include directories for .h files and add them to a file list
includeFiles = [];
for dir in includeDirs:
	includeFiles += glob.glob(dir + "/*.h");

# First, print a summary of what we have parsed
print("\n=======> SUMMARY (PARSED)")
print("Projectname   : " + projectname);
print("Toolchain PATH: " + gnu_toolchain_directory);
print("Source Files  : " + str(len(sourceFiles)));
print("Include Dirs  : " + str(len(includeDirs)));
print("Include Files : " + str(len(includeFiles)));
print("LINKER_SCRIPT1: " + linker_script1);
print("PREPROC       : " + preproc);
print("LD_SYS_LIBS   : " + ld_sys_libs);
if VERBOSE:
	print("\nLD_FLAGS      : " + ld_flags);
	print("\nC_FLAGS       : " + c_flags);
	print("\nCXX_FLAGS     : " + cxx_flags);
	print("\nASM_FLAGS     : " + asm_flags);

# Generate XML-style directory and file tags (structure)
xmlFiles = "";
allFiles = sourceFiles + includeFiles;
allFiles.sort();
indent = 6;
cwd = [];
for file in allFiles:
	parts = file.split("/");
	filename = parts.pop();
	maxi = min(len(cwd), len(parts));
	i = 0;
	while( (i < maxi) and (cwd[i] == parts[i]) ):
		i = i + 1;
	nwd = parts[0:i];


	# If needed, decrease folder depth and add closing tags
	n = len(cwd);
	while(len(nwd) < n):
		indent = indent - 2;
		xmlFiles += ' '*indent + "</folder>\n";
		n = n - 1;

	# If needed, increase folder depth and add start tags (i.e. new directories)
	m = len(nwd);
	while(m < len(parts)):
		xmlFiles += ' '*indent + "<folder Name=\"" + parts[m] + "\">\n";
		m = m + 1;
		indent = indent + 2;

	# We are now in the 'right' folder level
	cwd = parts;
	xmlFiles += ' '*indent + "<file file_name=\"" + file + "\" />\n";
# If needed, decrease folder depth and add closing tags
n = len(cwd);
while(0 < n):
	indent = indent - 2;
	xmlFiles += ' '*indent + "</folder>\n";
	n = n - 1;

if VERBOSE:
	print("\n=======> SUMMARY (UNPARSED)")
	ifd = open('Makefile')
	lines = ifd.read().split('\n');
	print("\nFailed Lines: ", len(linesFailed));
	for lineno in linesFailed:
		print(str(lineno) + ": " + lines[lineno-1]);

	parsedLines = linesSuccess + linesFailed;
	allLines = range(0, len(lines))
	unparsedLines = [x for x in allLines if x not in parsedLines]
	print("\nUnparsed Lines: ", len(unparsedLines));
	for lineno in unparsedLines:
		print(str(lineno) + ": " + lines[lineno-1]);

# Build XML emProject Text
xml  = "<!DOCTYPE CrossStudio_Project_File>\n";
xml += "<solution Name=" + "\"" + projectname + "\"" + " target=\"8\" version=\"2\">\n";
xml += "  <project Name=" + "\"" + projectname + "\">\n";
xml += """\
    <configuration
      Name="Common"
      arm_architecture="v7EM"
      arm_core_type="Cortex-M4"
      arm_endian="Little"
      arm_fpu_type="FPv4-SP-D16"
      arm_simulator_memory_simulation_parameter="RX 08000000,00010000,FFFFFFFF;RWX 20000000,00004000,CDCDCDCD"
      arm_target_device_name="STM32F303K8"
      arm_target_interface_type="SWD"
      debug_start_from_entry_point_symbol="No"
      debug_target_connection="J-Link"
      linker_section_placements_segments="FLASH1 RX 0x08000000 0x00010000;RAM1 RWX 0x20000000 0x00004000"
      project_directory=""
      project_type="Externally Built Executable" />
""";
xml += "    <folder Name=\"Source\">\n";
xml += "    <file file_name=\"mbed_config.h\" />\n";
xml += xmlFiles;
xml += "    </folder>\n";
xml += "  </project>\n";
xml += "  <configuration\n";
xml += "    Name=\"Debug\"\n";
xml += "    build_toolchain_directory=\"" + gnu_toolchain_directory + "\"\n";
xml += "    asm_additional_options=\"" + asm_flags + "\"\n";
xml += "    c_additional_options=\"\"\n";
xml += "    c_only_additional_options=\"" + c_flags + "\"\n";
xml += "    c_preprocessor_definitions=\"DEBUG\"\n";
xml += "    c_user_include_directories=\".;" + ';'.join(map(str,includeDirs)) + "\"\n";
xml += "    cpp_only_additional_options=\"" + cxx_flags + "\"\n";
xml += "    external_assemble_command=\"&quot;$(ToolChainDir)/arm-none-eabi-gcc&quot; $(AsmOptions) &quot;$(RelInputPath)&quot; -o &quot;$(RelTargetPath)&quot;\"\n";
xml += "    external_c_compile_command=\"&quot;$(ToolChainDir)/arm-none-eabi-gcc&quot; $(COnlyOptions) $(Includes) &quot;$(RelInputPath)&quot; -o &quot;$(RelTargetPath)&quot;\"\n";
xml += "	external_cpp_compile_command=\"&quot;$(ToolChainDir)/arm-none-eabi-g++&quot; $(CppOnlyOptions) $(Includes) &quot;$(RelInputPath)&quot; -o &quot;$(RelTargetPath)&quot;\"\n";
xml += "	external_cpp_link_command=\"&quot;$(ToolChainDir)/arm-none-eabi-gcc&quot; $(LinkOptions) -T &quot;$(RelLinkerScriptPath)&quot; --output &quot;$(RelTargetPath)&quot; @$(ObjectsFilePath)\"\n";
xml += "    external_objects_file_name=\"$(OutDir)/.link_options.txt\"\n";
#xml += "    link_linker_script_file=\"" + linker_script + "\"\n";
xml += "    link_linker_script_file=\"$(OutDir)/mbednew-makefile.link_script.ld\"\n";
xml += "    link_use_linker_script_file=\"Yes\"\n";
xml += "    linker_additional_options=\"" + ld_flags + " " + ld_sys_libs + "\"\n";
xml += "    linker_pre_build_command=\"" + "&quot;$(ToolChainDir)&quot;/" + preproc + linker_script1 + "-o $(OutDir)/" + projectname + ".link_script.ld" + "\"\n";
xml += """\
    external_build_command=""
    external_clean_command=""
    external_link_command=""
    gcc_debugging_level="Level 3"
    gcc_optimization_level="None"
""";

xml += " />\n";
xml += "</solution>\n";



xmlFilename = projectname + ".emProject";
if os.path.exists(xmlFilename):
	os.system("mv " + xmlFilename + " " + xmlFilename + "_" + str(time.strftime("%y%j%H%M%S", time.gmtime())));
f = open(xmlFilename, "w");
f.write(xml);
f.close();
