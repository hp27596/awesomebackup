#!/usr/bin/env python3
from config import keys

#sort keybinds by modifiers
keys.sort(key=lambda x: x.modifiers)

clnlist = {}
genbind = {}
navbind1 = {}
navbind2 = {}
wsbind = {}

#clean up the list
for i in keys:
    if 'XF86' in i.key:
        continue
    else:
        keybind = ''
        for j in i.modifiers:
            if j == 'mod4':
                j = 'Super'
            if j == 'mod1':
                j = 'Alt'
            if j == 'shift':
                j = 'Shift'
            if j == 'control':
                j = 'Ctrl'

            keybind = keybind + j + ' '

        if i.key == 'space':
            i.key = 'Space'
        elif i.key == 'slash':
            i.key = '/'
        elif i.key == 'comma':
            i.key = ','
        elif i.key == 'period':
            i.key = '.'
        else:
            pass

        keybind = keybind + i.key
        clnlist.update({keybind:i.desc})

navkey = ['Up', 'Down', 'Left', 'Right', ' h', ' j', ' k', ' l']

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

for key, desc in clnlist.items():
    if 'Workspace' in desc:
        wsbind.update({key:desc})
    elif any(nav in key for nav in navkey) and ('Meta' in key):
        navbind1.update({key:desc})
    elif any(x in desc for x in ['Window', 'Layout']):
        navbind2.update({key:desc})
    else:
        genbind.update({key:desc})

print('Workspace Keybinds')
print('----------------')
for key, desc in wsbind.items():
    print(key, '=', desc)

print('\nNavigation Keybinds')
print('----------------')
for key, desc in navbind1.items():
    print(key, '=', desc)

print('----------------')
for key, desc in navbind2.items():
    print(key, '=', desc)

print('\nGeneral Keybinds')
print('----------------')
for key, desc in genbind.items():
    print(key, '=', desc)
