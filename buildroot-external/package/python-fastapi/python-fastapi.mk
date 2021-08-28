################################################################################
#
# python-fastapi
#
################################################################################

PYTHON_FASTAPI_VERSION = 0.61.1
PYTHON_FASTAPI_SOURCE = fastapi-$(PYTHON_FASTAPI_VERSION).tar.gz
PYTHON_FASTAPI_SITE = https://files.pythonhosted.org/packages/da/32/ea2b86e56674ff3d1bb0bbb2e3b74a04694ac0be3331e9f9d431c350bcc2
PYTHON_FASTAPI_SETUP_TYPE = distutils
PYTHON_FASTAPI_LICENSE = MIT
PYTHON_FASTAPI_LICENSE_FILES = LICENSE

$(eval $(python-package))
