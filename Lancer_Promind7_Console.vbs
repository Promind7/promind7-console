' Lance la console Streamlit sans fenêtre CMD (double-clic).
' Le dossier du script = racine du projet (même niveau que promind7_console.py).

Option Explicit

Dim fso, sh, root, venvPy, pyExe, cmd

Set fso = CreateObject("Scripting.FileSystemObject")
Set sh = CreateObject("WScript.Shell")
root = fso.GetParentFolderName(WScript.ScriptFullName)

If Not fso.FileExists(root & "\promind7_console.py") Then
    MsgBox "Fichier introuvable : promind7_console.py" & vbCrLf & "Emplacement attendu : " & root, vbCritical, "Promind7 Console"
    WScript.Quit 1
End If

sh.CurrentDirectory = root

' Parcours Stage & emploi : scripts sans suffixe -V2 sous 02-Contenus\01-Scripts
sh.Environment("Process")("PROMIND7_STAGE_EMPLOI_SCRIPT_ROOT") = _
    "D:\01-ProM7-consulting\01-Promind7\02-Contenus\01-Scripts\Parcours stage & emploi"

venvPy = root & "\.venv\Scripts\python.exe"
If fso.FileExists(venvPy) Then
    pyExe = Chr(34) & venvPy & Chr(34)
Else
    pyExe = "python"
End If

' 0 = fenêtre masquée ; False = ne pas attendre la fin (Streamlit reste actif)
cmd = "cmd /c cd /d " & Chr(34) & root & Chr(34) & " && " & pyExe & " -m streamlit run promind7_console.py"
sh.Run cmd, 0, False
