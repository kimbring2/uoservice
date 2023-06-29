		'''
		# Draw the player mobile object
		playerMobileObjectData = self._playerMobileObjectDataList[replay_step]
		#for obj in playerMobileObjectData:
		#	print("screenX: {0}, screenY: {1}".format(obj.screenX, obj.screenY))

		screen_image = utils.visObject(screen_image, self._playerMobileObjectDataList[replay_step], (0, 255, 0))
		for obj in self._playerMobileObjectDataList[replay_step]:
			#print("vendor_title: {0}, obj: {1}".format(vendor_title, obj))
			cv2.putText(screen_image, text=obj.name, org=(obj.screenX, obj.screenY),
		            	fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.8,
		            	color=(200, 200, 0), thickness=2, lineType=cv2.LINE_4)

		# Draw the mobile object
		screen_image = utils.visObject(screen_image, self._mobileObjectDataList[replay_step], (0, 0, 255))

		# Draw the item object
		#screen_image = utils.visObject(screen_image, self._itemObjectDataList[replay_step], (255, 0, 0))

		for obj in self._mobileObjectDataList[replay_step]:
			vendor_title = utils.isVendor(obj.title)
			if vendor_title != None:
				#print("vendor_title: {0}, obj: {1}".format(vendor_title, obj))
				cv2.putText(screen_image, text=vendor_title, org=(obj.screenX, obj.screenY),
			            	fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5,
			            	color=(0, 200, 200), thickness=2, lineType=cv2.LINE_4)

		screen_image = cv2.rotate(screen_image, cv2.ROTATE_90_CLOCKWISE)
		screen_image = cv2.flip(screen_image, 1)

		# Draw the screen image on the Pygame screen
		surf = pygame.surfarray.make_surface(screen_image)
		self._screenSurface.blit(surf, (0, 0))

		# Draw the replay step on the Pygame screen
		font = pygame.font.Font('freesansbold.ttf', 32)
		replay_step_surface = font.render("step: " + str(replay_step), True, (255, 255, 255))
		self._screenSurface.blit(replay_step_surface, (0, 0))

		#self._actionTypeList.append(self.actionTypeList[step])
		#self._walkDirectionList.append(self.walkDirectionList[step])
		#self._mobileSerialList.append(self.mobileSerialList[step])
		#self._itemSerialList.append(self.itemSerialList[step])
		#self._indexList.append(self.indexList[step])
		#self._amountList.append(self.amountList[step])

		# Player status draw
		self._statusSurface.fill(((0, 0, 0)))
		player_status_grpc = self._playerStatusList[replay_step]
		player_status_dict = utils.parsePlayerStatus(player_status_grpc)
		font = pygame.font.Font('freesansbold.ttf', 32)
		text_surface = font.render("Player Status", True, (255, 0, 255))
		self._statusSurface.blit(text_surface, (0, 0))
		for i, k in enumerate(player_status_dict):
		  font = pygame.font.Font('freesansbold.ttf', 16)
		  text_surface = font.render(str(k) + ": " + str(player_status_dict[k]), True, (255, 255, 255))
		  self._statusSurface.blit(text_surface, (0, 20 * (i + 1) + 20))

		font = pygame.font.Font('freesansbold.ttf', 32)
		text_surface = font.render("Player Skills", True, (255, 0, 255))
		self._statusSurface.blit(text_surface, (0, 500))
		if len(self._playerSkillListList) > 0:
			playerSkillList = self._playerSkillListList[replay_step]
			for i, playerSkill in enumerate(playerSkillList):
				font = pygame.font.Font('freesansbold.ttf', 16)
				text_surface = font.render(str(playerSkill.index) + '. ' + str(playerSkill.name) + ": " + str(playerSkill.value), 
										   True, (255, 255, 255))
				self._statusSurface.blit(text_surface, (0, 20 * (i + 1) + 520))
				if playerSkill.index == 40:
					pass

		if len(self._openedCorpseList) > 0:
			openedCorpseList = self._openedCorpseList[replay_step]
			for openedCorpse in openedCorpseList:
				pass

		# Draw the action info on the Pygame screen
		font = pygame.font.Font('freesansbold.ttf', 16)
		text_surface = font.render("action type: " + str(self._actionTypeList[replay_step]), True, (255, 255, 255))
		self._screenSurface.blit(text_surface, (5, 40))
		text_surface = font.render("walk direction: " + str(self._walkDirectionList[replay_step]), True, (255, 255, 255))
		self._screenSurface.blit(text_surface, (5, 60))
		text_surface = font.render("run: " + str(self._runList[replay_step]), True, (255, 255, 255))
		self._screenSurface.blit(text_surface, (5, 80))
		text_surface = font.render("index: " + str(self._indexList[replay_step]), True, (255, 255, 255))
		self._screenSurface.blit(text_surface, (5, 100))

		# Draw the boundary line
		pygame.draw.line(self._screenSurface, (255, 255, 255), (1, 0), (1, self._screenHeight))
		pygame.draw.line(self._screenSurface, (255, 255, 255), (self._screenWidth - 1, 0), (self._screenWidth - 1, self._screenHeight))
		pygame.draw.line(self._screenSurface, (255, 255, 255), (0, self._screenHeight - 1), (self._screenWidth, self._screenHeight - 1))

		# Equip item draw
		self._equipItemSurface.fill(((0, 0, 0)))
		font = pygame.font.Font('freesansbold.ttf', 32)
		text_surface = font.render("Equip Items", True, (255, 0, 255))
		self._equipItemSurface.blit(text_surface, (0, 0))

		equippedItemList = self._equippedItemList[replay_step]
		print("equippedItemList: ", equippedItemList)

		# Backpack item draw
		backpack_item_grpc = self._backpackItemList[replay_step]
		backpack_item_dict = utils.parseItem(backpack_item_grpc)
		font = pygame.font.Font('freesansbold.ttf', 32)
		text_surface = font.render("Backpack Item", True, (255, 0, 255))
		self._equipItemSurface.blit(text_surface, (0, 400))
		for i, k in enumerate(backpack_item_dict):
		  font = pygame.font.Font('freesansbold.ttf', 16)
		  item = backpack_item_dict[k]
		  text_surface = font.render(str(k) + ": " + str(item[0]) + ", " + str(item[1]), True, (255, 255, 255))
		  self._equipItemSurface.blit(text_surface, (0, 20 * (i + 1) + 420))

		# Vendor item draw
		#print("len(self._vendorItemDataList): ", len(self._vendorItemDataList))
		font = pygame.font.Font('freesansbold.ttf', 32)
		text_surface = font.render("Vendor Item", True, (255, 0, 255))
		self._equipItemSurface.blit(text_surface, (0, 900))
		if len(self._vendorItemDataList) > 0:
			vendor_item_grpc = self._vendorItemDataList[replay_step]
			vendor_item_dict = utils.parseItem(vendor_item_grpc)
			for i, k in enumerate(vendor_item_dict):
			  font = pygame.font.Font('freesansbold.ttf', 16)
			  item = vendor_item_dict[k]
			  text_surface = font.render(str(k) + ": " + str(item[0]) + ", " + str(item[1]), True, (255, 255, 255))
			  self._equipItemSurface.blit(text_surface, (0, 20 * (i + 1) + 920))

		# Pop up menu draw
		self._npcSurface.fill(((0, 0, 0)))
		font = pygame.font.Font('freesansbold.ttf', 32)
		text_surface = font.render("Pop Up Menu", True, (255, 0, 255))
		self._npcSurface.blit(text_surface, (0, 0))
		if len(self._popupMenuDataList) > 0:
			for i, menu in enumerate(self._popupMenuDataList[replay_step]):
			  font = pygame.font.Font('freesansbold.ttf', 16)
			  text_surface = font.render(str(i) + ": " + str(menu), True, (255, 255, 255))
			  self._npcSurface.blit(text_surface, (0, 20 * (i + 1) + 20))
		'''