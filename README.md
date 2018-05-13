# Crom

A C/C++ project builder with simple declarative syntax.

[![Build Status](https://travis-ci.org/mropert/crom.svg?branch=master)](https://travis-ci.org/mropert/crom)

**This project is still in early development stage and more of a proof of concept than a real solution.**
**Should you be interested in using it, please contact me first.**

## Setup

Install through `pip` (once uploaded...):

```
pip install crom
```

## Requirements

Crom requires Python (either 2 or 3) and uses the following tools behind the scenes:
* Conan C/C++ package manager 1.2.0 or later (available through `pip`)
* CMake 3.2 or later

## Usage

### Start a new project

```
crom bootstrap lib MyLib
```

### Configure and install dependencies (if needed) then build project

```
mkdir build
cd build
crom build ..
```

### Reconfigure and install dependencies without building

```
cd build
crom configure ..
```

### Opt-out of crom

```
crom opt-out
```

### Build description

All contained under `build.yml`:

```yaml
name: MyLib
type: lib
sources:
- src/muf.cpp
headers:
- include/muf/muf.hpp
tests:
- test/muf_test.cpp
```

## License

Crom is published under the [MIT License](LICENSE.md)
