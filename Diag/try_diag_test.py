# coding=utf-8
# @Time    : 2022/1/4
# @Author  : Yi Chen
# @comments  : --



import logging.config
from dev_operation import *
import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.filedialog
import tkinter.messagebox
import threading
import os
import datetime
from zlib import crc32
from zlgcan import *
import time


def With_Thread(f):
	def Threads(*args):
		t = threading.Thread(target=f, args=(*args,))
		t.setDaemon(True)
		t.start()
	return Threads


def patch(f):
	def wrapper(*args, **kwargs):
		f(*args, **kwargs)
		while 1:
			time.sleep(1)
			if g is None:
				break
			else:
				continue
	return wrapper




flash_file_path = [0, 0]

WIDGHT_WIDTH = 600
WIDGHT_HEIGHT = 400

UDS_adderss = 0x740
UDS_adderss_3e = 0x740

device = ZCAN()
flag_transform = False
flag_receive = False
flag_con = 0

RX = ''
sig_TX = []
len_sig_TX = 0
global_time = 0

dev_fd = {"dev_handle": "0", "chn_handle": "0"}

# flash
flag_receive_flash = False
flag_transform_flash = False


def seedToKey(seed, MASK):
	"""
	安全算法，seed为2701回复的4个字节的16进制数
	:param seed: seed为2701回复的4个字节的16进制数转化为十进制数输入
	:param MASK: 长城规定的4个字节的16进制数16进制数转化为十进制数输入
	:return: key，16进制字节，长度4个字节
	"""
	logging.debug(f" : 进入{seed}计算，MASK为{MASK}")
	key = 0
	if seed != 0:
		for i in range(35):
			if seed & 0x80000000:
				seed = seed << 1
				seed = seed ^ MASK
			else:
				seed = seed << 1
		key = seed
	sed = hex(key).replace("0x", "").zfill(8)[-8:]
	logging.debug(f" : 进入{seed}计算，MASK为{MASK}，计算结果为{sed}")
	return hex(key).replace("0x", "").zfill(8)[-8:]


