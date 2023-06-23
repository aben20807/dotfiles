import time
import sys
import os
import subprocess
import argparse
from typing import List, Union
from urllib import request, error
from types import SimpleNamespace

""" terminal color """
TC = SimpleNamespace(
    **{
        "YELLOW": "\033[33m",
        "GREEN": "\033[92m",
        "RED": "\033[91m",
        "BLUE": "\033[34m",
        "RESET": "\033[0m",
    }
)

DRIVER_PATH = os.path.dirname(os.path.realpath(__file__))


def check_network():
    try:
        request.urlopen("https://www.google.com/", timeout=5)
        return True
    except error.URLError:
        return False


class Cmd:
    def __init__(self, cmd: str, cwd="./") -> None:
        self.cmd = cmd
        self.cwd = cwd

    def run(self):
        print(f"{self.cmd}", end="", flush=True)
        cwd_not_cur = f" in {self.cwd}" if self.cwd != "./" else ""
        if DRY_RUN:
            print(f"{cwd_not_cur} {TC.YELLOW}dry run{TC.RESET}")
            return
        process = subprocess.Popen(
            self.cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            executable="bash",
            cwd=self.cwd,
        )
        timeStarted = time.time()
        out = ""
        try:
            out, err = process.communicate()
            if process.returncode != 0:
                raise RuntimeError(str(out + err, encoding="utf8"))
        except RuntimeError as e:
            print(f" {TC.RED}failed{TC.RESET}")
            print(e)
            sys.exit(1)

        timeDelta = time.time() - timeStarted
        print(f"{cwd_not_cur} {TC.GREEN}passed{TC.RESET} ({timeDelta:.3f}s)")
        return out


def section(title: str, cmd_list: Union[List[Cmd], None] = None):
    if cmd_list is None:
        cmd_list = []
    global CUR_SECTION
    if CUR_SECTION >= START_SECTION:
        print(f"\n> #{CUR_SECTION} {TC.BLUE}{title}{TC.RESET}")
        for cmd in cmd_list:
            cmd.run()
    CUR_SECTION += 1


def get_args():
    parser = argparse.ArgumentParser(
        description="Setup environment",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "mode", type=str, choices=["install", "clean"]
    )
    parser.add_argument(
        "-s",
        "--section",
        type=int,
        default=0,
        help="run from the given section number",
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="just dry run without running commands",
    )
    parser.add_argument(
        "--no-color", action="store_true", help="disable the terminal color"
    )
    return parser.parse_args()


def install():
    ppa_packages = ["ppa:neovim-ppa/stable"]
    section(
        "PPA packages",
        [Cmd(f"sudo add-apt-repository -y {' '.join(ppa_packages)}")],
    )

    apt_packages = [
        "dconf-editor",
        "neovim",
        "silversearcher-ag",
        "wget",
        "tmux",
        "htop",
        "ninja-build",
        "python3-pip",
        "chrome-gnome-shell",
        "net-tools",
        "bmon",
        "valgrind",
        "nodejs",
        "autoconf",
        "automake",
        "libtool",
        "pkg-config",
        "libssl-dev",
        "libffi-dev",
        "gcc",
        "make",
        "xclip",
        "fcitx-bin",
        "fcitx-chewing",
        "xutils-dev",
    ]
    section(
        "apt packages",
        [
            Cmd(
                f"sudo apt-get update && sudo apt-get install -y {' '.join(apt_packages)}"
            )
        ],
    )

    section(
        "git config", [Cmd(f"ln -s -b {DRIVER_PATH}/dotfiles/.gitconfig ~/.gitconfig")]
    )

    python_packages = [
        "setuptools",
        "pip",
        "cmake",
        "ranger",
        "colour-valgrind",
        "pygments",
        "black",
    ]
    section(
        "python packages",
        [
            Cmd(f"python3 -m pip install --upgrade {' '.join(python_packages)}"),
        ],
    )

    section(
        "oh-my-bash and theme",
        [
            Cmd(
                "curl -L https://raw.githubusercontent.com/aben20807/oh-my-ouo/master/setup.sh | bash"
            ),
            Cmd(r"sed -i 's/^\(OSH_THEME\s*=\s*\).*$/\1\"ouo\"/' ~/.bashrc"),
        ],
    )

    section(
        "rust and related tools",
        [
            Cmd(
                "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y"
            ),
            Cmd(
                r"""source "$HOME/.cargo/env" && rustc --version && cargo install exa du-dust git-delta && cargo install --locked bat"""
            ),
        ],
    )

    bashrc_alias_list = [
        "ls='exa -F --group-directories-first'",
        "ll='exa -alF'",
        "lls='exa --sort=size -l'",
        "cat='bat'",
        "disk='dust'",
        "r='ranger'",
        "vfzf='vim $(fzf)'",
        "vim='nvim'",
        "svim='sudo vim'",
        "apt-get='apt'",
        "explorer='nautilus'",
        "valgrind='colour-valgrind'",
    ]
    expanded = r"".join([rf"\nalias {a}" for a in bashrc_alias_list])
    section("bashrc alias", [Cmd(rf"""printf "{expanded}" >> ~/.bashrc""")])

    section(
        "tmux",
        [
            Cmd("printf '\nexport TERM=xterm\n' >> ~/.bashrc && source ~/.bashrc"),
            Cmd(f"ln -s -b {DRIVER_PATH}/dotfiles/.tmux.conf ~/.tmux.conf"),
            Cmd("mkdir ~/.tmux/plugins/ -p"),
            Cmd("git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm"),
            Cmd("bash ~/.tmux/plugins/tpm/bin/install_plugins"),
        ],
    )

    section("gdb", [Cmd("wget -P ~ https://git.io/.gdbinit")])

    # https://github.com/aben20807/blog-post-issues/issues/26
    section(
        "ctags",
        [
            Cmd("git clone https://github.com/universal-ctags/ctags.git"),
            Cmd("./autogen.sh && ./configure && make", f"{DRIVER_PATH}/ctags/"),
            Cmd("sudo make install", f"{DRIVER_PATH}/ctags/"),
        ],
    )

    section(
        "neovim",
        [
            Cmd("mkdir ~/.config/nvim -p"),
            Cmd(
                """sh -c 'curl -fLo "${XDG_DATA_HOME:-$HOME/.local/share}"/nvim/site/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'"""
            ),
            Cmd("curl -sL https://deb.nodesource.com/setup_16.x | sudo -E bash -"),
            Cmd(f"lndir -silent {DRIVER_PATH}/dotfiles/.config/nvim ~/.config/nvim"),
            Cmd("vim +'silent! PlugInstall' +qall < /dev/tty"),
            Cmd("curl https://pyenv.run | bash"),
            Cmd("""echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc"""),
            Cmd(
                """echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc"""
            ),
            Cmd("""echo 'eval "$(pyenv init -)"' >> ~/.bashrc"""),
            Cmd(
                "~/.pyenv/bin/pyenv install -v 3.10.6 && ~/.pyenv/bin/pyenv virtualenv 3.10.6 neovim3"
            ),
            Cmd("~/.pyenv/versions/neovim3/bin/python -m pip install pynvim"),
        ],
    )

    section(
        "setup GNOME GUI",
        [
            Cmd(
                "gsettings set org.gnome.shell.extensions.dash-to-dock click-action minimize-or-overview"
            ),
            Cmd(
                '''gsettings set org.gnome.desktop.input-sources xkb-options "['caps:escape']"'''
            ),
            Cmd("gsettings set org.gnome.desktop.interface cursor-blink false"),
        ],
    )

    section(
        "nautilus",
        [
            Cmd("git clone https://github.com/chr314/nautilus-copy-path.git"),
            Cmd("sudo make install && nautilus -q", f"{DRIVER_PATH}/nautilus-copy-path"),
        ],
    )

    section("Finished. Please reopen the terminal.")


