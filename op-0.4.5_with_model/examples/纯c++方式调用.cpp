// 此文件包含 "main" 函数。程序执行将在此处开始并结束。
// 纯c++ 调用，不需要将插件注册到系统
// 注意： 由于stl的二进制兼容性很差，因此需要在相同编译环境下使用libop!!!,否则会出错
// 更多调用方式可参考op项目的tests子项目

#include <iostream>

#include <string>
#include<vector>

#include "libop.h" //libop接口的头文件
#ifdef _M_X64
#pragma comment(lib,"../bin/x86/op_x64.lib") //64位lib
#else
#pragma comment(lib,"../bin/x86/op_x86.lib") //32位lib
#endif



int main(int argc, char* argv[])
{
	using namespace std;
	//op接口的类名为libop,这里直接实例化使用即可
	libop op;
	wstring ver;
	op.Ver(ver);
	std::wcout << ver << std::endl;
	long ret;
	op.MoveTo(30, 30, &ret);
	op.SetShowErrorMsg(1, &ret);
	op.SetPath(L"C:/Users/wall/Desktop", &ret);

	long x, y;
	op.FindPic(0, 0, 2000, 2000, L"test.bmp", L"000000", 1.0, 0, &x, &y, &ret);

	return 0;
}

