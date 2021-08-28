################################################################################
#
# python-adafruit-blinka
#
################################################################################

PYTHON_ADAFRUIT_BLINKA_VERSION = 5.2.3
PYTHON_ADAFRUIT_BLINKA_SOURCE = Adafruit-Blinka-$(PYTHON_ADAFRUIT_BLINKA_VERSION).tar.gz
PYTHON_ADAFRUIT_BLINKA_SITE = https://files.pythonhosted.org/packages/c4/08/ee9ccfe844a934214acac307135a6a2bcd3c8d2167d2075ee1f536031bbd
PYTHON_ADAFRUIT_BLINKA_SETUP_TYPE = setuptools
PYTHON_ADAFRUIT_BLINKA_LICENSE = MIT
PYTHON_ADAFRUIT_BLINKA_LICENSE_FILES = LICENSE

# Since the binary file adafruit_blinka/microcontroller/bcm283x/pulseio/libgpiod_pulsein
# is 32 bit but the architecture is 64 bit we turn of architecture consitency checking
PYTHON_ADAFRUIT_BLINKA_BIN_ARCH_EXCLUDE = /usr/lib/python3.8/site-packages/adafruit_blinka

define PYTHON_ADAFRUIT_BLINKA_PRE_PATCH_FIXUP
	echo "patch adafruit blinka to support software i2c on ports 24, 23"
	cp $(PYTHON_ADAFRUIT_BLINKA_PKGDIR)/pin.py $(O)/build/python-adafruit-blinka-5.2.3/src/adafruit_blinka/microcontroller/bcm283x/pin.py
endef

PYTHON_ADAFRUIT_BLINKA_PRE_PATCH_HOOKS += PYTHON_ADAFRUIT_BLINKA_PRE_PATCH_FIXUP

$(eval $(python-package))
