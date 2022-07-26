import os
import re
import socket
import subprocess
from typing import List  # noqa: F401
from libqtile import layout, bar, widget, hook, qtile
from libqtile.config import Group, Key, Match, Screen, Rule
from libqtile.config import EzClick as Click, EzDrag as Drag
from libqtile.command import lazy
from libqtile.widget import Spacer

#mod4 or mod = super key
#don't bind things to [mod, mod1], crashes qtile
mod = "mod4"
mod1 = "alt"
mod2 = "control"
home = os.path.expanduser('~')

win_list = []
def toggle_stick_win(qtile):
    global win_list
    if qtile.current_window in win_list:
        win_list.remove(qtile.current_window)
    else:
        win_list.append(qtile.current_window)
def unstick_win(qtile): #used to kill sticky window
    global win_list
    win_list.remove(qtile.current_window)

@hook.subscribe.setgroup
def move_win():
    for w in win_list:
        w.togroup(qtile.current_group.name)
        # qtile.current_group.focus_back() #testing
        subprocess.Popen("qtile cmd-obj -o group -f prev_window", shell=True) # I want qtile to not focus on the sticky window by default, but couldn't find a better way to call this funciton, so this is some hacky shit.

@lazy.function
def float_to_front(qtile):
    for window in qtile.current_group.windows:
        if window.floating:
            window.cmd_bring_to_front()

@lazy.function
def move_floating(qtile, direction):
    if qtile.current_window.floating:
        if direction == "up":
            qtile.current_window.cmd_move_floating(0, -90)
        elif direction == "down":
            qtile.current_window.cmd_move_floating(0, 90)
        elif direction == "left":
            qtile.current_window.cmd_move_floating(-100, 0)
        elif direction == "right":
            qtile.current_window.cmd_move_floating(100, 0)

@lazy.function
def resize_floating(qtile, mod):
    if qtile.current_window.floating:
        if mod == "grow":
            qtile.current_window.cmd_resize_floating(100, 100)
        elif mod == "shrink":
            qtile.current_window.cmd_resize_floating(-100, -100)

@lazy.function
def switch_workspace(qtile, group_name):
    if group_name == qtile.current_screen.group.name:
        return qtile.current_screen.set_group(qtile.current_screen.previous_group)
    for i, group in enumerate(qtile.groups):
        if group_name == group.name:
            return qtile.current_screen.set_group(qtile.groups[i])

myTerm = "alacritty" # My terminal of choice

#STARTKEYS
keys = [

# Custom function keys
    Key([mod], "y", lazy.function(toggle_stick_win), desc="Toggle Sticky Window"),
    Key([mod, mod2], "d", resize_floating("grow"), desc="Grow Floating Window"),
    Key([mod, mod2], "a", resize_floating("shrink"), desc="Shrink Floating Window"),
    Key([mod, "shift"], "d", move_floating("right"), desc="Move Floating Window Right"),
    Key([mod, "shift"], "a", move_floating("left"), desc="Move Floating Window Left"),
    Key([mod, "shift"], "s", move_floating("down"), desc="Move Floating Window Down"),
    Key([mod, "shift"], "w", move_floating("up"), desc="Move Floating Window Up"),

# KEYBINDS
    Key([mod], "period", lazy.spawn(home +'/.config/misc/dm-opendot.sh'), desc='Dmenu Dotfiles Opener'),
    Key([mod], "g", lazy.spawn('google-chrome-stable --enable-features=VaapiVideoDecoder,VaapiVideoEncoder --disable-features=UseChromeOSDirectVideoDecoder --gtk-version=4'), desc='Launch Google Chrome'),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc='Toggle Window Fullscreen'),
    Key([mod], "q", lazy.function(unstick_win), lazy.window.kill(), desc='Kill Current Window'),
    Key([mod], "e", lazy.spawn(home + '/.config/emacs-launch.sh'), desc='Launch Emacs Client'),
    Key([mod], "Return", lazy.spawn(myTerm), desc='Launch Terminal'),
    Key([mod], "t", lazy.spawn('thunar'), desc='Launch File Manager'),
    Key([mod], "m", lazy.spawn('env GDK_SCALE=2 steam'), desc='Launch Steam'),
    Key([mod], "o", lazy.spawn(home + '/.config/misc/dm-logout.sh'), desc='Logout Menu'),
    Key([mod], "p", lazy.spawn(home + '/.config/misc/togglepicom.sh'), desc='Toggle Picom Transparency'),
    Key([mod], "slash", lazy.spawn(home + "/.config/misc/dm-scriptlauncher.sh"), desc='Dmenu Misc Script Launcher'),
    Key([mod], "i", lazy.spawn('clipmenu -i -l 15 -p "Choose Clipboard:"'), desc='Dmenu Clipboard'),

