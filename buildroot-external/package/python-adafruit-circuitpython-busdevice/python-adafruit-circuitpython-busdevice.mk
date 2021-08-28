################################################################################
#
# python-adafruit-circuitpython-busdevice
#
################################################################################

PYTHON_ADAFRUIT_CIRCUITPYTHON_BUSDEVICE_VERSION = 5.0.1
PYTHON_ADAFRUIT_CIRCUITPYTHON_BUSDEVICE_SOURCE = adafruit-circuitpython-busdevice-$(PYTHON_ADAFRUIT_CIRCUITPYTHON_BUSDEVICE_VERSION).tar.gz
PYTHON_ADAFRUIT_CIRCUITPYTHON_BUSDEVICE_SITE = https://files.pythonhosted.org/packages/1e/87/4257d665ee58c413c3b22174992c34c490a20155c4eebad5cd75e0837a44
PYTHON_ADAFRUIT_CIRCUITPYTHON_BUSDEVICE_SETUP_TYPE = setuptools
PYTHON_ADAFRUIT_CIRCUITPYTHON_BUSDEVICE_LICENSE = MIT
PYTHON_ADAFRUIT_CIRCUITPYTHON_BUSDEVICE_LICENSE_FILES = LICENSE

$(eval $(python-package))
