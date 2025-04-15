# TMUX

+ ref: [Tmux](https://aben20807.github.io/posts/20190814-tmux/)

## Install

```bash
$ sudo snap install tmux
$ printf '\nexport TERM=xterm' >> ~/.bashrc
$ # reopen terminal
```

+ `.tmux.conf`: [aben20807/dotfiles/linux/.tmux.conf](https://github.com/aben20807/dotfiles/blob/master/linux/.tmux.conf)

## My prefix key

+ PREFIX = `Ctrl-q`

## Create window

+ PREFIX `n`

## Go to previous/next window

+ `M-Left`
+ `M-Right`

## Swap (reorder) window

+ `S-Left`
+ `S-Right`

## Rename window

+ PREFIX `,`

## Create pane

+ PREFIX `|`: split right
+ PREFIX `-`: split down

## Copy mode

+ PREFIX `[`: change to copy mode
+ `q`: quit copy mode
+ PREFIX `v`: select in copy mode
+ PREFIX `y`: copy select in copy mode
+ PREFIX `]`: paste
+ PREFIX `p`: paste

## FZF

+ `C-f`: open fzf in command mode

## man

+ PREFIX `/`: open man in command mode

## Useful functions

+ PREFIX `w`: open the dash board of all sessions and windows
+ PREFIX `s`: open the dash board of all sessions
+ PREFIX `z`: zoom in/out the current pane
+ PREFIX `t`: show current time
+ PREFIX `?`: check all key bindings
+ PREFIX `:`: change to command mode
+ PREFIX `C-k`: clear history (scrollback buffer)

## Misc.

+ PREFIX `r`: reload config
