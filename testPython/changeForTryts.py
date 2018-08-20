# coding:utf-8
import json
import string
import copy
import math
import numpy as np

class changeForTryts(object):

    def __init__(self):
        self.BYTE_TO_TRITS_MAPPINGS =  [[0 for col in range(0)] for row in range(243)]
        self.TRYTE_TO_TRITS_MAPPINGS =  [[0 for col in range(0)] for row in range(27)]
        self.TRYTE_ALPHABET = "9ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.initialization()

    def getDict(self, json_string):
        #将json转换为字典表
        json_dict = dict()
        json_dict = json.loads(json_string)
        return json_dict
    
    #二进制转三进
    def change(self,Twonumber):
        num = int("Twonumber",2)
        n = int(math.log10(num)/math.log10(3)) + 1
        trits_number = ''
        for i in range(n):
            num_add = num/(3**(n-i-1))
            trits_number = trits_number + str(number_add)
            num = num - num_add * (3 ** (n-i-1))
        return trits_number

    def initialization(self):
        RADIX = 3
        MAX_TRIT_VALUE = (RADIX - 1) / 2
        MIN_TRIT_VALUE = -MAX_TRIT_VALUE
        NUMBER_OF_TRITS_IN_A_BYTE = 5
        NUMBER_OF_TRITS_IN_A_TRYTE = 3
        trits = [0] * NUMBER_OF_TRITS_IN_A_BYTE
        trits2 = [0] * NUMBER_OF_TRITS_IN_A_TRYTE
        for i in xrange(243):
            for j in xrange(NUMBER_OF_TRITS_IN_A_BYTE):
                trits[j] = trits[j] + 1 
                if trits[j] > 1:
                    trits[j] = -1
                else:
                    break
            self.BYTE_TO_TRITS_MAPPINGS[i] = trits[:]

        for i in xrange(27):
            for j in xrange(NUMBER_OF_TRITS_IN_A_TRYTE):
                trits2[j] = trits2[j] + 1
                if trits2[j] > 1:
                    trits2[j] = -1
                else:
                    break
            self.TRYTE_TO_TRITS_MAPPINGS[i] = trits2[:]

    ##循环：
    # stri:2 trits:3 
    def fromBinDicToTriDict(self,json_dict):
        new_dict = dict()
        trits = list()
        for key in json_dict:
            stri = json_dict.get(key)
            for i in range(len(stri)):
                number = ord(stri[i]
                trit5 = self.BYTE_TO_TRITS_MAPPINGS[number]
              #  trit3 = 
                trits.append(trit3)
            new_dict[key] = trits
        return new_dict

    def fromTriDictToTrytes(self, new_dict):
        for key in new_dict:
            trits = new_dict.get(key)
            for i in range(len(trits)):
                tryteNumber = self.TRYTE_TO_TRITS_MAPPINGS.index(trits[i])
                tryte = self.TRYTE_ALPHABET[tryteNumber]
            trytes = str.join(tryte)

        return tryte

    def helper(self, json_string):
        json_dict = self.getDict(json_string)
        new_dict = self.fromBinDicToTriDict(json_dict)
     #   self.change(Twonumber)
        return self.fromTriDictToTrytes(new_dict)


if __name__ == "__main__":
    obj = changeForTryts()
    print obj.helper('{"addr":"1dvffd1"}')
