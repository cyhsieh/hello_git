#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.



nowsub = 教測統

spend(start,end)
{
total := end - start
if (total <= 0)
	total += 60*60
min := floor(total / 60)
sec := mod(total,60)
return min . "分" . sec .  "秒"
}


^1::
inputbox,num,現在科目：%nowsub%,Enter the vol num of this disk...
if ErrorLevel
	return
else
{
run,detect.ahk
start := A_min*60 + A_sec 
runwait,xcopy D: F:\QQQQQ\高明老師教測統\101%nowsub%第%num%堂 /D/K/E/Y/C/I/H
end := A_min*60 + A_sec
div := spend(start,end)
msgbox,%nowsub%第%num%堂摳完了！ `n花了%div%
}
return