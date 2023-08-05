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

class Payments(BaseObject):
	"""
	
	"""

	__config = {
		
		"1dfe7134-12e0-4e33-9d92-5ed0ca2614f4" : OperationConfig("/labs/proxy/blockchain/b2bxb/api/v1/payments", "list", [], ["status"]),
		
		"4c0f5654-cb2a-4435-8f2b-004ee8eccfdb" : OperationConfig("/labs/proxy/blockchain/b2bxb/api/v1/payments", "create", [], []),
		
		"2fe5a3df-6747-47b7-a8eb-9cef86e782b1" : OperationConfig("/labs/proxy/blockchain/b2bxb/api/v1/payments/{reference}", "read", [], []),
		
	}

	def getOperationConfig(self,operationUUID):
		if operationUUID not in self.__config:
			raise Exception("Invalid operationUUID: "+operationUUID)

		return self.__config[operationUUID]

	def getOperationMetadata(self):
		return OperationMetadata(ResourceConfig.getInstance().getVersion(), ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext(), ResourceConfig.getInstance().getJsonNative())




	@classmethod
	def listByCriteria(cls,criteria=None):
		"""
		List objects of type Payments

		@param Dict criteria
		@return Array of Payments object matching the criteria.
		@raise ApiException: raised an exception from the response status
		"""

		if not criteria :
			return BaseObject.execute("1dfe7134-12e0-4e33-9d92-5ed0ca2614f4", Payments())
		else:
			return BaseObject.execute("1dfe7134-12e0-4e33-9d92-5ed0ca2614f4", Payments(criteria))




	@classmethod
	def create(cls,mapObj):
		"""
		Creates object of type Payments

		@param Dict mapObj, containing the required parameters to create a new object
		@return Payments of the response of created instance.
		@raise ApiException: raised an exception from the response status
		"""
		return BaseObject.execute("4c0f5654-cb2a-4435-8f2b-004ee8eccfdb", Payments(mapObj))










	@classmethod
	def read(cls,id,criteria=None):
		"""
		Returns objects of type Payments by id and optional criteria
		@param str id
		@param dict criteria
		@return instance of Payments
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

		return BaseObject.execute("2fe5a3df-6747-47b7-a8eb-9cef86e782b1", Payments(mapObj))



