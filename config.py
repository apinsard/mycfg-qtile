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
editor = os.getenv('EDITOR', 'nano')
editor_cmd = '%s -e %s' % (terminal, editor)
hostname = os.uname()[1]


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
        lazy.spawn(terminal)),
]

groups = [Group(i) for i in "12345"]

for i in range(len(groups)):
    grp = groups[i].name
    keys.append(Key([mod], 'F%d' % (i+1),
                lazy.group[grp].toscreen()))
    keys.append(Key([mod, shift], 'F%d' % (i+1),
                lazy.window.togroup(grp)))

layouts = [
    layout.Max(),
    layout.Stack(num_stacks=2)
]

widget_defaults = dict(
    font='Arial',
    fontsize=12,
    padding=2,
)

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
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
                widget.Sep(),
                widget.Prompt(),
                widget.WindowName(),
            ],
            24,
        ),
    ),
]

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
