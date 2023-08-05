from covertutils.handlers import BufferedHandler

class NullOrchestrator(Orchestrator) :

	def readyMessage( self, message, stream ) :
		return "%s:%s" % (stream, message)

	def depositChunk( self, chunk ) :
		return 'control', chunk




class SimpleMultiHandler( BufferedHandler ) :


	def __init__( handlers ) :
		assert type(handlers == list)
		self.handlers = [handler.getOrchestrator().getIdentity(), handler for handler in handlers ]
