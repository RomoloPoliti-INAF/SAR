# SOIM Auto Runner
![Version 0.1.0.devel.2](https://img.shields.io/badge/version-0.1.0.devel.2-blue?style=plastic)
![Language Python 3.12.1](https://img.shields.io/badge/python-3.12.1-orange?style=plastic&logo=python)

## Install

1. clone the repository:

```console
git clone git@github.com:RomoloPoliti-INAF/soimAuto.git
```

2. Install the dependencies

```console 
python3 -m pip install -Ur requirements.txt
```

Now you can run the software

## Usage

The basic usage of the code is 

```console
python3 -m SAR
```


### Kernel Folder Option

- This option allows you to specify the folder where SPICE kernels will be stored. Kernels are often fundamental components in various computational processes.

- Use the short option *-k* or the long option *--kernel*, followed by the desired folder path (replace *FOLDER*).

- Default Value: 'kernels'

- Example:

```console
python -m SAR -k /path/to/kernels
```
- in this example, the script will use the specified folder path for kernels.

### Debug Option

- The debug option is designed to facilitate debugging during script execution.
- Use the short option *-d* or the long option *--debug*  to enable debugging mode. It's a boolean option, so no additional argument is needed.

- Default Value: False
- Example:
```console
python -m SAR -d
```
- By including the *-d* option, the script will run in debug mode, allowing you to gather more detailed information for troubleshooting.

### Verbose Option

- The verbose option enhances the script's output by increasing the verbosity level.
- Use the short option *-v* or the long option *--verbose*. You can use it multiple times to increase verbosity.
- Example:
```console
python -m SAR -vv
```
- In this example, the script's output will be more detailed due to the increased verbosity level.

### Version Option

- This option provides a convenient way to check the version of your script.
- Use the short option *-V* or the long option *--version*.
- Example:

```console
python -m SAR --version
```

### Complete Example

```console
python -m SAR -k /path/to/kernels -d -vv
```
This example sets the kernels folder to "/path/to/kernels," enables debugging mode, and sets verbosity level to the maximum. Adjust the options based on your needs.

 The help documentation for the program, providing information on available options and their usage can be obtained using the option *-h* or *--help*.
