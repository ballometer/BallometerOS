################################################################################
#
# python-h11
#
################################################################################

PYTHON_H11_VERSION = 0.11.0
PYTHON_H11_SOURCE = h11-$(PYTHON_H11_VERSION).tar.gz
PYTHON_H11_SITE = https://files.pythonhosted.org/packages/22/01/01dc716e71eeead6c6329a19028548ac4a5c2a769a130722548c63479038
PYTHON_H11_SETUP_TYPE = setuptools
PYTHON_H11_LICENSE = MIT
PYTHON_H11_LICENSE_FILES = LICENSE.txt

$(eval $(python-package))
