Set op=CreateObject("op.opsoft")

MsgBox op.Ver()

MsgBox op.GetBasePath()
op.Sleep 1000
ret = op.RunApp("notepad.exe",0)
ret = op.MoveTo(30,30)


hwnd=op.FindWindow("","无标题 - 记事本")
if hwnd then
MsgBox hwnd
	ret=op.BindWindow(hwnd,"gdi","windows","windows",0)
	
	op.Sleep 1000
	if ret then
		MsgBox "bind ok"
		
		ret=op.Capture(0,0,2000,2000,"screen.bmp")
	else
		MsgBox "bind false"
	end if
	
	op.UnBindWindow
end if

Set op=nothing