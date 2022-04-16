from libqtile import bar, extension, hook, layout, qtile, widget
from libqtile.config import Group, Key, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import os
import subprocess

mod = 'mod4'
terminal = guess_terminal()
num_screens = 0

if qtile.core.name == 'x11':
    from Xlib import display

    d = display.Display()
    s = d.screen()
    r = s.root
    res = r.xrandr_get_screen_resources()._data
    for output in res['outputs']:
        mon = d.xrandr_get_output_info(output, res['config_timestamp'])._data
        if mon['num_preferred']:
            num_screens += 1
else:
    num_screens = 1


keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),

    # Floating Layout Keybinds
    Key([mod], 't', lazy.window.enable_floating()),
    Key([mod, 'shift'], 't', lazy.window.disable_floating()),

    # Audio Controls
    Key([], 'XF86AudioRaiseVolume', lazy.spawn('amixer set Master 5%+')),
    Key([], 'XF86AudioLowerVolume', lazy.spawn('pactl set-sink-volume @DEFAULT_SINK@ -5%')),
    Key([], 'XF86AudioMute', lazy.spawn('pactl set-sink-mute @DEFAULT_SINK@ toggle')),
    Key([], 'XF86AudioMicMute', lazy.spawn('pactl set-source-mute @DEFAULT_SOURCE@ toggle')),

    # Brightness Controls
    Key([], 'XF86MonBrightnessUp', lazy.spawn('light -T 1.667')),
    Key([], 'XF86MonBrightnessDown', lazy.spawn('light -T 0.6')),

    # Programs
    Key([mod], 'b', lazy.spawn('firefox')),
    Key([mod], 'c', lazy.spawn(terminal + ' -x python')),
    Key([mod], 'e', lazy.spawn('Thunar')),

    # Screenshots
    Key([], 'Print', lazy.spawn('xfce4-screenshooter -f')),
    Key(['mod1'], 'Print', lazy.spawn('xfce4-screenshooter -w')),
    Key(['control'], 'Print', lazy.spawn('xfce4-screenshooter -r')),
]

# on T540p, I use Win+E or folder icon as Print
if os.uname()[1] == 'nozomi':
    keys[-4] = Key([mod], 'l', lazy.spawn(terminal))
    for i in range(-3, 0):
        keys[i].modifiers.append(mod)
        keys[i].key = 'e'

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            desc="Move focused window to group {}".format(i.name)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
        #     desc="move focused window to group {}".format(i.name)),
    ])

layouts = [
    layout.MonadTall(align='MonadTail._right', border_width=1, border_focus='008000'),
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
        widget.GroupBox(inactive='aaaaaa', margin=2,
                        disable_drag=True, highlight_method='block'),
        widget.Prompt(foreground='00c0c0'),
        widget.WindowName(font='Conduit Pro Bold'),
        widget.Wttr(format='1', location={'Ballerup': 'Ballerup'}),
        widget.Sep(),
        widget.Net(interface='eth0'),  # 5
        widget.Sep(),
        widget.CPUGraph(border_color='c0c5ce', fill_color='6790eb', graph_color='6790eb',
                        border_width=1, line_width=1, type='box'),  # 7
        widget.Spacer(5),
        widget.TextBox('🌡️', padding=0),
        widget.ThermalSensor(padding=3, threshold=80),
        widget.Sep(),
        widget.Memory(update_interval=5),
        widget.Sep(padding=10),
        widget.CurrentLayoutIcon(),  # 14
        widget.Sep(padding=10),  # 15
        widget.Systray(),  # 16
        widget.Volume(emoji=True, step=5),
        widget.Clock(format='%a %F %R'),
]

if num_screens > 1:  # If on desktop pc with dual screens
    screens = [Screen(top=bar.Bar(widgets, 24, background='400000'))]
    for _ in range(num_screens):
        screens.append(
            Screen(
                top=bar.Bar(
                    [widget.GroupBox(inactive='aaaaaa', margin=2,
                                     disable_drag=True, highlight_method='block'), widgets[1],
                     widget.WindowName(font='Conduit Pro Bold')] + widgets[3:14] +
                    [widget.CurrentLayoutIcon()] + widgets[17:], 24, background='400000')))
else:  # If on laptop
    widgets[5] = widget.Net(format='{down} ↓↑ {up}')
    widgets[7] = widget.CPU(format='{load_percent}% ({freq_current}GHz)')
    widgets.insert(17, widget.BatteryIcon(theme_path='/usr/share/icons/Yaru++-Dark/status/16'))
    screens = [Screen(top=bar.Bar(widgets, 24, background='400000'))]

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
wmname = 'CWM'
os.environ['QT_QPA_PLATFORMTHEME'] = 'qt5ct'
