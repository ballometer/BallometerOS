################################################################################
#
# python-starlette
#
################################################################################

PYTHON_STARLETTE_VERSION = 0.13.8
PYTHON_STARLETTE_SOURCE = starlette-$(PYTHON_STARLETTE_VERSION).tar.gz
PYTHON_STARLETTE_SITE = https://files.pythonhosted.org/packages/86/f5/2713195e0d2f449554f3e0b749cc9d8ec5d00035279d6dfa02d4410adcbd
PYTHON_STARLETTE_SETUP_TYPE = setuptools
PYTHON_STARLETTE_LICENSE = BSD

$(eval $(python-package))
