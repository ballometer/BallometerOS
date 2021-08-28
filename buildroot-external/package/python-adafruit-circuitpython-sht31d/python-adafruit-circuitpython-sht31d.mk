################################################################################
#
# python-adafruit-circuitpython-sht31d
#
################################################################################

PYTHON_ADAFRUIT_CIRCUITPYTHON_SHT31D_VERSION = 2.3.2
PYTHON_ADAFRUIT_CIRCUITPYTHON_SHT31D_SOURCE = adafruit-circuitpython-sht31d-$(PYTHON_ADAFRUIT_CIRCUITPYTHON_SHT31D_VERSION).tar.gz
PYTHON_ADAFRUIT_CIRCUITPYTHON_SHT31D_SITE = https://files.pythonhosted.org/packages/4c/c9/ce6481729df6896e211cb68320ef5cf23b7541ab2db2679a4a93e6e8c1e6
PYTHON_ADAFRUIT_CIRCUITPYTHON_SHT31D_SETUP_TYPE = setuptools
PYTHON_ADAFRUIT_CIRCUITPYTHON_SHT31D_LICENSE = MIT
PYTHON_ADAFRUIT_CIRCUITPYTHON_SHT31D_LICENSE_FILES = LICENSE

$(eval $(python-package))
