import numpy as np
import grpc
import subprocess

import UoService_pb2
import UoService_pb2_grpc


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

		obs = {}
		obs['mobile_data'] = response.mobileList.mobile
		obs['equipped_item_data'] = response.equippedItemList.item
		obs['backpack_item_data'] = response.backpackItemList.item
		obs['opened_corpse_list'] = response.openedCorpseList.corpse
		obs['popup_menu_data'] = response.popupMenuList.menu
		obs['player_status_data'] = response.playerStatus
		obs['player_skills_data'] = response.playerSkillList.skills
		obs['vendor_item_data'] = response.vendorItemObjectList.gameObject
		obs['player_mobile_object_data'] = response.playerMobileObjectList.gameObject
		obs['mobile_object_data'] = response.mobileObjectList.gameObject
		obs['item_object_data'] = response.itemObjectList.gameObject
		obs['item_dropable_land_data'] = response.itemDropableLandList.gameSimpleObject

		return obs

	def parse_response(self, response):
	  player_skills_dict = {}
	  mobile_dict = {}
	  player_mobile_dict = {}
	  mountable_mobile_dict = {}
	  world_item_dict = {}
	  equipped_item_dict = {}
	  backpack_item_dict = {}
	  ground_item_dict = {}
	  opened_corpse_list_dict = {}
	  vendor_dict = {}
	  vendor_item_dict = {}
	  teacher_dict = {}
	  player_skill_dict = {}
	  popup_menu_list = []
	  cliloc_data_list = []
	  static_object_screen_x_list = []
	  static_object_screen_y_list = []

	  mobile_data = response.mobileList.mobile
	  equipped_item_data = response.equippedItemList.item
	  backpack_item_data = response.backpackItemList.item
	  opened_corpse_list = response.openedCorpseList.corpse
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
	    cliloc_dict = {}
	    cliloc_dict['text'] = data.text
	    cliloc_dict['affix'] = data.affix
	    cliloc_data_list.append(cliloc_dict)

	  for menu_data in popup_menu_data:
	    popup_menu_list.append(menu_data)

	  for obj in item_object_data:
	    ground_item_dict[obj.serial] = [obj.name, obj.type, obj.screenX, obj.screenY, obj.distance, obj.title]

	  for obj in vendor_item_data:
	    #print('type:{0}, x:{1}, y:{2}, dis:{3}, serial:{4}, name:{5}, amount:{6}, price:{7}'.
	    #      format(obj.type, obj.screenX, obj.screenY, obj.distance, obj.serial, obj.name, obj.amount, obj.price))
	    vendor_item_dict[obj.serial] = [obj.name, obj.type, obj.price, obj.amount, obj.title]

	  for obj in mobile_object_data:
	    #print('type:{0}, x:{1}, y:{2}, dis:{3}, serial:{4}, name:{5}, is_corpse:{6}, title:{7}'.
	    #    format(obj.type, obj.screenX, obj.screenY, obj.distance, obj.serial, obj.name, obj.isCorpse, obj.title))
	    mobile_dict[obj.serial] = [obj.name, obj.type, obj.screenX, obj.screenY, obj.distance, obj.title]

	  for obj in player_mobile_object_data:
	    #print('type:{0}, x:{1}, y:{2}, dis:{3}, serial:{4}, name:{5}, amount:{6}, price:{7}'.
	    #      format(obj.type, obj.screenX, obj.screenY, obj.distance, obj.serial, obj.name, obj.amount, obj.price))
	    player_mobile_dict[obj.serial] = [obj.name, obj.type, obj.screenX, obj.screenY, obj.distance, obj.title]

	  for i in range(0, len(static_object_screen_x_data)):
	  	static_object_screen_x_list.append(static_object_screen_x_data[i])
	  	static_object_screen_y_list.append(static_object_screen_y_data[i])

	  if len(mobile_data) == 0 or len(equipped_item_data) == 0:
	    return mobile_dict, equipped_item_dict, backpack_item_dict, ground_item_dict, opened_corpse_list_dict, \
	      vendor_dict, vendor_item_dict, mountable_mobile_dict, teacher_dict, \
	      popup_menu_list, cliloc_data_list, player_skills_dict

	  for mobile in mobile_data:
	    #print('name: {0}, x: {1}, y: {2}, race: {3}, serial: {4}\n'.format(mobile.name, mobile.x, mobile.y, mobile.race,
	    #                                                                   mobile.serial))
	    mobile_dict[mobile.serial] = [mobile.name, int(mobile.x), int(mobile.y), mobile.race]

	    if mobile.x >= 1600 or mobile.y >= 1280:
	      continue

	  for item in equipped_item_data:
	    #print('name: {0}, layer: {1}, serial: {2}, amount: {3}'.format(item.name, item.layer, item.serial, item.amount))
	    equipped_item_dict[item.serial] = [item.name, item.layer, item.amount]

	  for item in backpack_item_data:
	    backpack_item_dict[item.serial] = [item.name, item.layer, item.amount]

	  for opened_corpse in opened_corpse_list:
	    corpse_object = opened_corpse.corpse
	    #print('type: {0}, x: {1}, y: {2}, distance: {3}, name: {4}'.format(corpse_object.type, corpse_object.screenX, corpse_object.screenY,
	    #																																	 corpse_object.distance, corpse_object.name))
	    corpse_item_list = []
	    for item in opened_corpse.corpseItemList.item:
	    	corpse_item_list.append([item.name, item.layer, item.amount])

	    opened_corpse_list_dict[corpse_object.serial] = corpse_item_list

	  #print("opened_corpse_list_dict: ", opened_corpse_list_dict)

	  return mobile_dict, equipped_item_dict, backpack_item_dict, ground_item_dict, opened_corpse_list_dict, \
	      vendor_dict, vendor_item_dict, mountable_mobile_dict, teacher_dict, popup_menu_list, cliloc_data_list, player_skills_dict

	def step(self, action):
		action_type = action['action_type']
		mobile_serial = action['mobile_serial']
		item_serial = action['item_serial']
		walk_direction = action['walk_direction']
		index = action['index']
		amount = action['amount']

		self.stub.WriteAct(UoService_pb2.Actions(actionType=action_type, 
                                             mobileSerial=mobile_serial,
                                             itemSerial=item_serial,
                                             walkDirection=walk_direction,
                                             index=index, 
                                             amount=amount))

		self.stub.ActSemaphoreControl(UoService_pb2.SemaphoreAction(mode='post'))
		self.stub.ObsSemaphoreControl(UoService_pb2.SemaphoreAction(mode='wait'))

		response = self.stub.ReadObs(UoService_pb2.Config(name='step'))

		self.parse_response(response)

		obs = {}
		'''
		obs['mobile_data'] = response.mobileList.mobile
		obs['equipped_item_data'] = response.equippedItemList.item
		obs['backpack_item_data'] = response.backpackItemList.item
		obs['opened_corpse_list'] = response.openedCorpseList.corpse
		obs['popup_menu_data'] = response.popupMenuList.menu
		obs['player_status_data'] = response.playerStatus
		obs['player_skills_data'] = response.playerSkillList.skills
		obs['vendor_item_data'] = response.vendorItemObjectList.gameObject
		obs['player_mobile_object_data'] = response.playerMobileObjectList.gameObject
		obs['mobile_object_data'] = response.mobileObjectList.gameObject
		obs['item_object_data'] = response.itemObjectList.gameObject
		obs['item_dropable_land_data'] = response.itemDropableLandList.gameSimpleObject
		'''

		return obs




