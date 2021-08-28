# BallometerOS

BallometerOS is the operating system running on ballometer Raspberry Pi 3 B+ devices. It is based on [buildroot](https://github.com/buildroot/buildroot) and supports automatic over-the-air updates inspired by  Android's [A/B system updates approach](https://source.android.com/devices/tech/ota/ab).

https://ballometer.io/

## Overview

A dual partition approach with an active and a passive rootfs allows for atomic updates of the entire operating system including installed programs.

There are four partitions:

 * `mmcblk0p1` boot
 * `mmcblk0p2` rootfs A
 * `mmcblk0p3` rootfs B
 * `mmcblk0p4` data
 
The size of partitions 2 and 3 is at least 4G. 

In the boot filesystem a file called ```select.txt``` determines which rootfs and os boot folder should be used. 
If this file content is 
```
cmdline=cmdline-p2.txt
os_prefix=os-p2/
```
then the system boots into partition `mmcblk0p2` and uses the os files from boot folder `os-p2`. 

If the content of ```select.txt``` is
```
cmdline=cmdline-p3.txt
os_prefix=os-p3/
```
then the system boots into partition `mmcblk0p3` and uses the os files from boot folder `os-p3`.

## Python scripts

The python scripts that do the actual work of reading out the sensors and streaming the measurements to the server are located in [`board/ballometer/rootfs-overlay/root/ballometer`](https://github.com/ballometer/BallometerOS/tree/main/board/ballometer/rootfs-overlay/root/ballometer).

## Build locally

```bash
https://github.com/ballometer/BallometerOS.git
cd BallometerOS
make ballometer_defconfig && make
```

This creates a bootable image in ```output/images/sdcard.img```.

## GitHub Actions Workflow

A GitHub Actions Workflow builds the entire image on every push event, see [here](https://github.com/wipfli/buildroot/actions/workflows/build.yml) for the latest workflow runs. 
This is useful to spot errors in the configuration files and makes builds more reproducible.

A [release workflow](https://github.com/wipfli/buildroot/actions/workflows/release.yml) is triggered when a new tag starting with ```v*``` is pushed to GitHub. 
This workflow puts the version from the git tag into ```board/ballometer/rootfs-overlay/root/release.json```, builds the entire image, and publishes a GitHub release with the following assets:

 * ```rootfs.ext2.xz``` 
 * ```boot.tar.xz```
 * ```sdcard.img.zip```
 * ```sha256_checksums.json```

Running ballometer devices will download and use the ```.xz``` files for updates while the ```.zip``` file is intended for the perparation of new SD cards.

If you have modified the repository and staged some commits, you can create a new release with the following commands:

```bash
git commit -m "something something"
git tag -a v1.1.20 -m "version 1.1.20"
git push --atomic origin main v1.1.20
```

This will trigger the release workflow and produce the release assets automatically. 
For release candidates we use versions ending with ```-rc.<number>```, such as ```v1.1.20-rc.1```. 
A git tag containing ```rc``` leads to a GitHub pre-release.

## Update process

Running ballometer devices download full-system updates from the [GitHub releases](https://github.com/wipfli/buildroot/releases) of this repository. 
Every release has a ```boot.tar.xz``` file which contains the linux kernel, device tree overlays, and raspberry pi bootloader files. 
The rootfs including the programms and python scripts running in user space is contained in the release asset ```rootfs.ext2.xz```. 
This file gets downloaded, extracted, and flashed to the passive partition by the update process.

## Resize ```/data``` partition

Plug the SD card with the full system image into a raspberry pi. Check that the devices appear with
```bash
ls /dev/sda*
# /dev/sda   /dev/sda1  /dev/sda2  /dev/sda3  /dev/sda4
```

Resize the partition with fdisk:

```bash
fdisk /dev/sda
# d (delete)
# 4 (partition 4)
# n (new)
# p (primary)
# w (write)
``` 

Resize filesystem to fill partition:

```bash
resize2fs /dev/sda4
# Resizing the filesystem on /dev/sda4 to 124123132 (1k) blocks.
# The filesystem on /dev/sda4 is now 124123132 (1k) blocks long.
```
