################################################################################
#
# InfluxDB
#
################################################################################

INFLUXDB_VERSION = 1.8.2
INFLUXDB_SOURCE = influxdb-$(INFLUXDB_VERSION)_linux_armhf.tar.gz
INFLUXDB_SITE = https://dl.influxdata.com/influxdb/releases
INFLUXDB_LICENSE = MIT

define INFLUXDB_INSTALL_TARGET_CMDS
	$(INSTALL) -D -m 0755 $(@D)/influxdb-$(INFLUXDB_VERSION)-1/usr/bin/influxd $(TARGET_DIR)/usr/bin/influxd
	$(INSTALL) -D -m 0644 $(@D)/influxdb-$(INFLUXDB_VERSION)-1/etc/influxdb/influxdb.conf $(TARGET_DIR)/etc/influxdb/influxdb.conf
endef

$(eval $(generic-package))