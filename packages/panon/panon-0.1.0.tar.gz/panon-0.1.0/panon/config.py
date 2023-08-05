#!/usr/bin/python
log = 'info'
height = 32
position = 'bottom'
background_color = '#ffffff30'
fake_shadow = True

sections = [
#    {
#        # mpd
#        'auto-command': 'mpc | head -n 1',
#        'interval': 1,
#        'max-width': 20,
#        'click': 'mpc toggle',
#        'scroll-up': 'mpc prev',
#        'scroll-down': 'mpc next',
#    },
    'taskbar',
    'visualizer',
    {
        # volume control
        'icon-name': 'preferences-system-sound',
        'scroll-up': 'pamixer -u;pamixer -i 1;',
        'scroll-down': 'pamixer -u;pamixer -d 1;',
        'click': 'pamixer -t',
    }, {
        # show desktop
        'icon-name': 'desktop',
        'click': """
        if wmctrl -m | grep "mode: ON";then
            wmctrl -k off
        else
            wmctrl -k on
        fi""",
    },
    'multiload',
    {
        # time
        'auto-command': 'date +%T',
        'interval': 1,
    },
]

visualizer_foreground = 'hue_gradient'
# visualizer_foreground =  '#000000a0'
visualizer_background = background_color
visualizer_padding = height / 8
visualizer_decay = 0.01

multiload_interval = 0.5
multiload_layout = 4, 1,
multiload_inner_gap = 2
multiload_outer_gap = 2
multiload_fake_shadow = True
multiload_cpu_background = '#00000010'
multiload_cpu_foreground = '#00ffffff', '#ff00ffff', '#0000ffff', '#00ff00ff',  '#008080ff', '#0080ffff',
multiload_mem_background = multiload_cpu_background
multiload_mem_foreground = '#00ff00ff', '#ff00ffff', '#008080ff', '#0080ffff', '#008000ff', '#008080ff',
multiload_net_background = multiload_cpu_background
multiload_net_foreground = '#008080ff', '#0080ffff', '#008000ff', '#008080ff',
multiload_disk_background = multiload_cpu_background
multiload_disk_foreground = '#008000ff', '#008080ff',

# overwrite default configuration
import os.path

config_file = os.path.expanduser("~/.config/panonrc")
try:
    s = open(config_file).read()
    exec(s)
except BaseException:
    pass
