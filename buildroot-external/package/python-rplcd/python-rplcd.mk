################################################################################
#
# python-rplcd
#
################################################################################

PYTHON_RPLCD_VERSION = 1.3.0
PYTHON_RPLCD_SOURCE = RPLCD-$(PYTHON_RPLCD_VERSION).tar.gz
PYTHON_RPLCD_SITE = https://files.pythonhosted.org/packages/c2/79/cd1689e41cd65d587ce9db6dcac8c081b37faa8de91c45028e960b400d42
PYTHON_RPLCD_SETUP_TYPE = setuptools
PYTHON_RPLCD_LICENSE = MIT
PYTHON_RPLCD_LICENSE_FILES = LICENSE

$(eval $(python-package))
