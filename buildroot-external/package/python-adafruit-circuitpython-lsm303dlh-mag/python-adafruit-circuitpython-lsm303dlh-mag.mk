################################################################################
#
# python-adafruit-circuitpython-lsm303dlh-mag
#
################################################################################

PYTHON_ADAFRUIT_CIRCUITPYTHON_LSM303DLH_MAG_VERSION = 1.1.2
PYTHON_ADAFRUIT_CIRCUITPYTHON_LSM303DLH_MAG_SOURCE = adafruit-circuitpython-lsm303dlh-mag-$(PYTHON_ADAFRUIT_CIRCUITPYTHON_LSM303DLH_MAG_VERSION).tar.gz
PYTHON_ADAFRUIT_CIRCUITPYTHON_LSM303DLH_MAG_SITE = https://files.pythonhosted.org/packages/06/b7/4052a3070066122a11fbfaf86f73748e4c2348478cd9e7fdfd0d60491290
PYTHON_ADAFRUIT_CIRCUITPYTHON_LSM303DLH_MAG_SETUP_TYPE = setuptools
PYTHON_ADAFRUIT_CIRCUITPYTHON_LSM303DLH_MAG_LICENSE = MIT
PYTHON_ADAFRUIT_CIRCUITPYTHON_LSM303DLH_MAG_LICENSE_FILES = LICENSE

$(eval $(python-package))