class ZLG:
	def __init__(self):
		self.lock = threading.Lock()

	def open_device(self, channel_num, type_devcie=dev.get("type_devcie")):
		"""
		打开周立功设备的函数
		:param type_devcie: ZLG设备类型,可通过修改配置文件修改
		:param channel_num: 开启的设备通道号
		:return: 设备通道句柄
		"""
		global dev_fd
		handle = device.OpenDevice(type_devcie, 0, 0)
		if handle == INVALID_DEVICE_HANDLE:
			logging.critical(f" : 设备打开失败！")
			tkinter.messagebox.showwarning('警告', f'设备打开失败!')
			print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " : ", "Open Device failed!")
		else:
			logging.error(f" : 设备句柄号：{handle}！")
			info = device.GetDeviceInf(handle)
			logging.debug(f" : 设备信息：{info}！")
			if type_devcie.value == 52:
				chn_handle = can_net_start(device, handle, channel_num)
				logging.error(f" : 设备通道句柄：{chn_handle}！")
				dev_fd["dev_handle"] = handle
				dev_fd["chn_handle"] = chn_handle
				self.recive_device(dev_fd["chn_handle"])
				logging.critical(f" : 设备{type_devcie}打开成功！")
				print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " : 设备已开启！", )
				demo.device_display_lable.configure(text="设备 : 设备已开启！")
				logging.critical(f" : 设备句柄信息：{dev_fd}！")
				return handle, chn_handle
			elif type_devcie.value == 41 or 43:
				chn_handle = can_start(device, handle, channel_num)
				logging.error(f" : 设备通道句柄：{chn_handle}！")
				dev_fd["dev_handle"] = handle
				dev_fd["chn_handle"] = chn_handle
				self.recive_device(dev_fd["chn_handle"])
				logging.critical(f" : 设备{type_devcie}打开成功！")
				print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " : 设备已开启！", )
				demo.device_display_lable.configure(text="设备 : 设备已开启！")
				logging.critical(f" : 设备句柄信息：{dev_fd}！")
				return handle, chn_handle
			else:
				print(333)

	@With_Thread
	def transform_device_cycle(self, chn_handle):
		"""
		发送函数，循环报文
		:param chn_handle: 设备句柄
		:return: None
		"""
		logging.critical(f" ：开启会话保持3E80！")
		print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " TX: 开启会话保持！", )
		while not flag_transform:
			time.sleep(3)
			msgs = (ZCAN_Transmit_Data * 1)()
			msgs[0].transmit_type = 0  # 类型，CAN
			msgs[0].frame.eff = 0  # 帧类型，扩展帧
			msgs[0].frame.rtr = 0  # 帧类型，远程帧
			msgs[0].frame.can_id = UDS_adderss_3e
			msgs[0].frame.can_dlc = 8
			for signal_seq in range(msgs[0].frame.can_dlc):
				msgs[0].frame.data[signal_seq] = [2, 0x3E, 0x80, 0xcc, 0xcc, 0xcc, 0xcc, 0xcc][signal_seq]
			logging.debug(f' : 会话保持,TX : 02 3e 80 00 00 00 00 00')
			# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " TX: ", dict)
			device.Transmit(chn_handle, msgs, 1)

	@With_Thread
	def transform_device_cycle_flash(self, chn_handle):
		"""
		发送函数，循环报文
		:param chn_handle: 设备句柄
		:return: None
		"""
		logging.critical(f" ：开启会话保持3E80！")
		print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " TX: 开启会话保持！", )
		while not flag_transform_flash:
			time.sleep(3)
			msgs = (ZCAN_Transmit_Data * 1)()
			msgs[0].transmit_type = 0  # 类型，CAN
			msgs[0].frame.eff = 0  # 帧类型，扩展帧
			msgs[0].frame.rtr = 0  # 帧类型，远程帧
			msgs[0].frame.can_id = UDS_adderss_3e
			msgs[0].frame.can_dlc = 8
			for signal_seq in range(msgs[0].frame.can_dlc):
				msgs[0].frame.data[signal_seq] = [2, 0x3E, 0x80, 0xcc, 0xcc, 0xcc, 0xcc, 0xcc][signal_seq]
			logging.debug(f' : 会话保持,TX : 023e800000000000')
			# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " TX: ", dict)
			device.Transmit(chn_handle, msgs, 1)


	@staticmethod
	def transform_device_event_more(chn_handle, sig_list):
		msgs = (ZCAN_Transmit_Data * 1)()
		msgs[0].transmit_type = 0  # 类型，CAN
		msgs[0].frame.eff = 0  # 帧类型，扩展帧
		msgs[0].frame.rtr = 0  # 帧类型，远程帧
		msgs[0].frame.can_id = UDS_adderss
		msgs[0].frame.can_dlc = 8
		for signal_seq in range(msgs[0].frame.can_dlc):
			msgs[0].frame.data[signal_seq] = sig_list[signal_seq]
		device.Transmit(chn_handle, msgs, 1)
		tx_data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " TX: " + " ".join(hex(j).replace("0x", "").zfill(2) for j in sig_list) + "\n"
		log = " ".join(hex(j).replace("0x", "").zfill(2) for j in sig_list)
		logging.critical(f" : TX : {log}")
		demo.datadisplay.insert(INSERT, tx_data)
		demo.datadisplay.see('end')

	@staticmethod
	def transform_device_event_more_flash(chn_handle, sig_list):
		msgs = (ZCAN_Transmit_Data * 1)()
		msgs[0].transmit_type = 0  # 类型，CAN
		msgs[0].frame.eff = 0  # 帧类型，扩展帧
		msgs[0].frame.rtr = 0  # 帧类型，远程帧
		msgs[0].frame.can_id = UDS_adderss
		msgs[0].frame.can_dlc = 8
		for signal_seq in range(msgs[0].frame.can_dlc):
			msgs[0].frame.data[signal_seq] = sig_list[signal_seq]
		device.Transmit(chn_handle, msgs, 1)
		log = "".join(hex(j).replace("0x", "").zfill(2) for j in sig_list)
		logging.critical(f" : TX : {log}")


	@With_Thread
	def more_frams(self, chn_handle, imdata=None):
		"""
		发送函数，事件报文
		:param imdata: 多帧输入
		:param chn_handle: 设备句柄
		:return: None
		"""
		global sig_TX, len_sig_TX
		try:
			if imdata is None:
				imdata = demo.datainput_text.get("1.0", END)
				logging.error(f" : 面板输入 : {imdata}")
			else:
				imdata = imdata
				logging.error(f" : 非面板输入 : {imdata}")
			length = int((len(imdata))/2)
			logging.debug(f" : 输入数据长度 : {length}")
			if length > 7:
				sig = []
				x = 0
				for i in range(length):
					sig.append(int(imdata[x:x + 2], 16))
					x += 2
				sig_TX.append([int("1"+hex(length).replace("0x", "").zfill(3)[0], 16), int(hex(length).replace("0x", "").zfill(3)[1:], 16)] + sig[0:6])
				m = length - 6
				if m <= 105:
					y = 6
					for i in range(15):
						if m >= 7:
							sig_TX.append([int("2"+hex(i+1).replace("0x", ""), 16)] + sig[y:y+7])
							y += 7
							m -= 7
						elif 7 > m > 0:
							sig_TX.append([int("2"+hex(i+1).replace("0x", ""), 16)] + sig[y:y+m] + [0xcc]*(7-m))
							y += 7
							m -= 7
						else:
							break
				elif m > 105:
					y = 6
					for i in range(15):
						if m >= 7:
							sig_TX.append([int("2" + hex(i + 1).replace("0x", ""), 16)] + sig[y:y + 7])
							y += 7
							m -= 7
					while m >= 0:
						for i in range(16):
							if m >= 7:
								sig_TX.append([int("2" + hex(i).replace("0x", ""), 16)] + sig[y:y + 7])
								y += 7
								m -= 7
							elif 7 > m > 0:
								sig_TX.append([int("2" + hex(i).replace("0x", ""), 16)] + sig[y:y + m] + [0xcc]*(7-m))
								y += 7
								m -= 7
							else:
								break
				logging.critical(f" : 发送序列：{sig_TX}")
				len_sig_TX = len(sig_TX)
				self.transform_device_event_more(chn_handle, sig_TX[0])
				logging.error(f" : 多帧首帧发送完成")
			else:
				sig_list = [0xcc]*8
				sig_list[0] = length
				x = 0
				for i in range(sig_list[0]):
					sig_list[i+1] = int(imdata[x:x+2], 16)
					x += 2
				self.transform_device_event_more(chn_handle, sig_list)
				logging.error(f" : 单帧发送完成 : {sig_list}")
		except Exception as e:
			tkinter.messagebox.showwarning('警告', f'发送异常：{e}!')
			print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" 异常：{e}！")

	@With_Thread
	def more_frams_flash(self, chn_handle, imdata=None):
		"""
		发送函数，事件报文
		:param imdata: 多帧输入
		:param chn_handle: 设备句柄
		:return: None
		"""
		global sig_TX, len_sig_TX
		try:
			if imdata is None:
				imdata = demo.datainput_text.get("1.0", END)
				logging.error(f" : 面板输入 : {imdata}")
			else:
				imdata = imdata
				logging.error(f" : 非面板输入 : {imdata}")
			length = int((len(imdata)) / 2)
			logging.debug(f" : 输入数据长度 : {length}")
			if length > 7:
				sig = []
				x = 0
				for i in range(length):
					sig.append(int(imdata[x:x + 2], 16))
					x += 2
				sig_TX.append([int("1" + hex(length).replace("0x", "").zfill(3)[0], 16),
							   int(hex(length).replace("0x", "").zfill(3)[1:], 16)] + sig[0:6])
				m = length - 6
				if m <= 105:
					y = 6
					for i in range(15):
						if m >= 7:
							sig_TX.append([int("2" + hex(i + 1).replace("0x", ""), 16)] + sig[y:y + 7])
							y += 7
							m -= 7
						elif 7 > m > 0:
							sig_TX.append(
								[int("2" + hex(i + 1).replace("0x", ""), 16)] + sig[y:y + m] + [0xcc] * (7 - m))
							y += 7
							m -= 7
						else:
							break
				elif m > 105:
					y = 6
					for i in range(15):
						if m >= 7:
							sig_TX.append([int("2" + hex(i + 1).replace("0x", ""), 16)] + sig[y:y + 7])
							y += 7
							m -= 7
					while m >= 0:
						for i in range(16):
							if m >= 7:
								sig_TX.append([int("2" + hex(i).replace("0x", ""), 16)] + sig[y:y + 7])
								y += 7
								m -= 7
							elif 7 > m > 0:
								sig_TX.append(
									[int("2" + hex(i).replace("0x", ""), 16)] + sig[y:y + m] + [0xcc] * (7 - m))
								y += 7
								m -= 7
							else:
								break
				logging.critical(f" : 发送序列：{sig_TX}")
				len_sig_TX = len(sig_TX)
				self.transform_device_event_more_flash(chn_handle, sig_TX[0])
				logging.error(f" : 多帧首帧发送完成")
			else:
				sig_list = [0xcc] * 8
				sig_list[0] = length
				x = 0
				for i in range(sig_list[0]):
					sig_list[i + 1] = int(imdata[x:x + 2], 16)
					x += 2
				self.transform_device_event_more_flash(chn_handle, sig_list)
				logging.error(f" : 单帧发送完成 : {sig_list}")
		except Exception as e:
			tkinter.messagebox.showwarning('警告', f'发送异常：{e}!')
			print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" 异常：{e}！")

	@With_Thread
	def transform_device_event_sec(self, chn_handle, sig_dict=None):
		"""
		发送函数，事件报文
		:param sig_dict:
		:param chn_handle: 设备句柄
		:return: None
		"""
		logging.error(f" : 进入安全访问")
		if sig_dict is None:
			sig_dict = [2, 0x27, 1, 0xcc, 0xcc, 0xcc, 0xcc, 0xcc]
		msgs = (ZCAN_Transmit_Data * 1)()
		msgs[0].transmit_type = 0  # 类型，CAN
		msgs[0].frame.eff = 0  # 帧类型，扩展帧
		msgs[0].frame.rtr = 0  # 帧类型，远程帧
		msgs[0].frame.can_id = UDS_adderss
		msgs[0].frame.can_dlc = 8
		for signal_seq in range(msgs[0].frame.can_dlc):
			msgs[0].frame.data[signal_seq] = sig_dict[signal_seq]
		tx_data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " TX: " + " ".join(hex(j).replace("0x", "").zfill(2) for j in sig_dict) + "\n"
		log = " ".join(hex(j).replace("0x", "").zfill(2) for j in sig_dict)
		logging.critical(f" : TX : {log}")
		demo.datadisplay.insert(INSERT, tx_data)
		demo.datadisplay.see('end')
		device.Transmit(chn_handle, msgs, 1)

	@With_Thread
	def transform_device_event_sec_flash(self, chn_handle, sig_dict=None):
		"""
		发送函数，事件报文
		:param sig_dict:
		:param chn_handle: 设备句柄
		:return: None
		"""
		logging.error(f" : 进入安全访问")
		if sig_dict is None:
			sig_dict = [2, 0x27, 1, 0xcc, 0xcc, 0xcc, 0xcc, 0xcc]
		msgs = (ZCAN_Transmit_Data * 1)()
		msgs[0].transmit_type = 0  # 类型，CAN
		msgs[0].frame.eff = 0  # 帧类型，扩展帧
		msgs[0].frame.rtr = 0  # 帧类型，远程帧
		msgs[0].frame.can_id = UDS_adderss
		msgs[0].frame.can_dlc = 8
		for signal_seq in range(msgs[0].frame.can_dlc):
			msgs[0].frame.data[signal_seq] = sig_dict[signal_seq]
		log = "".join(hex(j).replace("0x", "").zfill(2) for j in sig_dict)
		logging.critical(f" : TX : {log}")
		device.Transmit(chn_handle, msgs, 1)


	@With_Thread
	def recive_device(self, chn_handle):
		"""
		:param chn_handle: 设备句柄
		:return: 无返回值
		"""
		global g, RX, flag_con, sig_TX, len_sig_TX
		try:
			while not flag_receive:
				rcv_num = device.GetReceiveNum(chn_handle, ZCAN_TYPE_CAN)
				if rcv_num:
					# print("Receive CAN message number:%d" % rcv_num)
					rcv_msg, rcv_num = device.Receive(chn_handle, rcv_num)
					rcv_can_data = []
					for i in range(rcv_num):
						# 二进制报文
						# rcv_can_data.append(dict(
						# 	{"No.": i, "timestamp": rcv_msg[i].timestamp, "can_id": rcv_msg[i].frame.can_id,
						# 	 "len": rcv_msg[i].frame.can_dlc,
						# 	 "eff": rcv_msg[i].frame.eff, "rtr": rcv_msg[i].frame.rtr,
						# 	 "data": ''.join(bin(rcv_msg[i].frame.data[j]).replace("0b", "").zfill(8) + '' for j in
						# 					 range(rcv_msg[i].frame.can_dlc))}))
						# 整数报文
						rcv_can_data.append(dict(
							{"No.": i,
							 "timestamp": rcv_msg[i].timestamp,
							 "can_id": rcv_msg[i].frame.can_id,
							 "len": rcv_msg[i].frame.can_dlc,
							 "eff": rcv_msg[i].frame.eff,
							 "rtr": rcv_msg[i].frame.rtr,
							 "data": [rcv_msg[i].frame.data[j] for j in range(rcv_msg[i].frame.can_dlc)]}))
					# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())," ：RX 信号 ：",[i for i in rcv_msg[0].frame.data])
					for i in range(rcv_num):
						if rcv_can_data[i]["can_id"] == 1864:
							ret_sig = ''.join(hex(j).replace("0x", "").zfill(2) for j in rcv_can_data[i]["data"])
							RX = ret_sig
							ret_sig_disp = ' '.join(hex(j).replace("0x", "").zfill(2) for j in rcv_can_data[i]["data"])
							rx_data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " RX: " + ret_sig_disp + "\n\n"
							logging.critical(f" : RX : {ret_sig_disp}")
							demo.datadisplay.insert(INSERT, rx_data)
							demo.datadisplay.see('end')
							if ret_sig[0] == "3":
								logging.critical(f" ：收到多帧传输的流控帧！FS为0x{ret_sig[1]}，BS为0x{ret_sig[2:4]}，STim为0x{ret_sig[4:6]}")
								print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" ：收到多帧传输的流控帧！FS为0x{ret_sig[1]}，BS为0x{ret_sig[2:4]}，STim为0x{ret_sig[4:6]}")
								if len_sig_TX - 1 > 8:
									for seq in range(1, 9):
										time.sleep(0.01)
										self.transform_device_event_more(dev_fd["chn_handle"], sig_TX[flag_con*8+seq])
									flag_con += 1
									len_sig_TX -= 8
								elif 0 < len_sig_TX - 1 <= 8:
									for seq in range(-(len_sig_TX-1), 0):
										time.sleep(0.01)
										self.transform_device_event_more(dev_fd["chn_handle"], sig_TX[seq])
									flag_con = 0
									sig_TX = []
								else:
									pass
							elif ret_sig[:6] == "066701":
								ret = seedToKey(int(ret_sig[6:14], 16), 0x20695467)
								time.sleep(0.1)
								demo.transform_device_event_sec(dev_fd["chn_handle"], [6, 0x27, 2, int(ret[:2], 16), int(ret[2:4], 16), int(ret[4:6], 16), int(ret[6:8], 16), 0xcc])
							elif ret_sig[:6] == "026702":
								logging.critical(f" : 普通安全访问通过！")
								print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " ：普通安全访问通过！")
							elif ret_sig[:6] == "066735":
								ret = seedToKey(int(ret_sig[6:14], 16), 0x35695467)
								time.sleep(0.1)
								demo.transform_device_event_sec(dev_fd["chn_handle"], [6, 0x27, 0x36, int(ret[:2], 16), int(ret[2:4], 16), int(ret[4:6], 16), int(ret[6:8], 16), 0xcc])
							elif ret_sig[:6] == "026736":
								logging.critical(f" : 刷写安全访问通过！")
								print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " ：刷写安全访问通过！")
							elif ret_sig[0] == "1":
								logging.critical(f" : 收到多帧传输的首帧！FF_DL为0x{ret_sig[1:4]}")
								print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" ：收到多帧传输的首帧！FF_DL为0x{ret_sig[1:4]}")
								demo.transform_device_event_sec(dev_fd["chn_handle"], [48, 0, 20, 0xcc, 0xcc, 0xcc, 0xcc, 0xcc])
							else:
								pass
				else:
					pass
		except Exception as e:
			tkinter.messagebox.showwarning('警告', f'接收异常：{e}!')
			print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" 数据接收异常：{e}！")
			logging.critical(f" : 数据接收异常 : {e}")

	@staticmethod
	def stop_thread():
		"""
		停止ECU动作的函数
		:return: None
		"""
		global flag_receive, flag_transform
		flag_receive = True
		flag_transform = True
		# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " : ", "修改标志位！！！")
		time.sleep(1)
		flag_receive = False
		flag_transform = False

	@staticmethod
	def stop_thread_flash():
		"""
		停止ECU动作的函数
		:return: None
		"""
		global flag_receive_flash, flag_transform_flash
		flag_receive_flash = True
		flag_transform_flash = True
		time.sleep(1)
		flag_receive_flash = False
		flag_transform_flash = False

	@With_Thread
	def close_device(self, handle, chn_handle):
		self.stop_thread()
		# Close CAN
		device.ResetCAN(chn_handle)
		# Close Device
		device.CloseDevice(handle)
		demo.device_display_lable.configure(text="设备 : 设备已关闭！")
		logging.critical(f" : 设备关闭完成")

	@staticmethod
	def deal_flash(ser_req, length, ser_pos):
		while True:
			logging.critical("检测循环！")
			time.sleep(0.03)
			if RX == "" or RX[2:8] == "7f"+ser_req[:2]+"78":
				continue
			elif RX[2:length+2] == ser_pos:
				logging.critical(f" {ser_req} 成功！返回值：{RX}")
				print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" {ser_req} 成功！返回值：{RX}")
				return [0, RX]
			elif RX[2:6] == "7f"+ser_req[:2] and RX[6:8] != "78":
				logging.critical(f" {ser_req} 失败！返回值：{RX}")
				print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" {ser_req} 失败！返回值：{RX}")
				return [255, RX]
			else:
				continue

	@staticmethod
	def deal_flash_31_router(ser_req, length, ser_pos):
		while True:
			if RX == "" or RX[2:8] == "7f"+ser_req[:2]+"78":
				continue
			elif RX[2:length] == ser_pos:
				if RX[2:(length+2)][-2:] == "00":
					logging.critical(f" {ser_req} 成功！返回值：{RX}")
					print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" {ser_req} 成功！返回值：{RX}")
					return [0, RX]
				elif RX[2:(length+2)][-2:] == "01":
					logging.critical(f" {ser_req} 失败！返回值：{RX}")
					print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" {ser_req} 失败！返回值：{RX}")
					return [255, RX]
			elif RX[2:6] == "7f"+ser_req[:2] and RX[6:8] != "78":
				logging.critical(f" {ser_req} 失败！返回值：{RX}")
				print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" {ser_req} 失败！返回值：{RX}")
				return [255, RX]
			else:
				continue

	@With_Thread
	def recive_device_flash(self, chn_handle):
		"""
		:param chn_handle: 设备句柄
		:return: 无返回值
		"""
		global g, RX, flag_con, sig_TX, len_sig_TX, global_time
		try:
			while not flag_receive_flash:
				rcv_num = device.GetReceiveNum(chn_handle, ZCAN_TYPE_CAN)
				if rcv_num:
					rcv_msg, rcv_num = device.Receive(chn_handle, rcv_num)
					rcv_can_data = []
					for i in range(rcv_num):
						rcv_can_data.append(dict(
							{"No.": i,
							 "timestamp": rcv_msg[i].timestamp,
							 "can_id": rcv_msg[i].frame.can_id,
							 "len": rcv_msg[i].frame.can_dlc,
							 "eff": rcv_msg[i].frame.eff,
							 "rtr": rcv_msg[i].frame.rtr,
							 "data": [rcv_msg[i].frame.data[j] for j in range(rcv_msg[i].frame.can_dlc)]}))
					# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())," ：RX 信号 ：",[i for i in rcv_msg[0].frame.data])
					for i in range(rcv_num):
						if rcv_can_data[i]["can_id"] == 1864:
							ret_sig = ''.join(hex(j).replace("0x", "").zfill(2) for j in rcv_can_data[i]["data"])
							RX = ret_sig
							logging.critical(f" : RX : {RX}")
							if ret_sig[0] == "3":
								logging.critical(f" ：收到多帧传输的流控帧！FS为0x{ret_sig[1]}，BS为0x{ret_sig[2:4]}，STim为0x{ret_sig[4:6]}")
								if len_sig_TX - 1 > 8:
									# msgs = (ZCAN_Transmit_Data * 8)()
									# for seq_num in range(8):
									# 	for seq in range(1, 9):
									# 		msgs[seq_num].transmit_type = 0  # 类型，CAN
									# 		msgs[seq_num].frame.eff = 0  # 帧类型，扩展帧
									# 		msgs[seq_num].frame.rtr = 0  # 帧类型，远程帧
									# 		msgs[seq_num].frame.can_id = UDS_adderss
									# 		msgs[seq_num].frame.can_dlc = 8
									# 		for signal_seq in range(msgs[seq_num].frame.can_dlc):
									# 			msgs[seq_num].frame.data[signal_seq] = sig_TX[flag_con * 8 + seq][signal_seq]
									# ret = device.Transmit(chn_handle, msgs, 8)
									# print(444, f"{ret}")
									for seq in range(1, 9):
										time.sleep(global_time)
										self.transform_device_event_more_flash(dev_fd["chn_handle"], sig_TX[flag_con * 8 + seq])
									flag_con += 1
									len_sig_TX -= 8
								elif 0 < len_sig_TX - 1 <= 8:
									# msgs = (ZCAN_Transmit_Data * (len_sig_TX - 1))()
									# for seq_num in range(len_sig_TX - 1):
									# 	for seq in range(-(len_sig_TX - 1), 0):
									# 		msgs[seq_num].transmit_type = 0  # 类型，CAN
									# 		msgs[seq_num].frame.eff = 0  # 帧类型，扩展帧
									# 		msgs[seq_num].frame.rtr = 0  # 帧类型，远程帧
									# 		msgs[seq_num].frame.can_id = UDS_adderss
									# 		msgs[seq_num].frame.can_dlc = 8
									# 		for signal_seq in range(msgs[seq].frame.can_dlc):
									# 			msgs[seq_num].frame.data[signal_seq] = sig_TX[seq][signal_seq]
									# ret = device.Transmit(chn_handle, msgs, 1)
									# print(333, f"{ret}")
									for seq in range(-(len_sig_TX - 1), 0):
										time.sleep(global_time)
										self.transform_device_event_more_flash(dev_fd["chn_handle"], sig_TX[seq])
									flag_con = 0
									sig_TX = []
								else:
									pass
							elif ret_sig[:6] == "066701":
								ret = seedToKey(int(ret_sig[6:14], 16), 0x20695467)
								demo.transform_device_event_sec_flash(dev_fd["chn_handle"], [6, 0x27, 2, int(ret[:2], 16), int(ret[2:4], 16), int(ret[4:6], 16), int(ret[6:8], 16), 0xcc])
							elif ret_sig[:6] == "026702":
								logging.critical(f" : 普通安全访问通过！")
							elif ret_sig[:6] == "066735":
								ret = seedToKey(int(ret_sig[6:14], 16), 0x35695467)
								demo.transform_device_event_sec_flash(dev_fd["chn_handle"], [6, 0x27, 0x36, int(ret[:2], 16), int(ret[2:4], 16), int(ret[4:6], 16), int(ret[6:8], 16), 0xcc])
							elif ret_sig[:6] == "026736":
								logging.critical(f" : 刷写安全访问通过！")
							elif ret_sig[0] == "1":
								logging.critical(f" : 收到多帧传输的首帧！FF_DL为0x{ret_sig[1:4]}")
								demo.transform_device_event_sec_flash(dev_fd["chn_handle"], [48, 0, 20, 0xcc, 0xcc, 0xcc, 0xcc, 0xcc])
							else:
								pass
				else:
					pass
		except Exception as e:
			tkinter.messagebox.showwarning('警告', f'接收异常：{e}!')
			logging.critical(f" : 数据接收异常 : {e}")

	@With_Thread
	def can_flash(self, path):
		try:
			logging.critical(f" : 刷写开始！")
			global RX, UDS_adderss, UDS_adderss_3e, flag_con, sig_TX, len_sig_TX, global_time

			# 初始化
			flag_con = 0
			RX = ''
			sig_TX = []
			len_sig_TX = 0

			# 停止普通接收线程
			self.stop_thread()

			# 启动刷写接收线程
			self.recive_device_flash(dev_fd["chn_handle"])
			global_time = 0.01

			# 预编程阶段
			UDS_adderss = 0x760
			UDS_adderss_3e = 0x760
			# 功能寻址：1003
			self.more_frams_flash(dev_fd["chn_handle"], "1083")
			logging.critical(f" ： 扩展会话!")
			print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" ： 进入扩展会话！")
			demo.process_display['value'] = 2

			# 功能寻址：3E80
			self.transform_device_cycle_flash(dev_fd["chn_handle"])
			print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" ： 开启会话保持")
			demo.process_display['value'] = 4

			UDS_adderss = 0x740
			# 物理寻址：安全访问
			self.transform_device_event_sec_flash(dev_fd["chn_handle"])
			ret = self.deal_flash("2701", 4, "6702")
			if ret[0] == 255:
				return 255
			demo.process_display['value'] = 6

			# 物理寻址：编程检查
			self.more_frams_flash(dev_fd["chn_handle"], "3101fd02")
			ret=self.deal_flash_31_router("31", 10, "7101fd02")
			if ret[0] == 255:
				return 255
			demo.process_display['value'] = 8

			UDS_adderss = 0x760
			# 功能寻址：关闭DTC
			self.more_frams_flash(dev_fd["chn_handle"], "8582")
			logging.critical(f" ： 关闭DTC")
			print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" ： 关闭DTC")
			demo.process_display['value'] = 10

			# 功能寻址：关闭通讯
			self.more_frams_flash(dev_fd["chn_handle"], "288301")
			logging.critical(f" ： 关闭通讯")
			print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" ： 关闭通讯")
			demo.process_display['value'] = 12

			UDS_adderss = 0x740
			# 物理寻址：1002
			self.more_frams_flash(dev_fd["chn_handle"], "1002")
			ret=self.deal_flash("1002", 4, "5002")
			if ret[0] == 255:
				return 255
			demo.process_display['value'] = 14

			global_time = 0

			# 物理寻址：2735
			self.transform_device_event_sec_flash(dev_fd["chn_handle"], [2, 0x27, 0x35, 0xcc, 0xcc, 0xcc, 0xcc, 0xcc])
			ret=self.deal_flash("2735", 4, "6736")
			if ret[0] == 255:
				return 255
			demo.process_display['value'] = 16

			# 编程阶段
			# falsh driver download
			with open(str(flash_file_path[1]), "rb") as f:
				file_size = os.path.getsize(str(flash_file_path[1]))
				logging.critical(f" 加载flash_driver : falsh driver 文件大小为{os.path.getsize(str(flash_file_path[1]))}！")
				print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f"  : 加载 falsh driver 文件大小为{os.path.getsize(str(flash_file_path[1]))}！")

				# 物理寻址：34,请求下载
				self.more_frams_flash(dev_fd["chn_handle"], "34004408002000" + hex(file_size).replace("0x", "").zfill(8))
				ret = self.deal_flash("340044", 2, "74")
				if ret[0] == 255:
					return 255
				demo.process_display['value'] = 18

				# 物理寻址：36
				for seq in range(1, 256):
					seq_hex = hex(seq).replace("0x", "").zfill(2)
					x = f.read(1024)
					file_size -= 1024
					logging.critical(f" : flash_driver剩余大小为{file_size}")
					if file_size <= -1024:
						logging.critical(f" 36 step RX: flash_driver软件上传完成,序号：{seq}！")
						print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" 36 step RX: flash_driver软件上传完成,序号：{seq}！")
						break
					else:
						self.more_frams_flash(dev_fd["chn_handle"], "36" + seq_hex + x.hex())
						ret=self.deal_flash("36" + seq_hex, 4, "76" + seq_hex)
						if ret[0] == 255:
							return 255
				while file_size > 0:
					logging.critical(f" 36 step RX: flash_driver软件Bloack 1 上传完成,序号：{seq}！")
					print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" 36 step RX: flash_driver软件Bloack 1 上传完成,序号：{seq}！")
					for seq in range(0, 256):
						seq_hex = hex(seq).replace("0x", "").zfill(2)
						x = f.read(1024)
						file_size -= 1024
						if file_size <= -1024:
							logging.critical(f" 36 step RX: flash_driver软件上传完成,序号：{seq}！")
							print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" 36 step RX: flash_driver软件上传完成,序号：{seq}！")
							break
						else:
							self.more_frams_flash(dev_fd["chn_handle"], "36" + seq_hex + x.hex())
							ret=self.deal_flash("36" + seq_hex, 4, "76" + seq_hex)
							if ret[0] == 255:
								return 255
			demo.process_display['value'] = 38

			# 物理寻址：37
			self.more_frams_flash(dev_fd["chn_handle"], "37")
			ret = self.deal_flash("37", 2, "77")
			if ret[0] == 255:
				return 255
			demo.process_display['value'] = 40

			# 物理寻址：3101FD03,XXXXXXXXCRC32计算结果
			with open(str(flash_file_path[1]), "rb") as f:
				self.more_frams_flash(dev_fd["chn_handle"], "3101fd03" + hex(crc32(f.read())).replace("0x", "").zfill(8))
				ret=self.deal_flash_31_router("3101fd03", 10, "7101fd03")
				if ret[0] == 255:
					return 255
				demo.process_display['value'] = 42

			# 物理寻址：2EF1F0+Tester_Id,此处设置虚拟诊断仪ID（10 Btye）:31313131313131313131,4s:32323232323232323232
			# 写入时间计算：
			str_time = datetime.datetime.now()
			self.more_frams_flash(dev_fd["chn_handle"], "2ef1f0"+"31313131313131313131"+
							hex(str_time.year-2000).replace("0x", "").zfill(2) +
							hex(str_time.month).replace("0x", "").zfill(2) +
							hex(str_time.day).replace("0x", "").zfill(2) +
							hex(str_time.hour).replace("0x", "").zfill(2) +
							hex(str_time.minute).replace("0x", "").zfill(2) +
							hex(str_time.second).replace("0x", "").zfill(2) + "32323232323232323232")
			ret=self.deal_flash("2efaf0", 6, "6ef1f0")
			if ret[0] == 255:
				return 255
			demo.process_display['value'] = 44

			# 编程阶段
			# APP应用
			# flash app
			with open(str(flash_file_path[0]), "rb") as f:
				file_size = os.path.getsize(str(flash_file_path[0]))
				logging.critical(f" 36 step : app 文件大小为{os.path.getsize(str(flash_file_path[0]))}！")
				print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" 36 step : app 文件大小为{os.path.getsize(str(flash_file_path[0]))}！")

				# 物理寻址：3101fd0044xxxxxxxxyyyyyyyy,擦除flash memory
				self.more_frams_flash(dev_fd["chn_handle"], "3101fd004410018000"+hex(file_size).replace("0x", "").zfill(8))
				ret=self.deal_flash_31_router("3101fd00", 10, "7101fd00")
				if ret[0] == 255:
					return 255
				demo.process_display['value'] = 46

				# 物理寻址：34
				self.more_frams_flash(dev_fd["chn_handle"], "34004410018000"+hex(file_size).replace("0x", "").zfill(8))
				ret = self.deal_flash("340044", 2, "74")
				if ret[0] == 255:
					return 255
				demo.process_display['value'] = 48

				# 物理寻址：36
				for seq in range(1, 256):
					seq_hex = hex(seq).replace("0x", "").zfill(2)
					x = f.read(1024)
					file_size -= 1024
					logging.critical(f" : APP剩余大小为{file_size}")
					if file_size <= -1024:
						logging.critical(f" 36 step RX: app软件上传完成,序号：{seq}！")
						print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" 36 step RX: app软件上传完成,序号：{seq}！")
						break
					else:
						self.more_frams_flash(dev_fd["chn_handle"], "36" + seq_hex + x.hex())
						ret=self.deal_flash("36" + seq_hex, 4, "76" + seq_hex)
						if ret[0] == 255:
							return 255
				while file_size > 0:
					logging.critical(f" 36 step RX: app软件Bloack 1 上传完成,序号：{seq},文件剩余大小为{file_size}！")
					print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" 36 step RX: app软件Bloack 1 上传完成,序号：{seq}！")
					for seq in range(0, 256):
						seq_hex = hex(seq).replace("0x", "").zfill(2)
						x = f.read(1024)
						file_size -= 1024
						if file_size <= -1024:
							logging.critical(f" 36 step RX: app软件上传完成,序号：{seq}！")
							print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" 36 step RX: app软件上传完成,序号：{seq}！")
							break
						else:
							self.more_frams_flash(dev_fd["chn_handle"], "36" + seq_hex + x.hex())
							ret=self.deal_flash("36" + seq_hex, 4, "76" + seq_hex)
							if ret[0] == 255:
								return 255
			demo.process_display['value'] = 88

			# 物理寻址：37
			self.more_frams_flash(dev_fd["chn_handle"], "37")
			ret=self.deal_flash("37", 2, "77")
			if ret[0] == 255:
				return 255
			demo.process_display['value'] = 90

			# 物理寻址：3101FD04,zzzzzzzzCRC32计算结果
			with open(str(flash_file_path[0]), "rb") as f:
				self.more_frams_flash(dev_fd["chn_handle"], "3101fd044410018000"+hex(file_size).replace("0x", "").zfill(8)+hex(crc32(f.read())).replace("0x", "").zfill(8))
				ret=self.deal_flash_31_router("3101fd0444", 10, "7101fd04")
				if ret[0] == 255:
					return 255
				demo.process_display['value'] = 92

			# 升级阶段
			self.more_frams_flash(dev_fd["chn_handle"], "3101fd01")
			ret = self.deal_flash_31_router("3101fd01", 10, "7101fd01")
			if ret[0] == 255:
				return 255
			demo.process_display['value'] = 94
			# 重启阶段
			self.more_frams_flash(dev_fd["chn_handle"], "1181")
			logging.critical(f" : 刷写完成，系统重启！")
			print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" 刷写完成，等待重启！")
			demo.process_display['value'] = 100

			# 重置
			self.stop_thread_flash()

			tkinter.messagebox.showwarning('提示', f'刷写完成，等待重启!')
		except Exception as e:
			tkinter.messagebox.showwarning('警告', f'刷写异常：{e}!')
			logging.critical(f" : 异常 : {e}")
			print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), f" : 异常 : {e}")


