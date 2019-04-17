import sys ; sys.path += ['.', '../..']
from SharedCode import Function
from CryptoCode.MD4 import MD4


md4 = MD4(b"hello")
md4.nextStep()
md4.printSectorsAsHash()
md4.nextStep()
md4.printSectorsAsHash()


