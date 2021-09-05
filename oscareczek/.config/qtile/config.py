from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
import os
import subprocess

from Xlib import display

alt = 'mod1'
win = 'mod4'

home = os.environ.get('HOME')

d = display.Display()
s = d.screen()
r = s.root
res = r.xrandr_get_screen_resources()._data
num_screens = 0
for output in res['outputs']:
    mon = d.xrandr_get_output_info(output, res['config_timestamp'])._data
    if mon['num_preferred']:
        num_screens += 1

# -----KEYBINDS------
keys = [
    # MonadTall Bindings
    Key([win], 'h', lazy.layout.left()),
    Key([win], 'l', lazy.layout.right()),
    Key([win], 'j', lazy.layout.down()),
    Key([win], 'k', lazy.layout.up()),
    Key([win], 'space', lazy.layout.next()),
    Key([win, 'shift'], 'h', lazy.layout.swap_left()),
    Key([win, 'shift'], 'l', lazy.layout.swap_right()),
    Key([win, 'shift'], 'j', lazy.layout.shuffle_down()),
    Key([win, 'shift'], 'k', lazy.layout.shuffle_up()),
    Key([win, 'shift'], 'plus', lazy.layout.grow()),
    Key([win, 'shift'], 'minus', lazy.layout.shrink()),
    Key([win, 'shift'], 'n', lazy.layout.reset()),
    Key([win, 'shift'], 'm', lazy.layout.maximize()),
    Key([win, 'shift'], 'space', lazy.layout.flip()),

    # Toggle between different layouts
    Key([win], 'Tab', lazy.next_layout()),

    # Floating Layout Keybinds
    Key([win], 't', lazy.window.enable_floating()),
    Key([win, 'shift'], 't', lazy.window.disable_floating()),

    # Window controls (layout agnostic)
    Key([win], 'w', lazy.window.kill()),
    Key([win, 'control'], 'r', lazy.restart()),
    Key([win, 'control'], 'q', lazy.shutdown()),
    Key([win], 'r', lazy.spawncmd('Run')),
    Key([win, 'shift'], 'r', lazy.spawn('xfce4-appfinder')),
    Key([win, 'control'], 'l', lazy.spawn(os.path.join(home, 'bin', 'lock_screen.sh'))),  # lock the screen
    Key([win, 'control'], 'x', lazy.spawn(os.path.join(home, 'bin', 'dmenu_session_manager'))),

    # Audio Controls
    Key([], 'XF86AudioRaiseVolume', lazy.spawn('pactl set-sink-volume @DEFAULT_SINK@ +5%')),
    Key([], 'XF86AudioLowerVolume', lazy.spawn('pactl set-sink-volume @DEFAULT_SINK@ -5%')),
    Key([], 'XF86AudioMute', lazy.spawn('pactl set-sink-mute @DEFAULT_SINK@ toggle')),

    # Screen brightness
    Key([], 'XF86MonBrightnessUp',   lazy.spawn('light -A 10')),
    Key([], 'XF86MonBrightnessDown', lazy.spawn('light -U 10')),

    # Programs
    Key([win], 'Return', lazy.spawn('sakura')),
    Key([win], 'b', lazy.spawn('firefox')),
    Key([win], 'c', lazy.spawn('sakura -x python')),
    Key([win], 'e', lazy.spawn('Thunar')),

    # Screenshots
    Key([], 'Print', lazy.spawn('xfce4-screenshooter -f')),
    Key([alt], 'Print', lazy.spawn('xfce4-screenshooter -w')),
    Key(['control'], 'Print', lazy.spawn('xfce4-screenshooter -r'))
]

# on T540p, I use Win+E or folder icon as Print
if os.uname()[1] == 'nozomi':
    keys[-4] = Key([win], 'l', lazy.spawn('sakura'))
    for i in range(-3, 0):
        keys[i].modifiers.append(win)
        keys[i].key = 'e'

groups = [Group(i) for i in '12345678']

for i in groups:
    keys.extend([
        # win1 + letter of group = switch to group
        Key([win], i.name, lazy.group[i.name].toscreen()),

        # win1 + shift + letter of group = switch to & move focused window to group
        Key([win, 'shift'], i.name, lazy.window.togroup(i.name)),
    ])

layouts = [
    layout.MonadTall(align='MonadTail._right', border_width=1, border_focus='#008000'),
    layout.Max(),
    layout.TreeTab(),
]


@hook.subscribe.startup_once
def autostart():
    path = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.run(path)


widget_defaults = dict(
    font='Conduit Pro',
    fontsize=14,
    padding=2,
)
extension_defaults = widget_defaults.copy()

widgets = [
        widget.GroupBox(inactive='#a9a9a9', active='#f3f4f5'),
        widget.Prompt(foreground='#00d2ff'),
        widget.WindowName(font='Conduit Pro Bold'),
        widget.Wttr(format='1', location={'Ballerup': 'Ballerup'}, json=False),
        widget.Sep(),
        widget.Net(interface='eth0'),  # 5
        widget.Sep(),
        widget.CPUGraph(border_color='#c0c5ce',  fill_color='#6790eb', graph_color='#6790eb', border_width=1,
                        line_width=1, type='box'),  # 7
        widget.Sep(linewidth=0, padding=5),
        widget.TextBox('🌡️', foreground='#bc5a03', padding=0),
        widget.ThermalSensor(foreground_alert='#cd1f3f', padding=3, threshold=80),
        widget.Sep(),
        widget.Memory(update_interval=5),
        widget.Sep(padding=10),
        widget.CurrentLayoutIcon(),  # 14
        widget.Sep(padding=10),  # 15
        widget.Systray(),  # 16
        widget.PulseVolume(emoji=True, limit_max_volume=True, step=5),
        widget.Clock(format='%a %Y-%m-%d %R'),
]

if num_screens > 1:  # If on desktop pc with dual screens
    screens = [Screen(top=bar.Bar(widgets, 24, background='#400000'))]
    for _ in range(num_screens):
        screens.append(Screen(top=bar.Bar([widget.GroupBox(inactive='#a9a9a9'), widgets[1],
                                           widget.WindowName(font='Conduit Pro Bold')] + widgets[3:14] +
                                          [widget.CurrentLayoutIcon()] + widgets[17:], 24, background='#400000')))
else:  # If on laptop
    widgets[5] = widget.Net(format='{down} ↓↑ {up}')
    widgets[7] = widget.CPU(format='{load_percent}% ({freq_current}GHz)')
    widgets.insert(17, widget.BatteryIcon())
    screens = [Screen(top=bar.Bar(widgets, 24, background='#400000'))]

# Drag floating layouts.
mouse = [
    Drag([win], 'Button1', lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([win], 'Button3', lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([win], 'Button2', lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = 'smart'


@hook.subscribe.client_new
def set_floating(window):
    window_name = window.window.get_name()
    floating_windows = ['GitKraken', 'Steam', 'gnome-calculator', 'Elite Dangerous Launcher', 'Discord Updater']
    if window_name and (window_name in floating_windows or window_name.startswith('Open Database - ')):
        window.floating = True


@hook.subscribe.client_new
def floating_dialogs(window):
    dialog = window.window.get_wm_type() == 'dialog'
    transient = window.window.get_wm_transient_for()
    if dialog or transient:
        window.floating = True


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = 'LG3D'
