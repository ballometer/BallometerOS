.PHONY: prepare all clean

all: prepare
	cd build && make -j4 -s

prepare:
	make -C buildroot O=../build/ BR2_EXTERNAL=../buildroot-external/ ballometer_defconfig

clean:
	rm -rf build
