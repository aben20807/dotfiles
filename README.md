# Dotfiles

## Setup

+ Note: if you want to use this repo, remember to modify `dotfiles/.gitconfig` 

```bash
sudo apt install curl && curl -L https://raw.githubusercontent.com/aben20807/dotfiles/master/setup.sh | bash 
```

## Not included

### Terminal perferences

+ Text and Background Color
  + uncheck `Use colors from system theme`
  + Built-in schemes: Tango dark
+ Palette
  + Built-in schemes: Tango

### COC extensions in Neovim

+ They will be automatically installed on first use of vim

### SSH for git

+ [107.03.02 git push 免帳號密碼 | ssh key](https://aben20807.blogspot.com/2018/03/1070302-git-push-ssh-key.html)

### Input method

+ `im-config` choose fcitx
+ Settings > Region & Language > Manage Installed Languages
+ Install/Remove Languages... > check "Chinese (traditional)" > Apply
+ Reboot
+ Open Fcitx Configuration
  + `+` > uncheck `Only Show Current Language` > search "Chewing" > OK
  + Configure > Global Config > Click Show Advance Option > Appearance > Do not show input window if there is only preedit string
+ Use `ctrl-space` to switch the input method


### GNOME Shell extensions

+ Open Extension Manager and search following extensions in the Browse tab
  + [cpufreq](https://extensions.gnome.org/extension/1082/cpufreq/)
  + [Net Speed](https://extensions.gnome.org/extension/4478/net-speed/)
  + [Freon](https://extensions.gnome.org/extension/841/freon/)
  + [Coverflow Alt-Tab](https://extensions.gnome.org/extension/97/coverflow-alt-tab/)
  + [OpenWeather](https://extensions.gnome.org/extension/750/openweather/)
