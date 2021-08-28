################################################################################
#
# python-adafruit-circuitpython-tsl2591
#
################################################################################

PYTHON_ADAFRUIT_CIRCUITPYTHON_TSL2591_VERSION = 1.2.3
PYTHON_ADAFRUIT_CIRCUITPYTHON_TSL2591_SOURCE = adafruit-circuitpython-tsl2591-$(PYTHON_ADAFRUIT_CIRCUITPYTHON_TSL2591_VERSION).tar.gz
PYTHON_ADAFRUIT_CIRCUITPYTHON_TSL2591_SITE = https://files.pythonhosted.org/packages/79/93/c2c89c6cd67e89777ad96b2ad15adfbb229fb555033e0392e8a150ec9254
PYTHON_ADAFRUIT_CIRCUITPYTHON_TSL2591_SETUP_TYPE = setuptools
PYTHON_ADAFRUIT_CIRCUITPYTHON_TSL2591_LICENSE = MIT
PYTHON_ADAFRUIT_CIRCUITPYTHON_TSL2591_LICENSE_FILES = LICENSE

$(eval $(python-package))
