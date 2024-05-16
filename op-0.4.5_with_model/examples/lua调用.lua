--//test begin-----------
print("test begin");
--init luacom
require("luacom");
--create op object
op=luacom.CreateObject("op.opsoft");
--print ver
print(op:Ver());
print(op:GetBasePath());
op:WinExec("notepad",1);


hwnd=op:FindWindow("","无标题 - 记事本");
if hwnd then
	send_hwnd=op:FindWindowEx(hwnd,"Edit","");
	ret=op:BindWindow(hwnd,"gdi","windows","windows",0);
	op:Sleep(1000);
	if ret then
		op:SendString(send_hwnd,"Hello World!");
		op:Sleep(500);
		print("bind ok.");
		print(op:GetColor(30,30));
		ret=op:Capture(0,0,100,100,"screen.bmp");
	else
		print("bind false");
	end
	
	
	
	
	op:UnBindWindow();
end

print("test end");

