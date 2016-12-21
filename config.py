import os

from platform import python_version

from libqtile import layout, bar, widget
from libqtile.command import lazy
from libqtile.config import Key, Screen, Group, Drag, Click

alt = 'mod1'
mod = 'mod4'
ctrl = 'control'
shift = 'shift'

terminal = 'urxvt'
editor = os.getenv('EDITOR', 'vi')
editor_cmd = '{term} -e {ed}'.format(term=terminal, ed=editor)
webbrowser = 'firefox'
mail = (
    '{term} -e tmux -2 new -s mail '
    'tmux source-file /home/tony/.config/tmux/mail-session.conf'
).format(term=terminal)
new_term = '{term} -e tmux -2'.format(term=terminal)

keys = [
    # Switch between windows in current stack pane
    # FIXME What is this?
    Key([mod], 'k',
        lazy.layout.down()),
    Key([mod, shift], 'j',
        lazy.layout.up()),

    # Move windows up or down in current stack
    # FIXME What is this?
    Key([mod, ctrl], 'k',
        lazy.layout.shuffle_down()),
    Key([mod, ctrl], 'j',
        lazy.layout.shuffle_up()),

    # Switch window focus to other pane(s) of stack
    Key([alt], 'Tab',
        lazy.layout.next()),

    # Swap panes of split stack
    Key([alt, shift], 'Tab',
        lazy.layout.rotate()),

    # Switch active screen
    Key([mod], 'Tab',
        lazy.next_screen()),

    # Switch layouts
    Key([mod], 'space',
        lazy.next_layout()),

    # Restart/Shutdown/Close
    Key([mod, ctrl], 'r',
        lazy.restart()),
    Key([mod, shift], 'q',
        lazy.shutdown()),
    Key([mod, shift], 'c',
        lazy.window.kill()),

    # Apps launcher
    Key([mod], 'r',
        lazy.spawncmd()),

    # Apps shortcuts
    Key([mod], 'Return',
        lazy.spawn(new_term)),
    Key([], 'XF86Mail',
        lazy.spawn(mail)),

]

autostart = {'term': new_term, 'net': webbrowser}
groups = [Group(i, spawn=autostart.get(i)) for i in ['term', 'net', 'mail']]

for i, group in enumerate(groups, 1):
    grp = group.name
    key = 'F%d' % i
    keys.append(Key([mod], key,
                    lazy.group[grp].toscreen()))
    keys.append(Key([mod, shift], key,
                    lazy.window.togroup(grp)))

layouts = [
    layout.Max(),
    layout.Matrix(margin=20),
]

widget_defaults = dict(
    font='Inconsolata',
    fontsize=12,
    padding=2,
)

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(highlight_method='text'),
                widget.Prompt(),
                widget.Spacer(),
                widget.TextBox("Vol."),
                widget.Volume(),
            ],
            24,
        ),
    ),
    Screen(
        top=bar.Bar(
            [
                widget.Clock(format='%b %-d, %a %H:%M'),
                widget.Spacer(),
                widget.MemoryGraph(frequency=10),
                widget.CPUGraph(frequency=10),
                widget.ThermalSensor(update_interval=60, threshold=60),
            ],
            24,
        ),
    ),
]
screens.reverse()  # I don't know why screens are not in the right order

mouse = [
    Drag([mod], 'Button1',
         lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], 'Button3',
         lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], 'Button2',
          lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_wrap = False
floating_layout = layout.Floating()
auto_fullscreen = True

wmname = 'Qtile (Python %s)' % python_version()
