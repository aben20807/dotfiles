# Neovim

+ ref: [To Lua or Not to Lua](https://aben20807.github.io/posts/20231103-to-lua-or-not-to-lua/)

## Install

+ use [bob](https://github.com/MordechaiHadad/bob)

```bash
$ cargo install bob-nvim
$ bob install 0.11.0
$ bob ls
$ bob use 0.11.0
```

## Setup for virtual environment (legacy)

```bash
$ mkdir ~/.config/nvim -p
$ sh -c 'curl -fLo "${XDG_DATA_HOME:-$HOME/.local/share}"/nvim/site/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'
$ curl -sL https://deb.nodesource.com/setup_16.x | sudo -E bash -
$ sudo apt-get update && sudo apt-get install -y nodejs"),
$ lndir -silent {DRIVER_PATH}/dotfiles/.config/nvim ~/.config/nvim
$ vim +'silent! PlugInstall' +qall < /dev/tty
$ curl https://pyenv.run | bash
$ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
$ echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
$ echo 'eval "$(pyenv init -)"' >> ~/.bashrc
$ ~/.pyenv/bin/pyenv install -v 3.10.6 && ~/.pyenv/bin/pyenv virtualenv 3.10.6 neovim3
$ ~/.pyenv/versions/neovim3/bin/python -m pip install pynvim
```

## Alias

```
$ printf '\nalias vim=nvim' >> ~/.bashrc
$ # reopen terminal
```

