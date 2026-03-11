# Luanti Engine Development

## C++ Debugging
These steps are only needed for debug builds.

GUI:
* Try the "Scope" Geany plugin (`geany-plugins-scope`) which is a "Graphical GDB frontend".

CLI (Command-Line Interface):
* build minetest with --debug option
* cd to minetest/bin directory
* type (you must put ./ before minetest to ensure that gdb will use your
  debug build instead of a version in your system path):
  `gdb ./minetest`
* After the symbols finish loading, complete the following within gdb:
  `run`
  * If the program terminates, gdb will tell you what debug symbol
    packages are needed for your distro.
  * When you are done debugging, type:
    quit
* Try debugging again after the proper packages are installed.

### minetest build speeds

#### 0.4 ~200527
* Intel i7-4770K
  * libraries ~3m
  * program ~4m

### Regression Tests
* Use of input in python, where should never be used except in
  poikilos.py (some/all of that may be moved to parsing.py in
  <https://github.com/Poikilos/pycodetool>) and minetestinfo.py for
  first-time setup or when `interactive_enable` is `True`

## [Deprecated setup file]
(See https://github.com/Hierosoft/hierosoft launcher instead)
Further steps needed to recreate setup file:
* extract entire zip
* run postinstall.bat
* change version number in %USERPROFILE%\Documents\GitHub\Enliven\winclient\install ENLIVEN.iss
* change version number in %USERPROFILE%\Documents\GitHub\Enliven\winclient\launcher-src\ENLIVEN.pro
