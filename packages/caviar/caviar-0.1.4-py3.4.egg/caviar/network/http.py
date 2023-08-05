#
# This file is part of CAVIAR.
#
# CAVIAR is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CAVIAR is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CAVIAR.  If not, see <http://www.gnu.org/licenses/>.
#

"""
HTTP module.
"""

import requests

class HTTPClient:

	"""
	HTTP client.
	"""
	
	def basic(self, user, password):
	
		"""
		Create a basic login session.
		
		:param str user:
		   User name.
		:param str password:
		   User password.
		   
		:rtype:
		   HTTPSession
		:return:
		   Basic login session.
		"""
		
		return HTTPSession(requests.auth.HTTPBasicAuth(
			user,
			password
		))

class HTTPSession:

	def __init__(self, auth):
	
		self.__auth = auth
		
	def get(self, url, params=None, headers=None):
	
		pass
		
	def post(self, url, body, params=None, headers=None):
	
		pass

	def delete(self, url, params=None, headers=None):
	
		pass

