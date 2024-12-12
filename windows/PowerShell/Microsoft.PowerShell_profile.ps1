# source: https://blog.miniasp.com/post/2021/11/24/PowerShell-prompt-with-Oh-My-Posh-and-Windows-Terminal
using namespace System.Management.Automation
using namespace System.Management.Automation.Language

Import-Module -Name Terminal-Icons

oh-my-posh init pwsh --config "$env:POSH_THEMES_PATH\onehalf.minimal.omp.json"  | Invoke-Expression

# 移除兩個不實用的 Cmdlet Aliases
If (Test-Path Alias:curl) {Remove-Item Alias:curl}
If (Test-Path Alias:wget) {Remove-Item Alias:wget}

# 快速開啟 c:\windows\system32\drivers\etc\hosts 檔案
function hosts { notepad c:\windows\system32\drivers\etc\hosts }

# PSReadLine
if ($host.Name -eq 'ConsoleHost')
{
    Import-Module PSReadLine
}

Set-PSReadLineOption -PredictionSource History
Set-PSReadLineOption -PredictionViewStyle ListView
Set-PSReadLineOption -EditMode Windows

# 設定按下 Ctrl+d 可以退出 PowerShell 執行環境
Set-PSReadlineKeyHandler -Chord ctrl+d -Function ViExit

# Move
Set-PSReadlineKeyHandler -Chord ctrl+a -Function BeginningOfLine
Set-PSReadlineKeyHandler -Chord ctrl+e -Function EndOfLine

# Delete
Set-PSReadLineKeyHandler -Chord Ctrl+u -Function RevertLine
Set-PSReadLineKeyHandler -Chord Ctrl+k -Function DeleteToEnd
Set-PSReadlineKeyHandler -Chord ctrl+w -Function BackwardDeleteWord # one word

# 上下搜尋
Set-PSReadlineKeyHandler -Key UpArrow -Function HistorySearchBackward
Set-PSReadlineKeyHandler -Key DownArrow -Function HistorySearchForward
Set-PSReadLineOption -HistorySearchCursorMovesToEnd