# ALACRITTY KEYBINDS
    Key([mod], "c", lazy.spawn(myTerm + ' --class calc,calc -e calc'), desc='Launch Calculator'),
    Key([mod], "n", lazy.spawn(myTerm + ' --class ranger,ranger -e ranger'), desc='Launch Ranger'),
    Key([mod], "b", lazy.spawn(myTerm + ' --class sysmon,sysmon -e btop'), desc='Launch System Monitor'),
    Key([mod], "r", lazy.spawn(home + "/.config/misc/dm-frecency"), desc='Program Launcher'),
    Key([mod], "u", lazy.spawn(myTerm + " -e " + home + "/.config/qtile/scripts/nmtui.sh"), desc='Connect to Wifi'), #fixes nmtui resizing issue

# SUPER + SHIFT KEYS
    Key([mod, "shift"], "r", lazy.restart(), desc='Restart Qtile'),
    Key([mod, "control"], "r", lazy.restart(), desc='Restart Qtile'),

# CONTROL + ALT KEYS

    # Key(["mod1", "control"], "u", lazy.spawn('pavucontrol')),
    Key(["mod1", "control"], "l", lazy.spawn('slock'), desc='Lock the Screen'),

# SCREENSHOTS

    Key([], "Print", lazy.spawn('flameshot full -p ' + home + '/Pictures'), desc='Capture Current Screen'),
    Key([mod2], "Print", lazy.spawn('flameshot gui'), desc='Capture Part of Screen'),

# INCREASE/DECREASE BRIGHTNESS
    Key([], "XF86MonBrightnessUp", lazy.spawn(home + "/.config/qtile/scripts/extbright.sh up")),
    Key([], "XF86MonBrightnessDown", lazy.spawn(home + "/.config/qtile/scripts/extbright.sh down")),

# INCREASE/DECREASE/MUTE VOLUME
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle"), lazy.spawn(home + "/.config/qtile/scripts/currentvolume.sh")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -D pulse set Master 5%-"), lazy.spawn(home + "/.config/qtile/scripts/currentvolume.sh")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -D pulse set Master 5%+"), lazy.spawn(home + "/.config/qtile/scripts/currentvolume.sh")),

    Key([mod], "F8", lazy.spawn("playerctl previous"), desc='Play Previous'),
    Key([mod], "F9", lazy.spawn("playerctl play-pause"), desc='Toggle Playback  '),
    Key([mod], "F10", lazy.spawn("playerctl next"), desc='Play Next'),

    Key([mod], "F11", lazy.spawn("amixer -D pulse set Master 5%-"), lazy.spawn(home + "/.config/qtile/scripts/currentvolume.sh"), desc='Volume Down'),
    Key([mod], "F12", lazy.spawn("amixer -D pulse set Master 5%+"), lazy.spawn(home + "/.config/qtile/scripts/currentvolume.sh"), desc='Volume Up'),

    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
    Key([], "XF86AudioStop", lazy.spawn("playerctl stop")),

# QTILE LAYOUT KEYS
    Key([mod, "shift"], "n", lazy.layout.normalize(), desc='Normalize Layout'),
    Key([mod], "space", lazy.next_layout(), desc='Toggle Next Layout'),

