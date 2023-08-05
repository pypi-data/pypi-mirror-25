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
Management module.
"""

class Management:

	"""
	Management client.
	"""

	def __init__(self, http_client, domain_name, das_machine, port, user,
			password):

		self.__http_session = http_client.basic(user, password)
		self.__domain_name = domain_name
		self.__host = das_machine.host
		self.__port = port
		self.__user = user
		self.__password = password

	def create_node(self, name, host):

		"""
		Create a node with the given name to the given host.

		:param str name:
		   Name of the node.
		   
		:rtype:
		   dict
		:return:
		   Created node data.
		"""

		pass

