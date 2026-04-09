$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$WshShell = New-Object -comObject WScript.Shell
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "ProMind7.lnk"
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "wscript.exe"
$Shortcut.Arguments = """$RepoRoot\Lancer_ProMind7_Silent.vbs"""
$Shortcut.IconLocation = "$RepoRoot\promind7_logo.ico"
$Shortcut.WorkingDirectory = $RepoRoot
$Shortcut.Description = "Lancer ProMind7 (Silent)"
$Shortcut.Save()
Write-Host "Shortcut created at $ShortcutPath"
