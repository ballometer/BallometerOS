import ballometer

lcd = ballometer.LCD()
buttons = ballometer.Buttons()

fn, params = ballometer.menu.startup({
    'lcd': lcd,
    'buttons': buttons,
    'metar_done': False,
})

while True:
    fn, params = fn(params)