# I only use Monadtall/wide layout and max layout 99% of the time, so this keybindings reflect that.
    Key([mod], "k", lazy.group.next_window(), float_to_front, desc='Focus Next Window'),
    Key([mod], "j", lazy.group.prev_window(), float_to_front, desc='Focus Previous Window'),
    Key([mod], "l", lazy.layout.grow_main(), desc='Increase Master Size'),
    Key([mod], "h", lazy.layout.shrink_main(), desc='Decrease Master Size'),

    Key([mod], "Down", lazy.group.next_window(), float_to_front, desc='Focus Next Window'),
    Key([mod], "Up", lazy.group.prev_window(), float_to_front, desc='Focus Previous Window'),
    Key([mod], "Right", lazy.layout.grow_main(), desc='Increase Master Size'),
    Key([mod], "Left", lazy.layout.shrink_main(), desc='Decrease Master Size'),

# This is for faster one handed operation
    Key([mod], "d", lazy.group.next_window(), float_to_front, desc='Focus Next Window'),
    Key([mod], "a", lazy.group.prev_window(), float_to_front, desc='Focus Previous Window'),

# FLIP LAYOUT FOR MONADTALL/MONADWIDE
    Key([mod, "shift"], "f", lazy.layout.flip(), desc='Flip Layout'),

# MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "j", lazy.layout.shuffle_up(), desc='Move Window Up The Stack'),
    Key([mod, "shift"], "k", lazy.layout.shuffle_down(), desc='Move Window Down The Stack'),
    Key([mod, "shift"], "l", lazy.layout.grow(), desc='Grow Window Size'),
    Key([mod, "shift"], "h", lazy.layout.shrink(), desc='Shrink Window Size'),

    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc='Move Window Up The Stack'),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc='Move Window Down The Stack'),
    Key([mod, "shift"], "Right", lazy.layout.grow(), desc='Grow Window Size'),
    Key([mod, "shift"], "Left", lazy.layout.shrink(), desc='Shrink Window Size'),

# TOGGLE FLOATING LAYOUT
    Key([mod, "shift"], "space", lazy.window.toggle_floating(), desc='Toggle Window Floating'),

# Change group
    Key([mod], "Tab", lazy.screen.next_group(), desc='Next Workspace'),
    Key([mod, "shift" ], "Tab", lazy.screen.prev_group(), desc='Previous Workspace'),
    Key(["mod1"], "Tab", lazy.group.next_window(), desc='Next Window'),
    Key(["mod1", "shift"], "Tab", lazy.group.prev_window(), desc='Previous Window'),

]
#ENDKEYS

groups = []
group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",]
group_labels = ["", "", "", "", "", "", "", "", "", ""]
group_layouts = ["monadtall", "max", "max", "max", "max", "max", "max", "max", "max", "floating",]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

for i in groups:
    keys.extend([

#CHANGE WORKSPACES
        Key([mod], i.name, switch_workspace(i.name), desc='Switch to Workspace {}'.format(i.name)),

# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name) , lazy.group[i.name].toscreen(), desc='Move Window to Workspace {}'.format(i.name)),
    ])

def init_layout_theme():
    return {"margin":10,
            "border_width":2,
            "border_focus": "#6790eb",
            "border_normal": "#2F343F",
            }

layout_theme = init_layout_theme()

layouts = [
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    layout.Matrix(**layout_theme),
    layout.Max(**layout_theme),
    layout.Floating(**layout_theme),
]

