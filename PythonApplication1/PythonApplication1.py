#coding=utf-8
import tkinter
import tkinter.filedialog
from tkinter import *
import threading
import pyautogui
import time
from ctypes import *
import configparser
import os

#读取ini
curpath = os.getcwd()
#curpath = os.path.dirname(os.path.realpath(__file__))
cfgpath = os.path.join(curpath, "main.ini")
config = configparser.ConfigParser()
config.read(cfgpath, encoding="utf-8")
span=config.get('section_1','span')
t1=config.get('section_1','t1')
t2=config.get('section_1','t2')
t3=config.get('section_1','t3')
t4=config.get('section_1','t4')

now = time.strftime("%H:%M:%S",time.localtime())
def loop1():
    pyautogui.press('scrolllock')
    pyautogui.press('scrolllock')
    now1 = time.strftime("%H:%M:%S",time.localtime())
    print(now1)
    span1=int(span)
    time.sleep(span1)
def loop2():
    user32 = windll.LoadLibrary('user32.dll')
    user32.LockWorkStation()
def screenOff():
    time.sleep(3)
    HWND_BROADCAST = 0xffff
    WM_SYSCOMMAND = 0x0112
    SC_MONITORPOWER = 0xF170
    MonitorPowerOff = 2
    SW_SHOW = 5
    windll.user32.PostMessageW(HWND_BROADCAST, WM_SYSCOMMAND,SC_MONITORPOWER, MonitorPowerOff)
    shell32 = windll.LoadLibrary("shell32.dll")
    shell32.ShellExecuteW(None, 'open', 'rundll32.exe','USER32', '', SW_SHOW)
def LOOP():
    global stop_threads
    while (t1<now<t2 or t3<now<t4):
        loop1()
        if stop_threads:
            break
    while t1<=now<t2:
        loop2()
def Button_2_onCommand():
    global stop_threads
    str_obj.set("正在运行")
    stop_threads=False
    run_thread = threading.Thread(target=LOOP)
    run_thread.setDaemon(True)
    run_thread.start()
def Button_3_onCommand():
    str_obj.set("未运行")
    global stop_threads
    stop_threads=True
def Button_5_onCommand():
    off_thread = threading.Thread(target=screenOff)
    off_thread.start()


root = tkinter.Tk()
root.title('锁屏小工具')
#窗口居中
sw = root.winfo_screenwidth()
  #得到屏幕宽度
sh = root.winfo_screenheight()
  #得到屏幕高度
#窗口宽高为100
x = (sw-100) / 2
y = (sh-600) / 2
root.geometry('+%d+%d' %(x,y))


Button_2 = tkinter.Button(root, text="开始运行", font=('Arial', 12), width=10, height=1,
                         command=Button_2_onCommand)
Button_3 = tkinter.Button(root, text="结束运行", font=('Arial', 12), width=10, height=1,
                         command=Button_3_onCommand)
Button_5 = tkinter.Button(root, text="一键息屏", font=('Arial', 12), width=10, height=1,
                         command=Button_5_onCommand)

    
str_obj = tkinter.StringVar()
str_obj.set("正在运行")

span_in = tkinter.StringVar()
span_in.set("间隔时间：" + span + "秒")

Label_4 = tkinter.Label(root,
                 height = 1,
                 width = 10,              
                 font=("华文行楷", 20),
                 textvariable = str_obj,
                 )


#间隔时间赋值
Label_1 = tkinter.Label(root,
                 height = 1,
                 width = 20,                
                 font=("宋体", 12),
                 textvariable = span_in,
                 )

Label_4.grid(column=1, row=0,padx=0,pady=20) #运行状态
Label_1.grid(column=1, row=1,padx=0,pady=20) #间隔时间

Button_2.grid(column=1, row=2,padx=0,pady=20) #开始运行
Button_3.grid(column=1, row=3,padx=0,pady=20) #结束运行
Button_5.grid(column=1, row=4,padx=0,pady=20) #一键息屏

#程序初始化
Button_2_onCommand()

root.mainloop()

