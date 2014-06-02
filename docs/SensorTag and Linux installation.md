How to setup and communicate with the SensorTag from Texas Instruments
======================================================================

The SensorTag from Texas Instruments (TI) is a Bluetooth Low Energy device with six different sensors, two buttons and some LEDs attached. This document describes how to setup and communicate with the different sensors on the SensorTag. The description is based on a PC running Debian Linux (version 7.4.0), but other Linux distributions may probably also be used as well. 
The PC must support Bluetooth 4.0 in dual mode. The school has Bluetooth 4.0 dongles with dual mode support, if your PC does not support Bluetooth 4.0.

Download and install Linux
--------------------------

The Debian Linux distribution can be downloaded and installed from the [Debian homepage](https://www.debian.org).

For easy installation, download the 32/64 bit PC Network Installer and create either a bootable CD/DVD or a bootable USB pendrive. The windows tool UNetBootin is an easy tool to use, to make bootable USB drives from ISO files. [UNetBootin Homepage](http://unetbootin.sourceforge.net)

Updating the BlueZ software
---------------------------
After Linux is installed, the BlueZ software suite has to be updated to the newest version. The BlueZ software suite can be used to communicate with various Bluetooth devices. The reason for updating BlueZ is, that the default BlueZ installation in the Debian ditribution only supports reading from Bluetooth low power devices. But in the project HID, it is necessary also to write commands to the SensorTags which starts reading the different sensors. 
The following guideline is a copy from the [Michael Saunby’s blog](http://mike.saunby.net/2013/04/raspberry-pi-and-ti-cc2541-sensortag.html) about Raspberry Pi and the TI SensorTag, with some additional notes added.

1. Open a Linux terminal.
2. Change directory (cd) into a directory in the home folder (e.g. cd ~/Downloads)
3. Download the latest BlueZ software:
  * `wget https://www.kernel.org/pub/linux/bluetooth/bluez-5.18.tar.gz`
4. Unpack the downloaded the Bluez software: 
  * `tar xvf bluez-5.18.tar.gz`
5. Download the necessary libraries to the Linux system: 
  * `apt-get install libusb-dev libdbus-1-dev libglib2.0-dev automake libudev-dev libical-dev libreadline-dev`
This command has to be executed with root privileges. To obtain root privilege, use the command:
  * su root (then enter the root password)
or
  * sudo (then enter the root password)

6. Download the make project: (root):
  * `apt-get install make`

7. Now it is time to configure and build the downloaded Bluez software. Change directory to the Bluez folder:
  * `cd bluez-5.18`

8. Write the following in the terminal:
  * `./configure --disable-systemd`
  * A lot of text will be outputted to the terminal. This process should only take a few seconds.

9. Make (compile) the BlueZ software by writing (root):
  * `make`
  * The terminal outputs a lot of text describing the different compiling steps, when building the Bluez software. The build process may take a few minutes.

10. Install the BlueZ software by writing the following (root):
  * `make install`

11. The `gatttool` has to be copied manually into the Linux applications: (Root)
  * `cp attrib/gatttool /usr/local/bin/`

12. Rename (or remove) the default Debian `gatttool` by writing the following command: (root)
  * `mv /usr/bin/gatttool /usr/bin/gatttool-old`

In one of the comments in the guideline from the blog, it is noticed that the kernel has to be equal or higher to version 3.5. But the version of the default kernel in Debian version 7.4.0 is 3.2, which seems to work just fine! So don’t begin to update the Linux kernel, unless you find it funny.

Communicating with the SensorTag
--------------------------------
The SensorTag operates as basically as a GATT server, to which a GATT client can write commands and read data. The Linux tool `gatttool` can be used as a tool for read and write operations.

* First find the Bluetooth device handle in the Linux system:
```
   $ hcitool dev

   Devices:
      hci0: 00:02:72:CC:E3:82
      hci1: 00:10:C6:29:FD:4B
```
This computer contains two Bluetooth cards. In this case it is the hci0 handle that is the Bluetooth Low energy card.

* Press the button on the side of the SensorTag, and enter the command below for scanning: (root).
```
   $ hcitool -i hci0 lescan

   LE Scan...
   34:B1:F7:D5:05:FC (unknown)
   34:B1:F7:D5:05:FC SensorTag
```

* The address of the SensorTag is 34:B1:F7:D5:05:FC. Luckily there is only one protocol at the top of Bluetooth Low Energy, called the GATT protocol. The Linux tool `gatttool` implements the GATT protocol, and can be used for communicating with the SensorTag. The `gatttool` has to be executed with root privilege, and in the case below, it is used in interactive mode.
```
   $ gatttool -i hci0 -b 34:B1:F7:D5:05:FC --interactive
   [34:B1:F7:D5:05:FC][LE]>
```
A prompt is returned - connect to the device:
```
   [34:B1:F7:D5:05:FC][LE]> connect
   Attempting to connect to 34:B1:F7:D5:05:FC
   Connection successful
   [34:B1:F7:D5:05:FC][LE]>
```

Read out the temperature and humidity:

```
   [34:B1:F7:D5:05:FC][LE]> char-read-hnd 0x3C
   Characteristic value/descriptor 00 00 00 00
   [34:B1:F7:D5:05:FC][LE]>
```

The 0x3C is a "handle" - or address in the SensorTag, the `gatttool` can read. But before the SensorTag can start measuring the temperature / humidity, a command has to be written to the handle 0x38 to setup the sensor measuring.

```
   [34:B1:F7:D5:05:FC][LE]> char-write-cmd 0x38 01
   [34:B1:F7:D5:05:FC][LE]> char-read-hnd 0x3C
   Characteristic value/descriptor 85 69 7B 36 
   [34:B1:F7:D5:05:FC][LE]>
```

The output from the temperature / humidity sensor is in a raw format, which has to be converted into Celsius and humidity by a mathematical formal (which can be found in the datasheet for the temperature sensor). 

__Example calculation__
_Temperature:_
Temp = -45.86 + 176.72 / 65536 * 0x6985 = 25.58 grader

_Humidity:_
Read = 0x367B & ~0x0003; // Clear the last two bits
Hum = -6.0 + 125.0 / 65536 * Read = 54.16% 

* Disconnecting the device:
```
   [34:B1:F7:D5:05:FC][LE]> disconnect
```

* Exit `gatttool`
```
   [34:B1:F7:D5:05:FC][LE]> exit
```

SensorTag Links
-----------------------
The official BlueZ homepage: [link](http://www.bluez.org "BlueZ Homepage")

The official SensorTag webpage from Texas instruments: [link](http://www.ti.com/ww/en/wireless_connectivity/sensortag/index.shtml?INTC=SensorTag&HQS=sensortag "TI SensorTag")

Michael Saunbys blog about Raspberry Pi, Python and SensorTag: [link](http://mike.saunby.net/2013/04/raspberry-pi-and-ti-cc2541-sensortag.html "Blog about Raspberry pi, python and SensorTag")

Joost Yervante Damad blog about SensorTag experiments [link](http://joost.damad.be/2013/08/experiments-with-bluetooth-low-energy.html "Blog about SensorTag experiments")

Page about unboxing and how to get started with the SensorTag [link](http://www.cnx-software.com/2013/07/21/texas-instruments-sensortag-unboxing-getting-started-with-bluetooth-low-energy-in-linux-with-a-raspberry-pi/ "Unboxing the SensorTag")

Article about the SensorTag hardware [link](http://makezine.com/2013/04/18/teardown-of-the-ti-sensortag/ "Article about the SensorTag hardware")

Pretty cool webpage about programming and controlling the different sensors in the SensorTag. The examples are written in techBASIS, but the examples is understandable [link](http://www.byteworks.us/Byte_Works/SensorTag.html ")

