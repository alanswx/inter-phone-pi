from ptwinkle import Twinkle
import time
from gpiozero import LED, Button


ringer = LED(17)
offhook = Button(21)
waiting_to_answer = False

mTP = ''

def tick():
  global waiting_to_answer
  # check GPIO (off hook)
  if (waiting_to_answer and not offhook.is_pressed):
       ringer.on()
       time.sleep(1)
       ringer.off()
       time.sleep(1)
  if (waiting_to_answer and offhook.is_pressed):
       waiting_to_answer = False
       mTP.answer()
  if (waiting_to_answer == False  and offhook.is_pressed):
        mTP.call("101")
        waiting_to_answer = False
  





def callback(event, *args):
    global mTP
    global waiting_to_answer

    if (event!="tick"): print("callback")
    if event=="registration_succeeded":
        uri, expires = args
        print("registratiom succeeded, uri: %s, expires in %s seconds"%(uri, expires))
        # The module keeps the session, you havent to register
        #mTP.message("name@domain", "Hello")
        #mTP.call("name@domain")

    if event=="tick":
        tick()
        #print("tick")
    if event=="new_msg":
        msg=args[0]
        print("new_msg!: "+str(msg))
    
    if event=="incoming_call":
        call=args[0]
        print("call: "+str(call))
        print(args)
        waiting_to_answer = True

    if event=="cancelled_call":
        line=args[0]
        print("call cancelled, line: %s"%(line))
        waiting_to_answer = False
        
    if event=="failed_call":
        line=args[0]
        print("failed_call, line: %s"%(line))
        
    if event=="dtmf_received":
        line=args[0]
        key=args[0]
        print("dtmf_received, line: %s, key: %s"%(key))
        
    if event=="answered_call":
        call=args[0]
        print("answered: %s"%(str(call)))
        
    if event=="ended_call":
        line=args[0]
        print("call ended, line: %s"%(line))

mTP = Twinkle(callback)  
#mTP.set_account("103","10.0.1.220","pisunfish")
mTP.set_account_by_file("/home/alans/intercom/user")
mTP.run()
