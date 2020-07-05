# File to C-style array converter
Python script for converting any file to C/C++-style array source code file.

For example, for device firmware is required binary image that will store inside finally hex file. 

And file index.html
```html
<html>
    <body>
        <p>This is a very simple HTML document</p>
    </body>
</html>
```
will converted to output.h
```c++
// File: index.html 
const uint8_t index_html[] = {
    0x3c, 0x68, 0x74, 0x6d, 0x6c, 0x3e, 0x0a, 0x20, 
    0x20, 0x20, 0x20, 0x3c, 0x62, 0x6f, 0x64, 0x79, 
    0x3e, 0x0a, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 
    0x20, 0x20, 0x3c, 0x70, 0x3e, 0x54, 0x68, 0x69, 
    0x73, 0x20, 0x69, 0x73, 0x20, 0x61, 0x20, 0x76, 
    0x65, 0x72, 0x79, 0x20, 0x73, 0x69, 0x6d, 0x70, 
    0x6c, 0x65, 0x20, 0x48, 0x54, 0x4d, 0x4c, 0x20, 
    0x64, 0x6f, 0x63, 0x75, 0x6d, 0x65, 0x6e, 0x74, 
    0x3c, 0x2f, 0x70, 0x3e, 0x0a, 0x20, 0x20, 0x20, 
    0x20, 0x3c, 0x2f, 0x62, 0x6f, 0x64, 0x79, 0x3e, 
    0x0a, 0x3c, 0x2f, 0x68, 0x74, 0x6d, 0x6c, 0x3e
};
```

# Requirements
Python >=3.6

## How to use
**NOTE:** Linux users should add executable permission to python script before using.

```Bash
chmod +x file2array.py
```

### Options

`file2array.py -f input_file_name -a -o output_file_name -t "const uint8_t" -offset 44`

`-f input_file_name` - specifies file name will convert

`-o output_file_name` - specifies output file name

`-a` - data will be appended to the output file

`-t "const uint8_t"` - specifies arrays data type (same type for each input file), by default, type is `const unsigned char`. 

**Note:** Use quotes if data type consist of several words.

`-offset 44` - specifies input file data offset in input file, e.g.: raw data in the wav file starts from 44'th byte. Use integer or hex value.  

### Usage examples

#### Convert one file
Linux
```bash
./file2array.py -f index.html -o files.h -t "const uint8_t"
```
Windows
```bash
py file2array.py -f index.html -o files.h -t "const uint8_t"
```

#### Convert several files to one output file
Linux
```bash
./file2array.py -f index.html -o files.h -t "const uint8_t"
./file2array.py -f dorbell.wav -a -o files.h -t "const uint8_t" -offset 44
```
Windows
```bash
py file2array.py -f index.html -o files.h -t "const uint8_t"
py file2array.py -f dorbell.wav -a -o files.h -t "const uint8_t" -offset 44
```

#### Convert several files to several output files
Linux
```bash
./file2array.py -f index.html -o index.h -t "const uint8_t"
./file2array.py -f dorbell.wav -o dorbell.h -t "const uint8_t" -offset 44
```
Windows
```bash
py file2array.py -f index.html -o index.h -t "const uint8_t"
py file2array.py -f dorbell.wav -o dorbell.h -t "const uint8_t" -offset 44
```

#### Including to source code
```c
#include "index.h"      // include insert index_html array source code to this place
#include "dorbell.h"    // include insert dorbell_wav array source code to this place

...
memcpy(buf, index_h, 100);
...
set_pwm_value(dorbell_h[i++]);
...
```

### Limitations
For script simplicity, input file loads to RAM after that a new data image created in RAM. By calculation, 1 bytes of input file required about 8 RAM bytes. 

In most cases, convertible files have small size and limited by microcontrollers memory size that why RAM size limitation doesn't matter. 