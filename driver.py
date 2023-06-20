import time
import sys
import subprocess

YELLOW = "\033[33m"
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[34m"
RESET = "\033[0m"

def section(title: str):
    print(f"\n> {BLUE}{title}{RESET}")

def exec_cmd(cmd: str, cwd="./"):
    print(f"{cmd}", end="", flush=True)
    if DRY_RUN:
        print(f" {YELLOW}dry run{RESET}")
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
    try:
        out, _ = process.communicate()
        if process.returncode != 0:
            raise RuntimeError(str(out, encoding="utf8"))
    except RuntimeError as e:
        print(f" {RED}failed{RESET}")
        print(e)
        sys.exit(1)
    timeDelta = time.time() - timeStarted
    print(f" {GREEN}passed{RESET} ({timeDelta:.3f}s)")
    return out

def main():
    global DRY_RUN
    DRY_RUN = True
    if DRY_RUN:
        print(f"{YELLOW}dry run{RED} mode{GREEN} is{BLUE} ON{RESET}")

    section("Install apt packages")
    apt_packages = ["gconf-editor", "neovim", "git", "silversearcher-ag"]
    exec_cmd(f"sudo apt-get install -y {apt_packages}")

    section("Install oh-my-bash and theme")
    exec_cmd("curl -L https://raw.githubusercontent.com/aben20807/oh-my-ouo/master/setup.sh | bash")

    # reset terminal color for WSL in windows
    # exec_cmd("tput init")

if __name__ == "__main__":
    main()
