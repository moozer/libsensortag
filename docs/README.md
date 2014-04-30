How to setup and communicate with the SensorTag from Texas Instruments
======================================================================

The SensorTag from Texas Instruments (TI) is a Bluetooth Low Energy device with six different sensors, two buttons and some LEDs attached. This document describes how to setup and communicate with the different sensors on the SensorTag. The description is based on a PC running Debian Linux (version 7.4.0), but other Linux distributions may probably also be used as well. 
The PC must support Bluetooth 4.0 in dual mode. The school has Bluetooth 4.0 dongles with dual mode support, if your PC does not support Bluetooth 4.0.

Download and install Linux
--------------------------

The Debian Linux distribution can be downloaded and installed from the Debian homepage. [Debian homepage](https://www.debian.org)

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

10. 10.	Install the BlueZ software by writing the following (root):
  * `make install`

11. the `gatttool` has to be copied manually into the Linux applications: (Root)
  * `cp attrib/gatttool /usr/local/bin/`

12: Rename (or remove) the default Debian `gatttool` by writing the following command: (root)
  * `mv /usr/bin/gatttool /usr/bin/gatttool-old`

In one of the comments in the guideline from the blog, it is noticed that the kernel has to be equal or higher to version 3.5. But the version of the default kernel in Debian version 7.4.0 is 3.2, which seems to work just fine! So don’t begin to update the Linux kernel, unless you find it funny.

Communicating with the SensorTag
--------------------------------
The SensorTag operates as basically as a GATT server, to which a GATT client can write commands and read data. The Linux tool `gatttool` can be used as a tool for read and write operations.


