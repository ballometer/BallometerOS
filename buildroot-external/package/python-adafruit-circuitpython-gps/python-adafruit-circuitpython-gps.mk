################################################################################
#
# python-adafruit-circuitpython-gps
#
################################################################################

PYTHON_ADAFRUIT_CIRCUITPYTHON_GPS_VERSION = 3.6.5
PYTHON_ADAFRUIT_CIRCUITPYTHON_GPS_SOURCE = adafruit-circuitpython-gps-$(PYTHON_ADAFRUIT_CIRCUITPYTHON_GPS_VERSION).tar.gz
PYTHON_ADAFRUIT_CIRCUITPYTHON_GPS_SITE = https://files.pythonhosted.org/packages/dc/d9/f6c08a74d8212d440dcd116cb377a80dde63f8047fcf5eedd103e49a2981
PYTHON_ADAFRUIT_CIRCUITPYTHON_GPS_SETUP_TYPE = setuptools
PYTHON_ADAFRUIT_CIRCUITPYTHON_GPS_LICENSE = MIT
PYTHON_ADAFRUIT_CIRCUITPYTHON_GPS_LICENSE_FILES = LICENSE

$(eval $(python-package))
