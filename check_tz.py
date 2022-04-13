import time
print ("time.timezone")
print (time.timezone)
print ("time.localtime()")
print (time.localtime())
print ("time.localtime().tm_isdst")
print (time.localtime().tm_isdst)
print ("time.altzone")
print (time.altzone)
offset = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
print ("offset")
print (offset)
