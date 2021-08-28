################################################################################
#
# python-adafruit-circuitpython-register
#
################################################################################

PYTHON_ADAFRUIT_CIRCUITPYTHON_REGISTER_VERSION = 1.9.0
PYTHON_ADAFRUIT_CIRCUITPYTHON_REGISTER_SOURCE = adafruit-circuitpython-register-$(PYTHON_ADAFRUIT_CIRCUITPYTHON_REGISTER_VERSION).tar.gz
PYTHON_ADAFRUIT_CIRCUITPYTHON_REGISTER_SITE = https://files.pythonhosted.org/packages/92/26/4f2b4733e210d528d0c2f560aa0e1d4905eb064c90900576e0f9d724df5b
PYTHON_ADAFRUIT_CIRCUITPYTHON_REGISTER_SETUP_TYPE = setuptools
PYTHON_ADAFRUIT_CIRCUITPYTHON_REGISTER_LICENSE = MIT
PYTHON_ADAFRUIT_CIRCUITPYTHON_REGISTER_LICENSE_FILES = LICENSE

$(eval $(python-package))