def clean():
    apt_packages = [
        "dconf-editor",
        "neovim",
        "silversearcher-ag",
        "tmux",
        "htop",
        "ninja-build",
        "chrome-gnome-shell",
        "net-tools",
        "bmon",
        "valgrind",
        "nodejs",
        "autoconf",
        "automake",
        "libtool",
        "pkg-config",
        "libssl-dev",
        "libffi-dev",
        "gcc",
        "xclip",
        "fcitx-bin",
        "fcitx-chewing",
        "xutils-dev",
    ]
    section(
        "apt packages",
        [Cmd(f"sudo apt-get purge --autoremove -y {' '.join(apt_packages)}")],
    )

    ppa_packages = ["ppa:neovim-ppa/stable"]
    section(
        "PPA packages",
        [Cmd(f"sudo add-apt-repository --remove -y {' '.join(ppa_packages)}")],
    )


    section("git config", [Cmd(f"rm -f ~/.gitconfig")])

    python_packages = [
        "cmake",
        "ranger",
        "colour-valgrind",
        "pygments",
        "black",
    ]
    section(
        "python packages",
        [
            Cmd(f"python3 -m pip uninstall -y {' '.join(python_packages)}"),
        ],
    )

    section(
        "rust and related tools",
        [
            Cmd("rm -rf ~/.cargo && rm -rf ~/.rustup"),
        ],
    )

    section(
        "tmux",
        [
            Cmd(f"rm -f ~/.tmux.conf"),
            Cmd("yes | rm -rf ~/.tmux/"),
        ],
    )

    section("gdb", [Cmd("rm -f ~/.gdbinit")])

    # https://github.com/aben20807/blog-post-issues/issues/26
    section(
        "ctags",
        [
            Cmd("sudo make uninstall", f"{DRIVER_PATH}/ctags/"),
        ],
    )

    section(
        "neovim",
        [
            Cmd("rm -rf ~/.config/nvim"),
            Cmd("yes | rm -rf ~/.pyenv"),
        ],
    )

    section(
        "nautilus",
        [
            Cmd("sudo make uninstall && nautilus -q", f"{DRIVER_PATH}/nautilus-copy-path"),
        ],
    )

    section("Finished. Please reopen the terminal.")


def main():
    args = get_args()

    if args.no_color:
        for k in TC.__dict__:
            TC.__dict__[k] = ""

    if not check_network():
        print(f"{TC.RED}Please check your network settings{TC.RESET}")
        sys.exit(1)

    global DRY_RUN
    DRY_RUN = args.dry_run
    if DRY_RUN:
        print(f"{TC.YELLOW}dry run{TC.RED} mode{TC.GREEN} is{TC.BLUE} ON{TC.RESET}")

    global START_SECTION
    START_SECTION = args.section
    global CUR_SECTION
    CUR_SECTION = 0

    if args.mode == "install":
        install()
    elif args.mode == "clean":
        clean()


if __name__ == "__main__":
    main()
