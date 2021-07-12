#defines a class that represents a pt's config


class TransportConfig( object ):

    """
    This class embeds configuration options for pluggable transport modules.

    The options are set by obfsproxy and then passed to the transport's class
    constructor.  The pluggable transport might want to use these options but
    does not have to.  An example of such an option is the state location which
    can be used by the pluggable transport to store persistent information.
    """

    def __init__(self):
        #initialise a transportconfig object

        self.stateLocation = None
        self.serverTransportOptions = None

        #true if client
        self.weAreClient = None
        #true if external mode
        self.weAreExternal = None

    def setStateLocation( self, stateLocation ):
        #set given stateLocation
        self.stateLocation = stateLocation

    def getStateLocation(self):
        #return saved state location
        return self.stateLocation

    def setServerTransportOptions(self, serverTransportOptions):
        #set given server transport options

        self.serverTransportOptions = serverTransportOptions

    def getServerTransportOptions(self):
        #return saved serverTransportOptions

        return self.serverTransportOptions



    def setListenerMode(self, mode):
        if mode == "client" or mode == "socks":
            self.weAreClient = True
        elif mode == "server" or mode == "ext_server":
            self.weAreClient = False
        else:
            raise ValueError("Invalid listener mode: %s" % mode)

    def setObfsproxymode(self, mode):
        if mode == "external":
            self.weAreExternal = True
        elif mode == "managed":
            self.weAreExternal = False
        else:
            raise ValueError("Invalid obfsproxy mode: %s" % mode)


    def __str__(self):
        #return string representation of transportconfig instance

        return str(vars(self))