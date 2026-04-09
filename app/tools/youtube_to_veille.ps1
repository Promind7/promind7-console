# Whisper uniquement → Sources/videos/transcripts (playlist : en chaîne)
# Usage (depuis la racine du repo V2) :
#   powershell -File app/tools/youtube_to_veille.ps1 "https://www.youtube.com/watch?v=..."
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Url,
    [string]$WhisperModel = "base",
    [string]$WhisperLang = "",
    [switch]$NoPlaylist,
    [int]$MaxVideos = 0
)
$ErrorActionPreference = "Stop"
$AppDir = Split-Path -Parent $PSScriptRoot
$Root = Split-Path -Parent $AppDir
Set-Location $Root
$pyArgs = @(
    "app/tools/fetch_youtube_transcript.py",
    $Url,
    "--whisper-model", $WhisperModel
)
if ($WhisperLang) {
    $pyArgs += @("--whisper-lang", $WhisperLang)
}
if ($NoPlaylist) {
    $pyArgs += "--no-playlist"
}
if ($MaxVideos -gt 0) {
    $pyArgs += @("--max-videos", "$MaxVideos")
}
& python @pyArgs
