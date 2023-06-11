import numpy as np
import grpc
import subprocess

import UoService_pb2
import UoService_pb2_grpc
import utils


class UoService:
	def __init__(self, grpc_port, window_width, window_height):
			self.grpc_port = grpc_port
			self.window_width = window_width
			self.window_height = window_height
			self.stub = None

	def _open_grpc(self):
		channel = grpc.insecure_channel('localhost:' + str(self.grpc_port))
		self.stub = UoService_pb2_grpc.UoServiceStub(channel)

	def reset(self):
		self.stub.WriteAct(UoService_pb2.Actions(actionType=0, mobileSerial=0, walkDirection=0, index=0, amount=0))
		self.stub.ActSemaphoreControl(UoService_pb2.SemaphoreAction(mode='post'))

		self.stub.ObsSemaphoreControl(UoService_pb2.SemaphoreAction(mode='wait'))
		response = self.stub.ReadObs(UoService_pb2.Config(name='reset'))

		obs_raw = self.parse_response(response)

		obs = {}
		
		#mobile_dict, equipped_item_dict, backpack_item_dict, bank_item_dict, opened_corpse_list_dict, vendor_dict, \
		#			 vendor_item_dict, mountable_mobile_dict, teacher_dict, popup_menu_list, cliloc_data_list, player_skills_dict
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

		return obs

	def parse_response(self, response):
		player_skills_dict = {}
		mobile_dict = {}
		corpse_dict = {}
		player_mobile_dict = {}
		mountable_mobile_dict = {}
		ground_item_dict = {}
		world_item_dict = {}
		equipped_item_dict = {}
		backpack_item_dict = {}
		bank_item_dict = {}
		opened_corpse_list_dict = {}
		vendor_dict = {}
		vendor_item_dict = {}
		teacher_dict = {}
		player_skill_dict = {}
		popup_menu_list = []
		cliloc_dict = {}
		static_object_screen_x_list = []
		static_object_screen_y_list = []

		mobile_data = response.mobileList.mobile
		equipped_item_data = response.equippedItemList.item
		backpack_item_data = response.backpackItemList.item
		bank_item_data = response.bankItemList.item
		opened_corpse_list = response.openedCorpseList.containers
		popup_menu_data = response.popupMenuList.menu
		player_status_data = response.playerStatus
		player_skills_data = response.playerSkillList.skills
		static_object_screen_x_data = response.staticObjectInfoList.screenXs
		static_object_screen_y_data = response.staticObjectInfoList.screenYs
		vendor_item_data = response.vendorItemObjectList.gameObject
		cliloc_data = response.clilocDataList.clilocData
		player_mobile_object_data = response.playerMobileObjectList.gameObject
		mobile_object_data = response.mobileObjectList.gameObject
		item_object_data = response.itemObjectList.gameObject
		item_dropable_land_data = response.itemDropableLandList.gameSimpleObject

		for skill in player_skills_data:
			player_skills_dict[skill.name] = [skill.index, skill.isClickable, skill.value, skill.base, skill.cap, skill.lock]

		for data in cliloc_data:
			#print("data: ", data)

			if data.serial not in cliloc_dict:
				cliloc_dict[data.serial] = [[data.text, data.affix, data.name]]
			else:
				cliloc_dict[data.serial].append([[data.text, data.affix, data.name]])

		for item in bank_item_data:
			#print('type:{0}, x:{1}, y:{2}, dis:{3}, serial:{4}, name:{5}, amount:{6}, price:{7}'.
			#			format(obj.type, obj.screenX, obj.screenY, obj.distance, obj.serial, obj.name, obj.amount, obj.price))
			bank_item_dict[item.serial] = [item.name, item.layer, item.amount]

		#print("bank_item_data: ", bank_item_data)
		#print("\n")

		for menu_data in popup_menu_data:
			popup_menu_list.append(menu_data)

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

		for obj in player_mobile_object_data:
			#print('type:{0}, x:{1}, y:{2}, dis:{3}, serial:{4}, name:{5}, amount:{6}, price:{7}'.
			#			format(obj.type, obj.screenX, obj.screenY, obj.distance, obj.serial, obj.name, obj.amount, obj.price))
			player_mobile_dict[obj.serial] = [obj.name, obj.type, obj.screenX, obj.screenY, obj.distance, obj.title]

		for i in range(0, len(static_object_screen_x_data)):
			static_object_screen_x_list.append(static_object_screen_x_data[i])
			static_object_screen_y_list.append(static_object_screen_y_data[i])

		if len(mobile_data) == 0 or len(equipped_item_data) == 0:
			return mobile_dict, equipped_item_dict, backpack_item_dict, bank_item_dict, opened_corpse_list_dict, \
				vendor_dict, vendor_item_dict, mountable_mobile_dict, teacher_dict, popup_menu_list, cliloc_dict, \
				player_skills_dict, corpse_dict

		for mobile in mobile_data:
			#print('name: {0}, x: {1}, y: {2}, race: {3}, serial: {4}\n'.format(mobile.name, mobile.x, mobile.y, mobile.race,
			#																																	 mobile.serial))
			mobile_dict[mobile.serial] = [mobile.name, int(mobile.x), int(mobile.y), mobile.race]
			if mobile.x >= 1600 or mobile.y >= 1280:
				continue

		for item in equipped_item_data:
			#print('name: {0}, layer: {1}, serial: {2}, amount: {3}'.format(item.name, item.layer, item.serial, item.amount))
			equipped_item_dict[item.serial] = [item.name, item.layer, item.amount]

		for item in backpack_item_data:
			backpack_item_dict[item.serial] = [item.name, item.layer, item.amount]

		for opened_corpse in opened_corpse_list:
			corpse_object = opened_corpse.container
			#print('type: {0}, x: {1}, y: {2}, distance: {3}, name: {4}'.format(corpse_object.type, corpse_object.screenX, corpse_object.screenY,
			#																																	 corpse_object.distance, corpse_object.name))
			corpse_item_list = []
			for item in opened_corpse.containerItemList.item:
				corpse_item_list.append([item.name, item.layer, item.amount])

			opened_corpse_list_dict[corpse_object.serial] = corpse_item_list

		#print("opened_corpse_list_dict: ", opened_corpse_list_dict)

		return mobile_dict, equipped_item_dict, backpack_item_dict, bank_item_dict, opened_corpse_list_dict, vendor_dict, \
					 vendor_item_dict, mountable_mobile_dict, teacher_dict, popup_menu_list, cliloc_dict, player_skills_dict, \
					 corpse_dict

	def step(self, action):
		action_type = action['action_type']
		item_serial = action['item_serial']
		mobile_serial = action['mobile_serial']
		walk_direction = action['walk_direction']
		index = action['index']
		amount = action['amount']

		self.stub.WriteAct(UoService_pb2.Actions(actionType=action_type, 
																						 itemSerial=item_serial,
																						 mobileSerial=mobile_serial,
																						 walkDirection=walk_direction,
																						 index=index, 
																						 amount=amount))
		self.stub.ActSemaphoreControl(UoService_pb2.SemaphoreAction(mode='post'))

		self.stub.ObsSemaphoreControl(UoService_pb2.SemaphoreAction(mode='wait'))
		response = self.stub.ReadObs(UoService_pb2.Config(name='step'))

		obs_raw = self.parse_response(response)

		obs = {}
		
		#mobile_dict, equipped_item_dict, backpack_item_dict, bank_item_dict, opened_corpse_list_dict, vendor_dict, \
		#vendor_item_dict, mountable_mobile_dict, teacher_dict, popup_menu_list, cliloc_dict, player_skills_dict, \
		#corpse_dict
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
		
		return obs