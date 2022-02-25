# print([i for i in range(1,18-(18%8),8)])
# for y in range(1,18-(18%8),8):
# 	print(y)
# 	for i in range(8):
# 		print(y+i)
# for i in range(-2,0):
# # 	print(i)
#
# import tkinter as tk
# from tkinter import *
# from tkinter import scrolledtext
# from tkinter import ttk
# # root = tk.Tk()
# # monty = ttk.LabelFrame(root, text=' Monty Python') # 创建一个容器，其父容器为win
# # monty.grid(column=0, row=0, padx=10, pady=10)
# # scr = scrolledtext.ScrolledText(monty, width=30, height=5, wrap=tk.WORD)
# # scr.grid(column=0, columnspan=3)
# # root.mainloop()
#
# root = tk.Tk()
# root.grid()
# app = ttk.Frame(root)
# app.grid()
#
# fram1 = tk.LabelFrame(app, text='1')
# txt1 = tk.Text(fram1)
# sl1 = Scrollbar(fram1)
# sl1['command'] = txt1.yview
# # sl1.grid(row=0, column=1,sticky=S + W  )
# # txt1.grid(row=0, column=0,sticky=S + W  )
# # fram1.grid(row=0, column=0, sticky=S + W )
# sl1.grid(row=0, column=1, sticky=S + W + E + N)
# txt1.grid(row=0, column=0, sticky=S + W + E + N)
# fram1.grid(row=0, column=0, sticky=S + W + E + N)
# mainloop()


# !/usr/bin/python3
# -*- coding: utf-8 -*-
#
# import tkinter
# import threading
# import time
#
#
# class section:
# 	def onPaste(self):
# 		print("显示AI机器人一天的工作")
#
# 	def onCopy(self):
# 		print("如果要现在开始工作，就点开始，否则会根据日常的安排工作")
#
# 	def onCut(self):
# 		print("学习新的工作技术，只要教过AI一次，就会了，以后的工作都可以交给他")
#
#
# def move(event):
# 	global x, y, root
# 	new_x = (event.x - x) + root.winfo_x()
# 	new_y = (event.y - y) + root.winfo_y()
# 	s = "300x300+" + str(new_x) + "+" + str(new_y)
# 	root.geometry(s)
# 	print("当把我放到左上角200*200的区域时我会走人的,当前是x:%s,y:%s" % (new_x, new_y))
# 	if new_x < 50 and new_y < 50:
# 		exit()
#
#
# def button_1(event):
# 	global x, y
# 	x, y = event.x, event.y
# 	print("event.x, event.y = ", event.x, event.y)
#
#
# '右键菜单设置'
#
#
# def button_3(event):
# 	global menu
# 	print(event.x_root, event.y_root)
# 	menu.post(event.x_root, event.y_root)
# 	'''
# 	global root
# 	root.Menu(root.abc,tearoff=0)
# 	root.Menu.post(event.x_root, event.y_root)
# 	'''
#
#
# global x, y, root, menu
#
#
# def aiui():
# 	global root, menu
# 	root = tkinter.Tk()
# 	root.overrideredirect(True)
# 	root.wm_attributes('-topmost', 1)
# 	sw = root.winfo_screenwidth()
# 	sh = root.winfo_screenheight()
# 	root_x = sw - 300
# 	root_y = sh - 300 - 50
# 	root.attributes("-alpha", 0.4)  # 窗口透明度60 %
#
# 	root.geometry("300x300+%d+%d" % (root_x, root_y))
#
# 	canvas = tkinter.Canvas(root)
# 	canvas.configure(width=300)
# 	canvas.configure(height=300)
# 	# canvas.configure(bg = "red")
# 	canvas.configure(highlightthickness=0)
#
# 	filename = tkinter.PhotoImage(file="ai_1.gif")
# 	canvas.create_image(150, 150, image=filename)
#
# 	canvas.bind("<B1-Motion>", move)
# 	canvas.bind("<Button-1>", button_1)
# 	canvas.bind("<Button-3>", button_3)
#
# 	canvas.pack()
#
# 	section_obj = section()
# 	menu = tkinter.Menu(canvas, tearoff=0)
# 	menu.add_command(label="我的工作", command=section_obj.onCopy)
# 	menu.add_separator()
# 	menu.add_command(label="开始工作", command=section_obj.onPaste)
# 	menu.add_separator()
# 	menu.add_command(label="技能学习", command=section_obj.onCut)
# 	menu.add_separator()
# 	menu.add_command(label="退出", command=root.quit)
#
# 	root.mainloop()
#
#
# '''线程控制'''
# exitFlag = 0
#
#
# class threadControl(threading.Thread):
# 	def __init__(self, threadID, name, counter):
# 		threading.Thread.__init__(self)
# 		self.threadID = threadID
# 		self.name = name
# 		self.counter = counter
#
# 	def run(self):
# 		print("开始线程：" + self.name)
# 		if self.name == 'aiui':
# 			aiui()
# 		print_time(self.name, self.counter, 5)
# 		print("退出线程：" + self.name)
#
#
# def print_time(threadName, delay, counter):
# 	while counter:
# 		if exitFlag:
# 			threadName.exit()
# 		time.sleep(delay)
# 		print("%s: %s" % (threadName, time.ctime(time.time())))
# 		counter -= 1
#
#
# if __name__ == '__main__':
# 	thread1 = threadControl(1, 'thread_1', 1)
# 	thread2 = threadControl(2, 'thread_2', 2)
# 	aiui_obj = threadControl(3, 'aiui', 3)
#
# 	aiui_obj.start()
#
# 	thread1.start()
# 	thread2.start()
# 	thread1.join()
# 	thread2.join()
#
# 	aiui_obj.join()
# 	print("退出主线程")


