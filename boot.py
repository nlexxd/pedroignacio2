import libraries, time, components, network, ubinascii
from components import servo_izquierda_a, servo_izquierda_b, servo_derecha_a, servo_derecha_b, control

time.sleep(5)

def saniao(inst):
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
        time.sleep(1)
        saniao("stop")
        time.sleep(1.5)
        print("izquierda A REVERSE")
        servo_izquierda_a.speed(-100)
        time.sleep(1)
        saniao("stop")
        time.sleep(1.5)
        print("izquierda B FORWARD")
        servo_izquierda_b.speed(100)
        time.sleep(1)
        saniao("stop")
        time.sleep(1.5)
        print("izquierda B REVERSE")
        servo_izquierda_b.speed(-100)
        time.sleep(1)
        saniao("stop")
        time.sleep(1.5)
        print("derecha A FORWARD")
        servo_derecha_a.speed(-100)
        time.sleep(1)
        saniao("stop")
        time.sleep(1.5)
        print("derecha A REVERSE")
        servo_derecha_a.speed(100)
        time.sleep(1)
        saniao("stop")
        time.sleep(1.5)
        print("derecha B FORWARD")
        servo_derecha_b.speed(-100)
        time.sleep(1)
        saniao("stop")
        time.sleep(1.5)
        print("derecha B REVERSE")
        servo_derecha_b.speed(100)
        time.sleep(1)
        saniao("stop")
        time.sleep(1.5)
        
saniao("test")

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

    else:
        saniao("stop")
    
    print(sn)
    time.sleep_ms(30)
