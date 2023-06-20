import time
import sys
import subprocess
import argparse
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


def section(title: str):
    print(f"\n> {TC.BLUE}{title}{TC.RESET}")


def exec_cmd(cmd: str, cwd="./"):
    print(f"{cmd}", end="", flush=True)
    if DRY_RUN:
        print(f" {TC.YELLOW}dry run{TC.RESET}")
        return
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        executable="bash",
        cwd=cwd,
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
    print(f" {TC.GREEN}passed{TC.RESET} ({timeDelta:.3f}s)")
    return out


def get_args():
    parser = argparse.ArgumentParser(
        description="Setup environment",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
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

    global DRY_RUN
    DRY_RUN = args.dry_run
    if DRY_RUN:
        print(f"{TC.YELLOW}dry run{TC.RED} mode{TC.GREEN} is{TC.BLUE} ON{TC.RESET}")

    section("Install apt packages")
    apt_packages = [
        "gconf-editor",
        "neovim",
        "git",
        "silversearcher-ag",
        "wget",
        "tmux",
        "htop",
        "ninja-build",
        "python3-pip"
    ]
    exec_cmd(f"sudo apt-get update && sudo apt-get install -y {' '.join(apt_packages)}")

    section("Install oh-my-bash and theme")
    exec_cmd(
        "curl -L https://raw.githubusercontent.com/aben20807/oh-my-ouo/master/setup.sh | bash"
    )

    section("Install Rust and related tools")
    exec_cmd("curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y")
    exec_cmd("source ~/.cargo/env")
    exec_cmd("rustc --version")
    exec_cmd("cargo install exa du-dust git-delta")
    exec_cmd("cargo install --locked bat")
    exec_cmd(r"""printf "\nalias ls='exa -F --group-directories-first'" >> ~/.bashrc""")
    exec_cmd(r"""printf "\nalias ll='exa -alF'" >> ~/.bashrc""")
    exec_cmd(r"""printf "\nalias lls='exa --sort=size -l'" >> ~/.bashrc""")
    exec_cmd(r"""printf "\nalias cat='bat'" >> ~/.bashrc""")
    exec_cmd(r"""printf "\nalias disk='dust'" >> ~/.bashrc""")

    section("Tmux")
    # https://github.com/aben20807/aben20807.vim/blob/master/.tmux.conf

    section("Neovim")

    section("Setup GNOME GUI")
    exec_cmd(
        "gsettings set org.gnome.shell.extensions.dash-to-dock click-action minimize-or-overview"
    )
    exec_cmd(
        "gsettings set org.desktop.input-sources.xkb-options custom-value ['caps:escape']"
    )

    # reset terminal color for WSL in windows
    # exec_cmd("tput init")


if __name__ == "__main__":
    main()
