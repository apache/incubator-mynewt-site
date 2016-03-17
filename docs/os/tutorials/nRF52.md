## Blinky on nRF52 board

### Objective

Download a generic firmware skeleton ("bootstrap image") that applies to any hardware and then throw in additional applicable pkgs to generate a build for a specific board, namely the
nRF52 Series chip from Nordic Semiconductors.

#### Hardware needed

* nRF52 Development Kit
* Laptop running Mac OS
* It is assumed you have already installed newt tool. 
* It is assumed you already installed native tools as described [here](../get_started/native_tools.md)

#### install jlinkEXE

In order to be able to communicate with the SEGGER J-Link debugger on the dev board, you have to download and install the J-Link GDB Server software on to your laptop. You may download the "Software and documentation pack for Mac OS X" from [https://www.segger.com/jlink-software.html](https://www.segger.com/jlink-software.html). 

#### Create a project.  

Create a new project to hold your work.  For a deeper understanding, you can read about project creation in 
[Get Started -- Creating Your First Project](../get_started/project_create.md)
or just follow the commands below.

```no-highlight
    $ mkdir ~/dev
    $ cd ~/dev
    $ newt new myproj
    Downloading project skeleton from apache/incubator-mynewt-blinky...
    Installing skeleton in myproj...
    Project myproj successfully created.

    $ cd myproj

    $ newt install -v 
    apache-mynewt-core
    Downloading repository description for apache-mynewt-core... success!
    ...
    apache-mynewt-core successfully installed version 0.7.9-none
``` 

#### Create the target

Create a single target for the nrf52.  NOTE: The nrf52 mynewt core does not
yet have bootloader support, so we will create a single image to download
to the device.

```no-highlight
$ newt target create blink_nordic
$ newt target set blink_nordic app=apps/blinky
$ newt target set blink_nordic bsp=@apache-mynewt-core/hw/bsp/nrf52pdk
$ newt target set blink_nordic build_profile=debug
$ newt target show 
targets/blink_nordic
    app=apps/blinky
    bsp=@apache-mynewt-core/hw/bsp/nrf52pdk
    build_profile=debug
```

#### Build the image 

```no-highlight
$ newt build blink_nordic
...
Compiling main.c
Archiving blinky.a
Linking blinky.elf
App successfully built: ~/dev/myproj/bin/blink_nordic/apps/blinky/blinky.elf
```

#### Connect the board

Connect the evaluation board via micro-USB to your PC via USB cable.
        
#### Download to the target

Download the executable to the target platform.

```no-highlight
$ newt -v load blink_nordic
```

#### Congratulations

You have created, setup, compiled, loaded, and ran your first mynewt application
for the nrf52 evaluation board.






