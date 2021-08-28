import test_bmp
import test_lcd
import test_lsm
import test_sht
import test_tsl
import test_wifi
import test_mic
import test_gps

print('###### test_bmp')
test_bmp.test_all()

print('###### test_lcd')
test_lcd.test_all()

print('###### test_lsm')
test_lsm.test_all()

print('###### test_sht')
test_sht.test_all()

print('###### test_tsl')
test_tsl.test_all()

print('###### skip test_wifi')
# test_wifi.test_all()

print('###### test_mic')
test_mic.test_all()

print('###### test_gps')
test_gps.test_all()
