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
Domain module.
"""

import caviar.domain.node
import caviar.engine
import caviar.network

import importlib
import sys

class Domain:

	"""
	Domain.

	:param caviar.engine.Engine engine:
	   Underlying engine.
	"""

	def __init__(self, engine, name, admin_host, admin_port, running,
			restart_required):

		self.__engine = engine
		self.__name = name
		self.__admin_host = admin_host
		self.__admin_port = admin_port
		self.__running = running
		self.__restart_required = restart_required
		
	def __eq__(self, other):
	
		return self.__name == other.__name
		
	def __asadmin(self):

		return self.__engine.asadmin()
		
	def manage(self, admin_user, admin_password):

		"""
		Manage this domain.
		
		Ensure it is running and without requiring to be restarted, and update
		its state.

		:param str admin_user:
			Name of the administrator user.
		:param str admin_password:
			Password of the administrator user.

		:rtype:
			ManagedDomain
		:return:
			The managed domain.
		"""
		
		if not self.__running:
			self.__asadmin().start_domain(self.__name)
		elif self.__restart_required:
			self.__asadmin().restart_domain(self.__name)
		self.__running = True
		self.__restart_required = False

		return ManagedDomain(
			self.__engine,
			self.__name,
			self.__admin_host,
			self.__admin_port,
			admin_user,
			admin_password
		)

class ManagedDomain(Domain):

	"""
	Managed domain.

	:param caviar.engine.Engine engine:
	   Underlying engine.
	:param str domain_name:
	   Managed domain name.
	:param str admin_host:
	   Administrator host.
	:param str admin_port:
	   Administrator port.
	:param str admin_user:
	   Administrator user name.
	:param str admin_password:
	   Administrator password.
	"""

	def __init__(self, engine, name, admin_host, admin_port, admin_user,
			admin_password):

		self.__engine = engine
		self.__name = name
		self.__admin_host = admin_host
		self.__admin_port = admin_port
		self.__admin_user = admin_user
		self.__admin_password = admin_password

	def __management(self):

		return self.__engine.management(
			self.__name,
			self.__admin_port,
			self.__admin_user,
			self.__admin_password
		)
		
	def __node_allocator(self, name):
	
		return self.__engine.node_allocator(name)
		
	def __map_node(self, data):
	
		return caviar.domain.node.Node(self.__engine)

	def create_node(self, name, allocator_name):

		"""
		Create a node on this domain.

		:param str name:
		   Node name.
		:param str allocator_name:
			Node allocator name.

		:rtype:
		   node.Node
		:return:
		   The created node.
		"""
		
		return self.__map_node(self.__management().create_node(
			name,
			self.__node_allocator(allocator_name).prepare(
				self.__name,
				name
			)
		))

class Environment:

	"""
	GlassFish environment.

	:param caviar.engine.Engine engine:
	   GlassFish engine.
	"""

	def __init__(self, engine):

		self.__engine = engine
		
	def __asadmin(self):

		return self.__engine.asadmin()
		
	def __map_domain(self, data):

		return Domain(
			self.__engine,
			data["name"],
			data["admin-host"],
			data["admin-port"],
			data["running"],
			data["restart-required"]
		)

	def domains(self):

		"""
		Available domains.

		:rtype:
		   Domain
		:return:
		   Iterator that yields available domains.
		"""

		for domain_data in self.__asadmin().list_domains():
			yield self.__map_domain(domain_data)

def environment(
	machinery_module_name,
	machinery_params,
	mgmt_public_key_path,
	mgmt_private_key_path,
	master_password,
	log_out=sys.stdout,
	ssh_module_name="caviar.provider.ssh.paramiko",
	das_server_name="das",
	node_alloc_server_prefix="nodealloc"
):

	"""
	Restore the specified environment.

	:param str machinery_module_name:
	   Machinery module name.
	:param dict machinery_params:
	   Machinery parameters.
	:param str mgmt_public_key_path:
	   Management public key path.
	:param str mgmt_private_key_path:
	   Management private key path.
	:param str master_password:
	   Used master password.
	:param fileobj log_out:
	   Logging output.

	:rtype:
	   Environment
	:return:
	   The restored environment.
	"""

	machinery_module = importlib.import_module(machinery_module_name)
	ssh_module = importlib.import_module(ssh_module_name)
	return Environment(caviar.engine.Engine(
		machinery_module.Machinery(
			machinery_params,
			mgmt_public_key_path,
			log_out
		),
		caviar.network.http_client(),
		caviar.network.ssh_session_factory(
			ssh_module.SSHClient(),
			mgmt_private_key_path
		),
		master_password,
		das_server_name,
		node_alloc_server_prefix
	))

