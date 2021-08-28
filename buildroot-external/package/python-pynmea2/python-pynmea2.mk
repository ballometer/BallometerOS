################################################################################
#
# python-pynmea2
#
################################################################################

PYTHON_PYNMEA2_VERSION = 1.15.0
PYTHON_PYNMEA2_SOURCE = pynmea2-$(PYTHON_PYNMEA2_VERSION).tar.gz
PYTHON_PYNMEA2_SITE = https://files.pythonhosted.org/packages/ca/6b/5009ac42b1f21fee5b68151e5536b03dc6ca5e5346a23fc943860680d91b
PYTHON_PYNMEA2_SETUP_TYPE = setuptools
PYTHON_PYNMEA2_LICENSE = MIT
PYTHON_PYNMEA2_LICENSE_FILES = LICENSE

$(eval $(python-package))