# import tkinter
# from tkinter import ttk
#
#
# def xFunc1(event):
# 	print(f"鼠标左键滑动坐标是:x={event.x},y={event.y}")
#
#
# win = tkinter.Tk()
# win.title("Kahn Software v1")  # #窗口标题
# win.geometry("600x500+200+20")  # #窗口位置500后面是字母x
# '''
# 鼠标移动事件
# <B1-Motion>   鼠标左键滑动
# <B2-Motion>   鼠标滚轮移动
# <B3-Motion>   鼠标右键滑动
# '''
# xLabel = tkinter.Label(win, text="KAHN Hello world")
# xLabel.pack()
# xLabel.bind("<B1-Motion>", xFunc1)
#
# win.mainloop()  # #窗口持久化

import tkinter
from tkinter import ttk


# def xFunc1(event):
# 	print(f"鼠标左键释放坐标是:x={event.x},y={event.y}")
#
#
# win = tkinter.Tk()
# win.title("Kahn Software v1")  # #窗口标题
# win.geometry("600x500+200+20")  # #窗口位置500后面是字母x
# '''
# 鼠标释放事件
# <ButtonRelease-1>   鼠标释放左键触发（经测试，必须先点到有效区域，同时在有效区域上释放才行）
# <ButtonRelease-2>   释放鼠标滚轮
# <ButtonRelease-3>   释放鼠标右键
# # <Enter>             鼠标进入触发事件，仅一次有效。下次光标需移出有效区域再次进入时才再次触发
# # <Leave>             鼠标离开触发事件，离开那一刹那触发
# # '''
# # xLabel = tkinter.Label(win,text="tom is a boy11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",bg="black",fg="red",font=("黑体",15)
# #                     ,width=15,height=2,wraplength=100,justify="left",anchor="center")
# # xLabel.pack()
# # xLabel.bind("<ButtonRelease-1>", xFunc1)
# #
# # win.mainloop()  # #窗口持久化
# #
# #
# #
# #     msgs = (ZCAN_Transmit_Data * 8)()
# # 	for seq in range(1, 9):
# # 		msgs[seq].transmit_type = 0  # 类型，CAN
# # 		msgs[seq].frame.eff = 0  # 帧类型，扩展帧
# # 		msgs[seq].frame.rtr = 0  # 帧类型，远程帧
# # 		msgs[seq].frame.can_id = UDS_adderss
# # 		msgs[seq].frame.can_dlc = 8
# # 		for signal_seq in range(msgs[seq].frame.can_dlc):
# # 			msgs[seq].frame.data[signal_seq] = sig_TX[flag_con * 8 + seq]
# # 	device.Transmit(chn_handle, msgs, 1)
# # 	# log = "".join(hex(j).replace("0x", "").zfill(2) for j in sig_list)
# # 	# logging.critical(f" : TX : {log}")
#
#
#     for i in range(transmit_num):
#         msgs[i].transmit_type = 0 #Send Self
#         msgs[i].frame.eff     = 0 #extern frame
#         msgs[i].frame.rtr     = 0 #remote frame
#         msgs[i].frame.can_id  = i
#         msgs[i].frame.can_dlc = 8
#         for j in range(msgs[i].frame.can_dlc):
#             msgs[i].frame.data[j] = j
#
#     ret = zcanlib.Transmit(chn_handle, msgs, transmit_num)
#     print("Tranmit Num: %d." % ret)
#
#
# 	def transform_device_event_more_flash(chn_handle, sig_list, num):
# 		msgs = (ZCAN_Transmit_Data * num)()
# 		for seq in range()
# 			msgs[0].transmit_type = 0  # 类型，CAN
# 			msgs[0].frame.eff = 0  # 帧类型，扩展帧
# 			msgs[0].frame.rtr = 0  # 帧类型，远程帧
# 			msgs[0].frame.can_id = UDS_adderss
# 			msgs[0].frame.can_dlc = 8
# 			for signal_seq in range(msgs[0].frame.can_dlc):
# 				msgs[0].frame.data[signal_seq] = sig_list[signal_seq]
# 		device.Transmit(chn_handle, msgs, 1)
# 		log = "".join(hex(j).replace("0x", "").zfill(2) for j in sig_list)
# 		logging.critical(f" : TX : {log}")


print([i for i in range(-2,0)])

SIG_ESC_SecOC0_MAC_ESC_SecOC0 = 490,