# COLORS FOR THE BAR
def init_colors():
    return [["#2F343F", "#2F343F"], # color 0
            ["#2F343F", "#2F343F"], # color 1
            ["#c0c5ce", "#c0c5ce"], # color 2
            ["#ff5050", "#ff5050"], # color 3
            ["#f4c2c2", "#f4c2c2"], # color 4
            ["#ffffff", "#ffffff"], # color 5
            ["#ffd47e", "#ffd47e"], # color 6
            ["#62FF00", "#62FF00"], # color 7
            ["#000000", "#000000"], # color 8
            ["#c40234", "#c40234"], # color 9
            ["#6790eb", "#6790eb"], # color 10
            ["#ff00ff", "#ff00ff"], #11
            ["#4c566a", "#4c566a"], #12
            ["#282c34", "#282c34"], #13
            ["#212121", "#212121"], #14
            ["#e75480", "#e75480"], #15
            ["#2aa899", "#2aa899"], #16
            ["#abb2bf", "#abb2bf"],# color 17
            ["#555555", "#555555"], #18
            ["#56b6c2", "#56b6c2"], #19
            ["#b48ead", "#b48ead"], #20
            ["#e06c75", "#e06c75"], #21
            ["#fb9f7f", "#fb9f7f"], #22
            ["#ffd47e", "#ffd47e"]] #23

colors = init_colors()

# Default Separator format
def sep():
    return dict(linewidth = 1,
                padding = 10,
                size_percent = 65,
                fontsize = 90)

# WIDGETS FOR THE BAR

basecolor = colors[14]
maincolor = colors[18]

def init_widgets_defaults():
    return dict(font="Ubuntu Mono",
                fontsize = 22,
                padding = 2,
                foreground = colors[5],
                background = colors[14])

widget_defaults = init_widgets_defaults()

def init_widgets_list():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [
                widget.GroupBox(
                    font='Ubuntu Mono',
                    fontsize = 22,
                    padding_x = 3,
                    padding_y = 9,
                    active=colors[5],
                    inactive=colors[2],
                    highlight_method='block',
                    urgent_alert_method='block',
                    urgent_border=colors[9],
                    this_current_screen_border=maincolor,
                    this_screen_border=colors[17],
                    other_current_screen_border=colors[13],
                    other_screen_border=colors[17],
                    disable_drag=True,
                ),

                widget.Sep(**sep()),

                # widget.Spacer(),

                widget.TaskList(
                    highlight_method = 'block', # or border
                    font='Ubuntu Mono',
                    icon_size=22,
                    rounded=True,
                    padding_x=5,
                    padding_y=10,
                    margin_y=0,
                    fontsize=0,
                    border=maincolor,
                    foreground=colors[5],
                    margin=0,
                    txt_floating='🗗',
                    txt_minimized='>_ ',
                    borderwidth = 1,
                    background=basecolor,
                ),

                widget.WindowName(
                    font='Ubuntu Mono',
                    width=500,
                    max_chars=30,
                    fontsize=22,
                ),

                widget.CurrentLayoutIcon(
                    custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                    padding = 0,
                    scale = 0.7
                ),

                widget.Sep(**sep()),

                widget.ThermalSensor(
                    fmt = '{}',
                    tag_sensor = "Core 0",
                    update_interval = 5,
                ),

                widget.Sep(**sep()),

                widget.Battery(
                    format = ' {char} {percent:2.0%}',
                    update_interval = 2,
                    charge_char = '',
                    discharge_char = '',
                    full_char = '=',
                    mouse_callbacks = {'Button1': lambda : qtile.cmd_spawn(myTerm + " -e btop")},
                ),

                widget.Sep(**sep()),

                widget.Wlan(
                    format = '{quality} {essid}',
                    disconnected_message = 'Disconnected',
                    max_chars = 9,
                    mouse_callbacks = {'Button1': lambda : qtile.cmd_spawn(myTerm + " -e " + home + "/.config/qtile/scripts/nmtui.sh")}, #fixes nmtui resizing issue
                    update_interval = 5,
                ),

                widget.Sep(**sep()),

                widget.Volume(
                    fmt = " {}",
                ),

                widget.Sep(**sep()),

                widget.Clock(
                    mouse_callbacks = {'Button1': lambda : qtile.cmd_spawn(myTerm + " -e " + home + "/.config/misc/timescript.sh")},
                    format="%a, %y %b %d",
                ),

                widget.Sep(**sep()),

                widget.Clock(
                    mouse_callbacks = {'Button1': lambda : qtile.cmd_spawn(myTerm + " -e " + home + "/.config/misc/timescript.sh")},
                    format="%H:%M",
                ),

                widget.Sep(**sep()),

                widget.Wttr(
                    format = '%c%t (%f)', #%l:
                    # update_interval = 1200,
                    mouse_callbacks = {'Button1': lambda : qtile.cmd_spawn(myTerm + " -e " + home + "/.config/misc/timescript.sh")},
                    location = {"Hanoi":"Hanoi"},
                ),

                # widget.Sep(**sep()),

                # widget.Systray(
                #     icon_size=30,
                # ),

                # widget.Sep(**sep()),

                # widget.Image(
                #     margin = 3,
                #     filename = '~/.config/qtile/icons/power2.png',
                #     mouse_callbacks = {'Button1': lazy.spawn('/home/hp/.config/misc/dm-logout.sh')},
                # ),

        ]
    return widgets_list

