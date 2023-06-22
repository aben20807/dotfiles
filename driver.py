import time
import sys
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
        "-s",
        "--section",
        type=int,
        default=0,
        help="run from the given section number",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        type=int,
        default=2,
        choices=[0, 1, 2, 3],
        help="verbose level",
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

    ppa_packages = ["ppa:neovim-ppa/stable"]
    section(
        "PPA packages",
        [Cmd(f"sudo add-apt-repository -y {' '.join(ppa_packages)}")],
    )

    apt_packages = [
        "dconf-tools",
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
    ]
    section(
        "apt packages",
        [
            Cmd(
                f"sudo apt-get update && sudo apt-get install -y {' '.join(apt_packages)}"
            )
        ],
    )

    python_packages = [
        "setuptools",
        "pip",
        "cmake",
        "ranger",
        "colour-valgrind",
        "pygments",
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
            )
        ],
    )

    section(
        "rust and related tools",
        [
            Cmd(
                "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y"
            ),
            Cmd(
                r"""printf '\n. "$HOME/.cargo/env"' >> ~/.bashrc && source ~/.bashrc"""
            ),
            Cmd("rustc --version"),
            Cmd("cargo install exa du-dust git-delta"),
            Cmd("cargo install --locked bat"),
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
            Cmd("printf '\nexport TERM=xterm' >> ~/.bashrc && source ~/.bashrc"),
            Cmd("ln -s -b ./dotfiles/.tmux.fonf" "~/.tmux.conf"),
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
            Cmd("./autogen.sh && ./configure && make", "./ctags/"),
            Cmd("sudo make install", "./ctags/"),
        ],
    )

    section(
        "neovim",
        [
            Cmd("mkdir ~/.config/ -p"),
            Cmd(
                """sh -c 'curl -fLo "${XDG_DATA_HOME:-$HOME/.local/share}"/nvim/site/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim'"""
            ),
            Cmd("curl -sL https://deb.nodesource.com/setup_16.x | sudo -E bash -"),
            Cmd("ln -s -b ./dotfiles/.config/nvim/" "~/.config/nvim/"),
            Cmd("vim +'silent! PlugInstall' +qall < /dev/tty"),
            Cmd(
                "curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash"
            ),
            Cmd(
                """echo 'export PATH="/home/'`whoami`'/.pyenv/bin:$PATH"' >> ~/.bashrc"""
            ),
            Cmd("""echo 'eval "$(pyenv init -)"' >> ~/.bashrc"""),
            Cmd("""echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc"""),
            Cmd("source ~/.bashrc"),
            Cmd("pyenv install -v 3.10.6"),
            Cmd("pyenv virtualenv 3.10.6 neovim3"),
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
                "gsettings set org.desktop.input-sources.xkb-options custom-value ['caps:escape']"
            ),
            Cmd("gsettings set org.gnome.desktop.interface cursor-blink false"),
        ],
    )

    section("Finished. Please reopen the terminal.")


if __name__ == "__main__":
    main()
