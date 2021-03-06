#coding=utf-8
#pyinstaller -F -w -i 1.ico PythonApplication1.py
import tkinter
import tkinter.filedialog
from tkinter import *
import threading
import pyautogui
import time
from ctypes import *
import configparser
import os

#保证按钮重复按下不重复执行函数
a1=0
a2=0 
a3=0

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
color=config.get('section_1','color') #倒计时颜色
off=config.get('section_1','screen')#锁屏倒计时


now = time.strftime("%H:%M:%S",time.localtime())

def loop1():
    global now
    pyautogui.press('scrolllock')
    pyautogui.press('scrolllock')
    span1=int(span)
    while span1>0 and stop_threads and (t1<now<t2 or t3<now<t4):
        now=time.strftime("%H:%M:%S",time.localtime())
        now_1.set(span1)
        span1 = span1-1       
        time.sleep(1)
def loop2():
    user32 = windll.LoadLibrary('user32.dll')
    user32.LockWorkStation()
def screenOff():
    global stop_threads,color,stop_off
    stop_threads=False
    stop_off=True
    Label_4.config(fg="red")
    span1=int(off)
    while span1>0 and stop_off:
        now_1.set(span1)
        span1 = span1-1       
        time.sleep(1)
    if stop_off:
        now_1.set("未运行")
        HWND_BROADCAST = 0xffff
        WM_SYSCOMMAND = 0x0112
        SC_MONITORPOWER = 0xF170
        MonitorPowerOff = 2
        SW_SHOW = 5
        windll.user32.PostMessageW(HWND_BROADCAST, WM_SYSCOMMAND,SC_MONITORPOWER, MonitorPowerOff)
        shell32 = windll.LoadLibrary("shell32.dll")
        shell32.ShellExecuteW(None, 'open', 'rundll32.exe','USER32', '', SW_SHOW)
    root.destroy()
def LOOP():
    global stop_threads,now,a1
    now=time.strftime("%H:%M:%S",time.localtime())
    while (t1<now<t2 or t3<now<t4) and stop_threads:
        now=time.strftime("%H:%M:%S",time.localtime())
        loop1()
    if t2<=now<t3:
       loop2()
       now_1.set("未运行")
       a1=0
def Button_2_onCommand():
    global stop_threads,stop_off,a1,a2,a3
    a2=0
    a3=0
    if a1==0:
        a1=1
        Label_4.config(fg=color)
        stop_threads=True
        stop_off=False #终止息屏
        run_thread = threading.Thread(target=LOOP)
        run_thread.setDaemon(True)
        run_thread.start()
def Button_3_onCommand():
    global stop_threads,stop_off,a1,a2,a3
    a1=0
    a3=0
    if a2==0:
        a2=1
        Label_4.config(fg=color)
        stop_threads=False
        stop_off=False
        now_1.set("未运行")    
def Button_5_onCommand():
    global a1,a2,a3
    a1=0
    a2=0
    if a3==0:
        a3=1
        off_thread = threading.Thread(target=screenOff)
        off_thread.setDaemon(True)
        off_thread.start()

root = tkinter.Tk()
root.title('小助手')
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


span_in = tkinter.StringVar()
span_in.set("间隔时间：" + span + "秒")

now_1 = tkinter.StringVar()
Label_4 = tkinter.Label(root,
                 height = 0,
                 width = 10,              
                 font=("华文彩云", 30),
                 fg=color,
                 textvariable = now_1,
                 )


#间隔时间赋值
Label_1 = tkinter.Label(root,
                 height = 0,
                 width = 15,                
                 font=("宋体", 12),
                 textvariable = span_in,
                 )

Label_4.grid(column=1, row=0,padx=0,pady=20) #倒计时
Label_1.grid(column=1, row=1,padx=0,pady=20) #间隔时间

Button_2.grid(column=1, row=2,padx=0,pady=20) #开始运行
Button_3.grid(column=1, row=3,padx=0,pady=20) #结束运行
Button_5.grid(column=1, row=4,padx=0,pady=20) #一键息屏

#程序初始化
Button_2_onCommand()

root.mainloop()


