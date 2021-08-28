################################################################################
#
# python-uvicorn
#
################################################################################

PYTHON_UVICORN_VERSION = 0.12.1
PYTHON_UVICORN_SOURCE = uvicorn-$(PYTHON_UVICORN_VERSION).tar.gz
PYTHON_UVICORN_SITE = https://files.pythonhosted.org/packages/cb/9e/ea8abc0c638f6e1d551c4e2e8e90bef4616bc73ccf060cb025ec166dba8f
PYTHON_UVICORN_SETUP_TYPE = setuptools
PYTHON_UVICORN_LICENSE = BSD

$(eval $(python-package))
