class DataTransform:

    #this class provides methods to obfuscate or transform data before it is proxied across the internet
    #obfuscate data would be being called by the client or upstream side, and unobfuscate will be being called by the
    #server

    def obfuscateData(self, data):
        #this is where you would pass data to be obfuscated
        #obfuscatedData = data.base64encode()
        obfuscatedData = data
        return obfuscatedData

    def unobfuscateData(self, data):
        #this is where you pass data to reverse the former method
        #unobfuscatedData = data.base64(decode)
        unobfuscatedData = data
        return unobfuscatedData