def init_widgets_list_vert():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [
                # widget.Cmus(),


                widget.Spacer(),

                widget.Systray(
                    icon_size=30,
                ),

                widget.Sep(**sep()),

                widget.Image(
                    margin = 3,
                    filename = '~/.config/qtile/icons/power2.png',
                    mouse_callbacks = {'Button1': lazy.spawn('/home/hp/.config/misc/dm-logout.sh')},
                ),


        ]
    return widgets_list

widgets_list = init_widgets_list()

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2

widgets_screen1 = init_widgets_screen1()

widgets_screen2 = init_widgets_screen2()

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_list(), size=40, opacity=0.85, background="000000"),
                left=bar.Bar(widgets=init_widgets_list_vert(), size=40, opacity=0.85, background= "000000"))]

screens = init_screens()

# MOUSE CONFIGURATION
mouse = [
    Drag("M-1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),

    Drag("M-3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),

    Click("M-2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []

# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME
# BEGIN

#########################################################
################ assgin apps to groups ##################
#########################################################
@hook.subscribe.client_new
def assign_app_group(client):
    d = {}
    #########################################################
    ################ assgin apps to groups ##################
    #########################################################
    d["1"] = []
    d["2"] = ["emacs"]
    d["3"] = ["crx_fkpbmjlkacnnbncjojlbhceofjnapopf", "google-chrome"]
    d["4"] = ["kdenlive"]
    d["5"] = ["Steam"]
    d["6"] = ["tmux", "nuclear", "crx_agimnkijcaahngcdmfeangaknmldooml",]
    d["7"] = ["thunar", "ranger"]
    d["8"] = ["sysmon", "qBittorrent"]
    d["9"] = ["telegram-desktop", ]
    d["0"] = []
    ##########################################################
    wm_class = client.window.get_wm_class()[0]

    for i in range(len(d)):
        if wm_class in list(d.values())[i]:
            group = list(d.keys())[i]
            client.togroup(group)
            client.group.cmd_toscreen()

# END
# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME

main = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])

@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])

@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True

floating_types = ["notification", "toolbar", "splash", "dialog"]
follow_mouse_focus = False # This causes focus jump when using dmenu if set to True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    *layout.Floating.default_float_rules,
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='file_progress'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='confirmreset'),
    Match(wm_class='makebranch'),
    Match(wm_class='maketag'),
    Match(wm_class='Arandr'),
    # Match(wm_class='feh'),
    Match(wm_class='Galculator'),
    Match(title='branchdialog'),
    Match(title='Open File'),
    Match(title='pinentry'),
    Match(wm_class='ssh-askpass'),
    Match(wm_class='lxpolkit'),
    Match(wm_class='Lxpolkit'),
    Match(wm_class='yad'),
    Match(wm_class='Yad'),
    Match(wm_class='Cairo-dock'),
    Match(wm_class='cairo-dock'),
    Match(title='Save File'),
    Match(wm_class='qutebrowser'),
    Match(wm_class='calc'),
    # Match(wm_class='caffeine'),

], fullscreen_border_width = 0, border_width = 0)

auto_fullscreen = True
focus_on_window_activation = "smart" # or focus
wmname = "Qtile" # LG3D if Java applications return errors
