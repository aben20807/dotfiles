# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color|*-256color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
#force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
        # We have color support; assume it's compliant with Ecma-48
        # (ISO/IEC-6429). (Lack of such support is extremely rare, and such
        # a case would tend to support setf rather than setaf.)
        color_prompt=yes
    else
        color_prompt=
    fi
fi

if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\W\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\W\$ '
fi
unset color_prompt force_color_prompt

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \W\a\]$PS1"
    ;;
*)
    ;;
esac

# -------------------------------
# Functions
# -------------------------------

function now() {
    date '+%Y%m%d_%H%M%S'
}


# -------------------------------
# Aliases
# -------------------------------
# ls aliases
alias ll="ls -alF --color=auto"
alias la="ls -A --color=auto"
alias l="ls -CF --color=auto"

# Git aliases
alias gp="git push"
alias gl="git log"


# Server
alias duh="du -hs" # show current directory size
alias dfh="df -h" # show disk usage
alias dud1h="du -d 1 -h"

# HuggingFace
alias hfc="huggingface-cli"

# UV VENV
alias sva="source .venv/bin/activate"
alias svga="source ~/general_venv/bin/activate" # make a general venv in home dir before using this

# GPU
alias nvi="nvidia-smi"
alias nvt="nvtop"

alias rocs="rocm-smi"
alias amt="amdgpu_top"

# Tmux
alias tns="tmux new -s"
alias tls="tmux ls"
alias tat="tmux attach -t"
alias tks="tmux kill-session -t"
alias tksall="tmux kill-server"

# Slurm
alias sinfa="sinfo -a"
alias seqa='squeue -a --format "%.18i %.9P %.34j %.8u %.2t %.10M %.6D %R"'
alias scons="scontrol show"
alias seqd="echo -n '在線人數:  ';w | grep aben | wc -l;echo '----squeue----';squeue -o '%.6i %.40j %.5y %.3t %.12M %.20R %.10b %.40Z';echo '----sinfo----';sinfo --exact -O 'PARTITION:13,Available:8,Nodes:6,NodeAddr:20,StateComplete,Gres

# Nsys
alias nsysp="nsys profile --stats=true --output=$(now)"


. "$HOME/.local/bin/env"

module load slurm

[[ -s /mnt/home/aben20807-gmai-6d67af/.autojump/etc/profile.d/autojump.sh ]] && source /mnt/home/aben20807-gmai-6d67af/.autojump/etc/profile.d/autojump.sh
export CUDA_HOME=$HOME/lib/cuda13
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH