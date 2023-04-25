import pywhatkit as pwk

no = int(input("Enter Phone NO To Send Message\n=>"))
message = str(input("Enter Message to Send to Give No\n=>"))
hour = (input("Enter Hours\n=>")
minute = (input("Enter minute\n=>")

pwk.sendwhatmsg(no,message,hour,minute)