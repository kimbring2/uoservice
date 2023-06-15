# ---------------------------------------------------------------------
# Project "UoService"
# Copyright (C) 2023, kimbring2 
#
# Purpose of this file : Communicating with Ultima Online game client through GRPC
#
# Please reference me when you are going to use this code as reference :)

## general package imports
import numpy as np
import grpc
import subprocess
import time
import numpy as np
import cv2
import random

## UoService package imports
from uoservice.protos import UoService_pb2
from uoservice.protos import UoService_pb2_grpc
from uoservice import utils


class UoService:
	'''UoService class including gRPC client'''
	def __init__(self, grpc_port, window_width, window_height):
		self.grpc_port = grpc_port
		self.window_width = window_width
		self.window_height = window_height
		self.stub = None

		self.world_item_dict = {}
		self.world_mobile_dict = {}

	def _open_grpc(self):
		# Open the gRPC channel using the port that is same of game client 
		channel = grpc.insecure_channel('localhost:' + str(self.grpc_port))
		self.stub = UoService_pb2_grpc.UoServiceStub(channel)

	def reset(self):
		print("UoService reset()")

		self.stub.Reset(UoService_pb2.Config(name='reset'))

		# Reset the gRPC server before communcation with it.
		self.stub.WriteAct(UoService_pb2.Actions(actionType=0, mobileSerial=0, walkDirection=0, index=0, amount=0))
		self.stub.ActSemaphoreControl(UoService_pb2.SemaphoreAction(mode='post'))

		self.stub.ObsSemaphoreControl(UoService_pb2.SemaphoreAction(mode='wait'))
		response = self.stub.ReadObs(UoService_pb2.Config(name='readobs'))

		obs_raw = self.parse_response(response)

		obs = {}
		obs['mobile_data'] = obs_raw[0]
		obs['equipped_item_data'] = obs_raw[1]
		obs['backpack_item_data'] = obs_raw[2]
		obs['bank_item_data'] = obs_raw[3]
		obs['opened_corpse_list'] = obs_raw[4]
		obs['popup_menu_data'] = obs_raw[9]
		obs['player_skills_data'] = obs_raw[11]
		obs['vendor_item_data'] = obs_raw[6]
		obs['vendor_data'] = obs_raw[5]
		obs['corpse_data'] = obs_raw[12]
		obs['cliloc_data'] = obs_raw[10]
		obs['teacher_data'] = obs_raw[8]
		obs['player_mobile_data'] = obs_raw[13]
		obs['ground_item_dict'] = obs_raw[14]
		obs['player_status_dict'] = obs_raw[15]
		obs['opened_corpse_data'] = obs_raw[4]

		return obs

	def parse_response(self, response):
		# Preprocess the gRPC response format to Python friendly type
		player_skills_dict = {}
		mobile_dict = {}
		corpse_dict = {}
		player_mobile_dict = {}
		mountable_mobile_dict = {}
		ground_item_dict = {}
		equipped_item_dict = {}
		backpack_item_dict = {}
		bank_item_dict = {}
		opened_corpse_list_dict = {}
		vendor_dict = {}
		vendor_item_dict = {}
		teacher_dict = {}
		player_skill_dict = {}
		player_status_dict = {}
		popup_menu_list = []
		cliloc_dict = {}
		static_object_screen_x_list = []
		static_object_screen_y_list = []

		world_item_data = response.WorldItemList.gameObjects
		world_mobile_data = response.WorldItemList.gameObjects

		equipped_item_data = response.equippedItemSerialList.serials
		backpack_item_data = response.backpackItemSerialList.serials
		bank_item_data = response.bankItemSerialList.serials
		opened_corpse_list = response.openedCorpseList.containers
		popup_menu_data = response.popupMenuList.menus
		player_status_data = response.playerStatus
		player_skills_data = response.playerSkillList.skills
		static_object_screen_x_data = response.staticObjectInfoList.screenXs
		static_object_screen_y_data = response.staticObjectInfoList.screenYs
		vendor_item_data = response.vendorItemSerialList.serials
		cliloc_data = response.clilocDataList.clilocDatas
		player_mobile_serial_data = response.playerMobileObjectList.serials
		mobile_serial_data = response.mobileObjectList.serials
		item_serial_data = response.itemObjectList.serials

		#print("len(world_item_data): ", len(world_item_data))
		if len(world_item_data) != 0:
			for obj in world_item_data:
				self.world_item_dict[obj.serial] = [obj.name, obj.type, obj.screenX, obj.screenY, obj.distance, obj.title, obj.layer]

		#print("len(world_item_data): ", len(world_item_data))
		if len(world_mobile_data) != 0:
			for obj in world_mobile_data:
				self.world_mobile_dict[obj.serial] = [obj.name, obj.type, obj.screenX, obj.screenY, obj.distance, obj.title, obj.layer]

		for item in bank_item_data:
			#print('type:{0}, x:{1}, y:{2}, dis:{3}, serial:{4}, name:{5}, amount:{6}, price:{7}'.
			#			format(obj.type, obj.screenX, obj.screenY, obj.distance, obj.serial, obj.name, obj.amount, obj.price))
			bank_item_dict[item.serial] = [item.name, item.layer, item.amount]

		for skill in player_skills_data:
			player_skills_dict[skill.name] = [skill.index, skill.isClickable, skill.value, skill.base, skill.cap, skill.lock]

		for data in cliloc_data:
			#print("data: ", data)
			if data.serial not in cliloc_dict:
				cliloc_dict[data.serial] = [[data.text, data.affix, data.name]]
			else:
				cliloc_dict[data.serial].append([[data.text, data.affix, data.name]])

		player_status_dict = utils.parsePlayerStatus(player_status_data)

		#print("self.world_item_dict: ", self.world_item_dict)
		print("self.world_mobile_dict: ", self.world_mobile_dict)

		#print("bank_item_data: ", bank_item_data)
		#print("\n")

		for menu_data in popup_menu_data:
			popup_menu_list.append(menu_data)

		'''
		for obj in item_object_data:
			ground_item_dict[obj.serial] = [obj.name, obj.type, obj.screenX, obj.screenY, obj.distance, obj.title]
			if obj.isCorpse:
				corpse_dict[obj.serial] = [obj.name, obj.type, obj.screenX, obj.screenY, obj.distance, obj.title]

		for obj in vendor_item_data:
			#print('type:{0}, x:{1}, y:{2}, dis:{3}, serial:{4}, name:{5}, amount:{6}, price:{7}'.
			#			format(obj.type, obj.screenX, obj.screenY, obj.distance, obj.serial, obj.name, obj.amount, obj.price))
			vendor_item_dict[obj.serial] = [obj.name, obj.type, obj.price, obj.amount, obj.title]

		for obj in mobile_object_data:
			#print('type:{0}, x:{1}, y:{2}, dis:{3}, serial:{4}, name:{5}, is_corpse:{6}, title:{7}'.
			#		format(obj.type, obj.screenX, obj.screenY, obj.distance, obj.serial, obj.name, obj.isCorpse, obj.title))
			mobile_dict[obj.serial] = [obj.name, obj.type, obj.screenX, obj.screenY, obj.distance, obj.title]

			vendor_title = utils.isVendor(obj.title)
			if vendor_title and obj.distance <= 5:
				vendor_dict[obj.serial] = [obj.name, obj.type, obj.screenX, obj.screenY, obj.distance, obj.title]

			#if obj.distance <= 5:
			#	print("obj.title: ", obj.title)

			teacher_title = utils.isTeacher(obj.title)
			if teacher_title and obj.distance <= 5:
				#print("teacher_title: ", teacher_title)
				teacher_dict[obj.serial] = [obj.name, obj.type, obj.screenX, obj.screenY, obj.distance, teacher_title]
		'''

		screen_image = np.zeros((172,137,4), dtype=np.uint8)
		#print("mobile_serial_data: ", mobile_serial_data)
		for serial in mobile_serial_data:
			#print('type:{0}, x:{1}, y:{2}, dis:{3}, serial:{4}, name:{5}, amount:{6}, price:{7}'.
			#			format(obj.type, obj.gameX, obj.gameY, obj.distance, obj.serial, obj.name, obj.amount, obj.price))

			#[obj.name, obj.type, obj.screenX, obj.screenY, obj.distance, obj.title, obj.layer]
			if serial in self.world_mobile_dict:
				mobile = self.world_mobile_dict[serial]

				mobile_dict[serial] = [mobile[0], mobile[1], mobile[2], mobile[3], mobile[4], mobile[5]]

				try:
					screen_image[int(mobile[2] / 10), int(mobile[3] / 10), 0] = 255
					screen_image[int(mobile[2] / 10), int(mobile[3] / 10), 1] = 0
					screen_image[int(mobile[2] / 10), int(mobile[3] / 10), 2] = 0
				except:
					pass
			else:
				#print("mobile serial is not existed in world_mobile_dict: ", serial)
				pass

		vis = True
		if vis:
			dim = (1720, 1370)
			screen_image = cv2.resize(screen_image, dim, interpolation = cv2.INTER_AREA)
			screen_image = cv2.rotate(screen_image, cv2.ROTATE_90_CLOCKWISE)
			screen_image = cv2.flip(screen_image, 1)
			cv2.imshow('screen_image_' + str(self.grpc_port), screen_image)
			cv2.waitKey(1)

		for i in range(0, len(static_object_screen_x_data)):
			static_object_screen_x_list.append(static_object_screen_x_data[i])
			static_object_screen_y_list.append(static_object_screen_y_data[i])

		if len(equipped_item_data) == 0:
			return mobile_dict, equipped_item_dict, backpack_item_dict, bank_item_dict, opened_corpse_list_dict, \
				vendor_dict, vendor_item_dict, mountable_mobile_dict, teacher_dict, popup_menu_list, cliloc_dict, \
				player_skills_dict, corpse_dict, player_mobile_dict, ground_item_dict, player_status_dict

		for item_serial in equipped_item_data:
			if item_serial in self.world_item_dict:
				item = self.world_item_dict[item_serial]
				# [obj.name, obj.type, obj.screenX, obj.screenY, obj.distance, obj.title, obj.layer]
				equipped_item_dict[item_serial] = [item[0], item[6], item[2]]
			else:
				#print("item is not existed: ", item_serial)
				pass

		for item_serial in backpack_item_data:
			#backpack_item_dict[item.serial] = [item.name, item.layer, item.amount]
			if item_serial in self.world_item_dict:
				item = self.world_item_dict[item_serial]
				#print('backpack name: {0}, layer: {1}, serial: {2}:'.format(item[0], item[1], item[2]))
				backpack_item_dict[item_serial] = [item[0], item[6], item[2]]
			else:
				#print("item is not existed: ", item_serial)
				pass

		for opened_corpse in opened_corpse_list:
			corpse_object = opened_corpse.container
			#print('type: {0}, x: {1}, y: {2}, distance: {3}, name: {4}'.format(corpse_object.type, corpse_object.screenX, corpse_object.screenY,
			#																																	 corpse_object.distance, corpse_object.name))
			corpse_item_list = []
			for item in opened_corpse.containerItemList.items:
				corpse_item_list.append([item.serial, item.name, item.layer, item.amount])

			opened_corpse_list_dict[corpse_object.serial] = corpse_item_list

		#print("backpack_item_dict: ", backpack_item_dict)

		return mobile_dict, equipped_item_dict, backpack_item_dict, bank_item_dict, opened_corpse_list_dict, vendor_dict, \
					 vendor_item_dict, mountable_mobile_dict, teacher_dict, popup_menu_list, cliloc_dict, player_skills_dict, \
					 corpse_dict, player_mobile_dict, ground_item_dict, player_status_dict

	def step(self, action):
		# Send the action data to game client and receive the state of that action
		action_type = action['action_type']
		item_serial = action['item_serial']
		mobile_serial = action['mobile_serial']
		walk_direction = action['walk_direction']
		index = action['index']
		amount = action['amount']
		run = action['run']

		self.stub.WriteAct(UoService_pb2.Actions(actionType=action_type, 
																						 itemSerial=item_serial,
																						 mobileSerial=mobile_serial,
																						 walkDirection=walk_direction,
																						 index=index, 
																						 amount=amount,
																						 run=run))
		self.stub.ActSemaphoreControl(UoService_pb2.SemaphoreAction(mode='post'))
		self.stub.ObsSemaphoreControl(UoService_pb2.SemaphoreAction(mode='wait'))
		response = self.stub.ReadObs(UoService_pb2.Config(name='readobs'))

		obs_raw = self.parse_response(response)

		obs = {}

		#print("obs_raw[2]: ", obs_raw[2])
		
		#mobile_dict, equipped_item_dict, backpack_item_dict, bank_item_dict, opened_corpse_list_dict, vendor_dict, \
		#vendor_item_dict, mountable_mobile_dict, teacher_dict, popup_menu_list, cliloc_dict, player_skills_dict, \
		#corpse_dict, player_mobile_dict, ground_item_dict, player_status_dict
		obs['mobile_data'] = obs_raw[0]
		obs['equipped_item_data'] = obs_raw[1]
		obs['backpack_item_data'] = obs_raw[2]
		obs['bank_item_data'] = obs_raw[3]
		obs['opened_corpse_list'] = obs_raw[4]
		obs['popup_menu_data'] = obs_raw[9]
		obs['player_skills_data'] = obs_raw[11]
		obs['vendor_item_data'] = obs_raw[6]
		obs['vendor_data'] = obs_raw[5]
		obs['corpse_data'] = obs_raw[12]
		obs['cliloc_data'] = obs_raw[10]
		obs['teacher_data'] = obs_raw[8]
		obs['player_mobile_data'] = obs_raw[13]
		obs['ground_item_data'] = obs_raw[14]
		obs['player_status_data'] = obs_raw[15]
		obs['opened_corpse_data'] = obs_raw[4]

		return obs