# GUI
class GUI(tk.Tk, ZLG):
	def __init__(self):
		super().__init__()
		logging.config.fileConfig('log_set.ini')
		self.title("ETC诊断工具@yc")
		self.resizable(False, False)
		self.geometry(str(WIDGHT_WIDTH) + "x" + str(WIDGHT_HEIGHT) + '+200+25')
		self.WidgetsInit()

	def WidgetsInit(self):
		self._First_frame = tk.Frame(self)
		self._First_frame.grid(row=1, column=1, padx=2, pady=2, sticky=tk.NSEW)

		self._Second_datainput = tk.LabelFrame(self._First_frame, height=275, width=200, text="诊断命令")
		self._Second_datainput.grid_propagate(0)
		self._Second_datainput.grid(row=0, column=0, padx=2, pady=2, sticky=tk.NE)
		self._Third_datainput_WidgetsInit()

		self._Second_dataprint = tk.LabelFrame(self._First_frame, height=275, width=387.5, text="诊断结果")
		self._Second_dataprint.grid_propagate(0)
		self._Second_dataprint.grid(row=0, column=1, padx=2, pady=2, sticky=tk.NE)
		self._Third_dataprint_WidgetsInit()

		self._Second_dataflash = tk.LabelFrame(self._First_frame, height=110, width=590.5, text="诊断刷写-TBC")
		self._Second_dataflash.grid_propagate(0)
		self._Second_dataflash.grid(row=1, column=0, columnspan=2, padx=2, pady=2, sticky=tk.NW)
		self._Third_dataflash_WidgetsInit()

	def _Third_datainput_WidgetsInit(self):
		self.device_open_button = tk.Button(self._Second_datainput, bg="green", width=2, text='打开',
												   command=lambda: self.open_device(0))
		self.device_open_button.grid(row=0, column=0, padx=5, pady=2.5, sticky=tk.E + tk.W)

		self.device_close_button = tk.Button(self._Second_datainput, bg="red", width=5, text='关闭',
											   command=lambda: self.close_device(dev_fd["dev_handle"], dev_fd["chn_handle"]))
		self.device_close_button.grid(row=0, column=1, padx=4, pady=2.5, sticky=tk.E + tk.W)

		self.Diag_set_Radiobutton_v = IntVar()
		self.Diag_set_Phy_button = tk.Radiobutton(self._Second_datainput, value=0, variable=self.Diag_set_Radiobutton_v,
												  text="物理寻址", command=self.Diag_Set_Setting)
		self.Diag_set_Phy_button.grid(row=1, column=0, padx=2, pady=1, sticky=tk.NW)
		self.Diag_set_Fun_button = tk.Radiobutton(self._Second_datainput, value=1, variable=self.Diag_set_Radiobutton_v,
												  text="功能寻址", command=self.Diag_Set_Setting)
		self.Diag_set_Fun_button.grid(row=1, column=1, padx=2, pady=1, sticky=tk.NW)

		self.datainput_text = tk.Text(self._Second_datainput, bd=3, height=3, width=10)
		self.datainput_text.grid(row=2, column=0, rowspan=2, padx=5)
		self.datainput_text.bind("<B1-Motion>", self.select_conut)
		self.trans_button = tk.Button(self._Second_datainput, width=6, text='发送',
											 command=lambda: self.more_frams(dev_fd["chn_handle"]))
		self.trans_button.grid(row=2, column=1, padx=2, pady=1, sticky=tk.E + tk.W)
		self.clear_button = tk.Button(self._Second_datainput, width=6, text='清空', command=self.data_delete)
		self.clear_button.grid(row=3, column=1, padx=2, pady=1, sticky=tk.E + tk.W)

		self.diag_secuity_button = tk.Button(self._Second_datainput, width=4, text='安全访问',
												command=lambda: self.transform_device_event_sec(dev_fd["chn_handle"]))
		self.diag_secuity_button.grid(row=4, column=0, padx=2, pady=2.5, sticky=tk.E + tk.W)

		self.diag_con_button = tk.Button(self._Second_datainput, width=4, text='会话保持',
												command=lambda: self.transform_device_cycle(dev_fd["chn_handle"]))
		self.diag_con_button.grid(row=4, column=1, padx=2, pady=2.5, sticky=tk.E + tk.W)

		self.device_display_lable = tk.Label(self._Second_datainput, text="设备:", justify="left", anchor="w")
		self.device_display_lable.grid(row=5, column=0, columnspan=2, padx=1.5, pady=2.5, sticky=tk.EW)

		self.len_display_lable = tk.Label(self._Second_datainput, text="长度:", justify="left", anchor="w")
		self.len_display_lable.grid(row=6, column=0, columnspan=2, padx=1.5, pady=2.5, sticky=tk.EW)

	def _Third_dataprint_WidgetsInit(self):
		self.scroll = tkinter.Scrollbar(self._Second_dataprint)
		self.scroll.grid(row=0, column=1, sticky=S + W + E + N)
		self.datadisplay = tk.Text(self._Second_dataprint, yscrollcommand=self.scroll.set, bd=3, height=18, width=50)
		self.datadisplay.grid(row=0, column=0)
		self.scroll['command'] = self.datadisplay.yview

	def _Third_dataflash_WidgetsInit(self):
		self.path = StringVar()
		tk.Label(self._Second_dataflash, text='镜像路径:').grid(row=0, column=0, padx=5, pady=2.5)
		self.file_path = tk.Entry(self._Second_dataflash, textvariable=self.path, width=34)
		self.file_path.grid(row=0, column=1, padx=5, pady=5)
		tk.Button(self._Second_dataflash, text='文件选择', command=self.data_file_path).grid(row=0, column=2, padx=5,
																						 pady=5)
		tk.Label(self._Second_dataflash, text='刷写进度:').grid(row=1, column=0, padx=5, pady=2.5, sticky=tk.E + tk.W)
		self.process_display = ttk.Progressbar(self._Second_dataflash, maximum=100, value=0, length=245,
											   mode='determinate')
		self.process_display.grid(row=1, column=1, padx=5, pady=2.5)
		tk.Button(self._Second_dataflash, text='直连刷写', command=lambda: self.can_flash(flash_file_path)).grid(row=1, column=2, padx=5, pady=5)

	def Diag_Set_Setting(self):
		global UDS_adderss, UDS_adderss_3e
		if self.Diag_set_Radiobutton_v.get() == 0:
			UDS_adderss = 0x740
			UDS_adderss_3e = 0x740
			print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), ' 寻址设置：', UDS_adderss, UDS_adderss_3e)
		elif self.Diag_set_Radiobutton_v.get() == 1:
			UDS_adderss = 0x760
			UDS_adderss_3e = 0x760
			print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " 寻址设置：", UDS_adderss, UDS_adderss_3e)
		else:
			pass

	def data_file_path(self):
		global flash_file_path
		self.file_path.delete(0, END)
		path_ = list(tkinter.filedialog.askopenfilenames())
		for i in range(2):
			path_[i] = path_[i].replace("/", "\\\\")
		flash_file_path = path_
		logging.debug(f" loginfo[data_file_path][1]：+ {path_}")
		print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " loginfo[data_file_path][1]：" + ";".join(path_))
		self.path.set(";".join(path_))

	@With_Thread
	def data_delete(self):
		self.datainput_text.delete("1.0", END)
		self.datadisplay.delete("1.0", END)


	@staticmethod
	def select_conut(event=None):
		if demo.datainput_text.selection_get() is None:
			pass
		else:
			length = demo.datainput_text.selection_get()
			demo.len_display_lable.configure(text=f"长度 : {len(length)} ！")
			return demo.datainput_text.selection_get()

if __name__ == '__main__':
	demo = GUI()
	try:
		demo.mainloop()
	except Exception as e:
		print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 异常：", e)
		exit(0)
	finally:
		demo.close_device(dev_fd["dev_handle"], dev_fd["chn_handle"])
		exit(0)
