#!/bin/sh

set -u
set -e

rm -rf ${O}/images/os-p2
mkdir ${O}/images/os-p2
cp ${O}/images/bcm2710-rpi-3-b-plus.dtb ${O}/images/os-p2/bcm2710-rpi-3-b-plus.dtb
cp -R ${O}/images/rpi-firmware/overlays ${O}/images/os-p2/overlays
touch ${O}/images/os-p2/overlays/README
cp ${O}/images/zImage ${O}/images/os-p2/zImage

cp ${BR2_EXTERNAL_BALLOMETER_PATH}/board/ballometer/boot/cmdline-p2.txt ${O}/images/os-p2/cmdline-p2.txt
cp ${BR2_EXTERNAL_BALLOMETER_PATH}/board/ballometer/boot/cmdline-p3.txt ${O}/images/os-p2/cmdline-p3.txt
cp ${BR2_EXTERNAL_BALLOMETER_PATH}/board/ballometer/boot/config.txt ${O}/images/config.txt
cp ${BR2_EXTERNAL_BALLOMETER_PATH}/board/ballometer/boot/select.txt ${O}/images/select.txt

rm -f ${O}/images/data.ext4 ${O}/images/data.ext2
${O}/host/sbin/mkfs.ext4 -d ${BR2_EXTERNAL_BALLOMETER_PATH}/board/ballometer/data -r 1 -N 0 -m 5 -L "data" -O ^64bit ${O}/images/data.ext2 "100M"
ln -sf data.ext2 ${O}/images/data.ext4
