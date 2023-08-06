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

class Node(BaseObject):
	"""
	
	"""

	__config = {
		
		"394e8410-1b43-45c4-a9cc-8af33c48c93e" : OperationConfig("/labs/proxy/chain/api/v1/network/create", "create", [], []),
		
		"59f70f71-1980-4492-bc29-d9d3c60f5685" : OperationConfig("/labs/proxy/chain/api/v1/network/invite", "create", [], []),
		
		"bcebcf67-188a-44d0-9ff0-f08718ecabae" : OperationConfig("/labs/proxy/chain/api/v1/network/join", "create", [], []),
		
		"7257dc46-3f6c-4ff3-a119-da1135d4bc96" : OperationConfig("/labs/proxy/chain/api/v1/network/node/{address}", "read", [], []),
		
		"fca24c6e-de8c-49e3-9cfb-166571bb8550" : OperationConfig("/labs/proxy/chain/api/v1/network/node", "query", [], []),
		
	}

	def getOperationConfig(self,operationUUID):
		if operationUUID not in self.__config:
			raise Exception("Invalid operationUUID: "+operationUUID)

		return self.__config[operationUUID]

	def getOperationMetadata(self):
		return OperationMetadata(ResourceConfig.getInstance().getVersion(), ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext(), ResourceConfig.getInstance().getJsonNative())


	@classmethod
	def provision(cls,mapObj):
		"""
		Creates object of type Node

		@param Dict mapObj, containing the required parameters to create a new object
		@return Node of the response of created instance.
		@raise ApiException: raised an exception from the response status
		"""
		return BaseObject.execute("394e8410-1b43-45c4-a9cc-8af33c48c93e", Node(mapObj))






	@classmethod
	def invite(cls,mapObj):
		"""
		Creates object of type Node

		@param Dict mapObj, containing the required parameters to create a new object
		@return Node of the response of created instance.
		@raise ApiException: raised an exception from the response status
		"""
		return BaseObject.execute("59f70f71-1980-4492-bc29-d9d3c60f5685", Node(mapObj))






	@classmethod
	def join(cls,mapObj):
		"""
		Creates object of type Node

		@param Dict mapObj, containing the required parameters to create a new object
		@return Node of the response of created instance.
		@raise ApiException: raised an exception from the response status
		"""
		return BaseObject.execute("bcebcf67-188a-44d0-9ff0-f08718ecabae", Node(mapObj))










	@classmethod
	def read(cls,id,criteria=None):
		"""
		Returns objects of type Node by id and optional criteria
		@param str id
		@param dict criteria
		@return instance of Node
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

		return BaseObject.execute("7257dc46-3f6c-4ff3-a119-da1135d4bc96", Node(mapObj))







	@classmethod
	def query(cls,criteria):
		"""
		Query objects of type Node by id and optional criteria
		@param type criteria
		@return Node object representing the response.
		@raise ApiException: raised an exception from the response status
		"""

		return BaseObject.execute("fca24c6e-de8c-49e3-9cfb-166571bb8550", Node(criteria))


