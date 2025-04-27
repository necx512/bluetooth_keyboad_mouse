#complete
hid_descriptor=bytes.fromhex("05010906a101850175019508050719e029e715002501810295017508810395057501050819012905910295017503910395067508150026ff000507190029ff8100c005010902A10185020901A1000509190129031500250175019503810275059501810105010930093109381581257F750895038106C0C0")


# complete mouse only
hid_descriptor=bytes.fromhex("05010902A10185020901A1000509190129031500250175019503810275059501810105010930093109381581257F750895038106C0C0")


#first
#hid_descriptor=bytes.fromhex("05010906a101850175019508050719e029e715002501810295017508810395057501050819012905910295017503910395067508150026ff000507190029ff8100c005010902A10185020901A1000509190129031500250175019503810205010930093109381581257F750895038106C0C0")

#second
#hid_descriptor=bytes.fromhex("05010906a101850175019508050719e029e715002501810295017508810395057501050819012905910295017503910395067508150026ff000507190029ff8100c005010902A10185020901A1000509190129031500250175059501810105010930093109381581257F750895038106C0C0")





#hid_descriptor=bytes.fromhex("05010906a101850175019508050719e029e715002501810295017508810395057501050819012905910295017503910395067508150026ff000507190029ff8100c005010902A10185020901A100050919012903150025017501950305010930093109381581257F750895038106C0C0")

i=0
err = False
while(i<len(hid_descriptor)):
    bSize=hid_descriptor[i]&3
    bType=(hid_descriptor[i]>>2)&3
    bTag=(hid_descriptor[i]>>4)&15

    if( (bSize == 0b10) and (bType == 0b11) and bTag == 0b1111):
        print("Long item detected")
        print("Not implemented yet. Check the USB Device Class Definition for Human Interface Devices (HID) Specification")
        exit(0)
    else:
        print(f"Short item of size {bSize}.", end=" ")
        if(bType==0):
            print("Main type.", end=" ")
            if(bTag == 0b1000):
              print("Input tag.", end=" ")
            elif(bTag == 0b1001):
              print("Output tag.", end=" ")
            elif(bTag == 0b1011):
              print("Feature tag.", end=" ")
            elif(bTag == 0b1010):
              print("Collection tag.", end=" ")
            elif(bTag == 0b1100):
              print("End Collection tag.", end=" ")
        elif(bType==1):
            print("Global type.", end=" ")
            if(bTag == 0b0000):
              print("Usage Page tag.", end=" ")
            elif(bTag == 0b0001):
              print("Logical Minimum tag.", end=" ")
            elif(bTag == 0b0010):
              print("Logical Maximum tag.", end=" ")
            elif(bTag == 0b0011):
              print("Physical Minimum tag.", end=" ")
            elif(bTag == 0b0100):
              print("Physical Maximum tag.", end=" ")
            elif(bTag == 0b0101):
              print("Unit exponent tag.", end=" ")
            elif(bTag == 0b0110):
              print("Unit tag.", end=" ")
            elif(bTag == 0b0111):
              print("Report Size tag.", end=" ")
            elif(bTag == 0b1000):
              print("Report ID tag.", end=" ")
            elif(bTag == 0b1001):
              print("Report Count tag.", end=" ")
            elif(bTag == 0b1010):
              print("Report Push tag.", end=" ")
            elif(bTag == 0b1011):
              print("Report Pop tag.", end=" ")
            else:
              print(f"Unexpected TAG {bTag}", end= " ")
              err=True
        elif(bType==2):
            print("Local type.", end=" ")
            if(bTag == 0b0000):
              print("Usage tag.", end=" ")
            elif(bTag == 0b0001):
              print("Usage Minimum tag.", end=" ")
            elif(bTag == 0b0010):
              print("Usage Maximum tag.", end=" ")
            elif(bTag == 0b0011):
              print("Designator index tag.", end=" ")
            else:
              print(f"Unexpected TAG {bTag}", end= " ")
              err=True
        else:
            print("unexpected type", end= " ")
            err=True


        if(bSize > 0):
          print("Value : ", end=" ")
          for j in range(bSize+1):
              print(hex(hid_descriptor[i+j])[2:],end=" ")
        print("")


        if(err):
            exit(0)
        i=i+1
        i=i+bSize
