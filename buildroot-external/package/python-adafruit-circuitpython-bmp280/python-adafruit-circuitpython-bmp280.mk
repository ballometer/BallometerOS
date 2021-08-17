################################################################################
#
# python-adafruit-circuitpython-bmp280
#
################################################################################

PYTHON_ADAFRUIT_CIRCUITPYTHON_BMP280_VERSION = 3.2.3
PYTHON_ADAFRUIT_CIRCUITPYTHON_BMP280_SOURCE = adafruit-circuitpython-bmp280-$(PYTHON_ADAFRUIT_CIRCUITPYTHON_BMP280_VERSION).tar.gz
PYTHON_ADAFRUIT_CIRCUITPYTHON_BMP280_SITE = https://files.pythonhosted.org/packages/06/ae/7304db1ca6d2aa2566486d1f48865e9405c6353e4aa56328dcc5355634ad
PYTHON_ADAFRUIT_CIRCUITPYTHON_BMP280_SETUP_TYPE = setuptools
PYTHON_ADAFRUIT_CIRCUITPYTHON_BMP280_LICENSE = MIT
PYTHON_ADAFRUIT_CIRCUITPYTHON_BMP280_LICENSE_FILES = LICENSE

$(eval $(python-package))
