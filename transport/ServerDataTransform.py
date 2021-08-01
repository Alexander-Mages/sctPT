import base64
class DataTransform:

    def obfuscateData(self, data):
        #this is where you pass data to be obfuscated
        #obfuscatedData = base64.b64encode(data)
        obfuscatedData = data
        return obfuscatedData

    def unobfuscateData(self, data):
        #this is where you pass data to reverse the former method
        #unobfuscatedData = base64.b64decode(data)
        unobfuscatedData = data
        return unobfuscatedData

    def passthroughData(self, data):
        return data