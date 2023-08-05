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
Network module.
"""

import caviar.network.http
import caviar.network.ssh

def http_client():

	"""
	Create an HTTP client.
	
	:rtype:
	   http.HTTPClient
	:return:
	   The created HTTP client.
	"""
	
	return caviar.network.http.HTTPClient()

def ssh_session_factory(ssh_client, private_key_path):

	"""
	Create an SSH session factory.
	
	:param SSHClient ssh_client:
	   SSH client implementation.
	:param str private_key_path:
	   Path of local private key file.
	   
	:rtype:
	   ssh.SSHSessionFactory
	:return:
	   The created SSH session factory.
	"""
	
	return caviar.network.ssh.SSHSessionFactory(ssh_client, private_key_path)

