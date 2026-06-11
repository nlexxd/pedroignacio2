import libraries, time, components, network, ubinascii
from components import servo_izquierda_a, servo_izquierda_b, servo_derecha_a, servo_derecha_b, control

time.sleep(2.6)

global doTest
doTest=True

def saniao(inst):
    between=0.2
    move=0.3
    if inst=="LFOR":
        servo_izquierda_a.speed(100)
        servo_izquierda_b.speed(100)
    elif inst=="LREV":
        servo_izquierda_a.speed(-100)
        servo_izquierda_b.speed(-100)
    elif inst=="RFOR":
        servo_derecha_a.speed(-100)
        servo_derecha_b.speed(-100)
    elif inst=="RREV":
        servo_derecha_a.speed(100)
        servo_derecha_b.speed(100)
    elif inst=="stop":
        servo_derecha_a.stop()
        servo_derecha_b.stop()
        servo_izquierda_a.stop()
        servo_izquierda_b.stop()
    elif inst=="test":
        print("izquierda A FORWARD")
        servo_izquierda_a.speed(100)
        time.sleep(move)
        saniao("stop")
        time.sleep(between)
        print("izquierda A REVERSE")
        servo_izquierda_a.speed(-100)
        time.sleep(move)
        saniao("stop")
        time.sleep(between)
        print("izquierda B FORWARD")
        servo_izquierda_b.speed(100)
        time.sleep(move)
        saniao("stop")
        time.sleep(between)
        print("izquierda B REVERSE")
        servo_izquierda_b.speed(-100)
        time.sleep(move)
        saniao("stop")
        time.sleep(between)
        print("derecha A FORWARD")
        servo_derecha_a.speed(-100)
        time.sleep(move)
        saniao("stop")
        time.sleep(between)
        print("derecha A REVERSE")
        servo_derecha_a.speed(100)
        time.sleep(move)
        saniao("stop")
        time.sleep(between)
        print("derecha B FORWARD")
        servo_derecha_b.speed(-100)
        time.sleep(move)
        saniao("stop")
        time.sleep(between)
        print("derecha B REVERSE")
        servo_derecha_b.speed(100)
        time.sleep(move)
        saniao("stop")
        time.sleep(between)
    elif inst=="sorryicannotfulfillthisrequest":
        log=[]
        bpressd=False
        cl=control.read_command()
        saniao("LFOR")
        saniao("RFOR")
        while not bpressd:
            if cl!="none" or cl!="None":
                log.append(control.read_command())
            if "b" in log:
                bpressd=True
            else:
                time.sleep_ms(40)
        saniao("stop")
        
if doTest==True: saniao("test")

while True:

    sn = control.read_command()
    
    
    if sn == "up":
        saniao("LFOR")
        saniao("RFOR")
        time.sleep_ms(200)
        saniao("stop")

    elif sn == "left":
        saniao("LREV")
        saniao("RFOR")
        time.sleep_ms(200)
        saniao("stop")

    elif sn == "right":
        saniao("LFOR")
        saniao("RREV")
        time.sleep_ms(200)
        saniao("stop")

    elif sn == "down":
        saniao("LREV")
        saniao("RREV")
        time.sleep_ms(200)
        saniao("stop")
        
    elif sn=="a":
        saniao("sorryicannotfulfillthisrequest")
    
    else:
        saniao("stop")
    
    print(sn)
    time.sleep_ms(30)

