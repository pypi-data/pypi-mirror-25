#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (c) 2016 MasterCard International Incorporated
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of
# conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list of
# conditions and the following disclaimer in the documentation and/or other materials
# provided with the distribution.
# Neither the name of the MasterCard International Incorporated nor the names of its
# contributors may be used to endorse or promote products derived from this software
# without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#


from mastercardapicore import BaseObject
from mastercardapicore import RequestMap
from mastercardapicore import OperationConfig
from mastercardapicore import OperationMetadata
from resourceconfig import ResourceConfig

class Card(BaseObject):
	"""
	
	"""

	__config = {
		
		"82f48baf-c82b-4207-84f5-26463ef875d3" : OperationConfig("/labs/proxy/qkr2/internal/api2/card", "create", ["X-Auth-Token"], []),
		
		"3595882f-48e1-4339-86cc-b611add4e0dd" : OperationConfig("/labs/proxy/qkr2/internal/api2/card/{id}", "delete", ["X-Auth-Token"], []),
		
		"e1d98537-d603-427e-99c2-5c10e38ee486" : OperationConfig("/labs/proxy/qkr2/internal/api2/card", "query", ["X-Auth-Token"], []),
		
		"13719954-c881-4600-8454-b6ff54a15340" : OperationConfig("/labs/proxy/qkr2/internal/api2/card/{id}", "read", ["X-Auth-Token"], ["amountMinorUnits","currency","id2"]),
		
		"d2baa5b9-7249-4b83-992f-45d80180a62c" : OperationConfig("/labs/proxy/qkr2/internal/api2/card/{id}", "update", ["X-Auth-Token"], []),
		
	}

	def getOperationConfig(self,operationUUID):
		if operationUUID not in self.__config:
			raise Exception("Invalid operationUUID: "+operationUUID)

		return self.__config[operationUUID]

	def getOperationMetadata(self):
		return OperationMetadata(ResourceConfig.getInstance().getVersion(), ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext(), ResourceConfig.getInstance().getJsonNative())


	@classmethod
	def create(cls,mapObj):
		"""
		Creates object of type Card

		@param Dict mapObj, containing the required parameters to create a new object
		@return Card of the response of created instance.
		@raise ApiException: raised an exception from the response status
		"""
		return BaseObject.execute("82f48baf-c82b-4207-84f5-26463ef875d3", Card(mapObj))









	@classmethod
	def deleteById(cls,id,map=None):
		"""
		Delete object of type Card by id

		@param str id
		@return Card of the response of the deleted instance.
		@raise ApiException: raised an exception from the response status
		"""

		mapObj =  RequestMap()
		if id:
			mapObj.set("id", id)

		if map:
			if (isinstance(map,RequestMap)):
				mapObj.setAll(map.getObject())
			else:
				mapObj.setAll(map)

		return BaseObject.execute("3595882f-48e1-4339-86cc-b611add4e0dd", Card(mapObj))

	def delete(self):
		"""
		Delete object of type Card

		@return Card of the response of the deleted instance.
		@raise ApiException: raised an exception from the response status
		"""
		return BaseObject.execute("3595882f-48e1-4339-86cc-b611add4e0dd", self)








	@classmethod
	def query(cls,criteria):
		"""
		Query objects of type Card by id and optional criteria
		@param type criteria
		@return Card object representing the response.
		@raise ApiException: raised an exception from the response status
		"""

		return BaseObject.execute("e1d98537-d603-427e-99c2-5c10e38ee486", Card(criteria))





	@classmethod
	def read(cls,id,criteria=None):
		"""
		Returns objects of type Card by id and optional criteria
		@param str id
		@param dict criteria
		@return instance of Card
		@raise ApiException: raised an exception from the response status
		"""
		mapObj =  RequestMap()
		if id:
			mapObj.set("id", id)

		if criteria:
			if (isinstance(criteria,RequestMap)):
				mapObj.setAll(criteria.getObject())
			else:
				mapObj.setAll(criteria)

		return BaseObject.execute("13719954-c881-4600-8454-b6ff54a15340", Card(mapObj))



	def update(self):
		"""
		Updates an object of type Card

		@return Card object representing the response.
		@raise ApiException: raised an exception from the response status
		"""
		return BaseObject.execute("d2baa5b9-7249-4b83-992f-45d80180a62c", self)






