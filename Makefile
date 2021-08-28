.PHONY: prepare all clean

all: prepare
	cd output && make -j4 -s

prepare:
	make -C buildroot O=../output/ BR2_EXTERNAL=../buildroot-external/ ballometer_defconfig

clean:
	rm -rf output
