#!/bin/sh

if [[ $(pgrep emacs --exact) == '' ]]; then
    \emacs --daemon
fi

if [[ $(pgrep emacsclient) == '' ]]; then
    # \emacsclient -c -e '(dashboard-refresh-buffer)' &
    \emacsclient -c &
else
    \emacsclient -e '(progn (+workspace/new)(find-file "'$@'"))' &
fi

# qtile cmd-obj -o group 2 -f toscreen
