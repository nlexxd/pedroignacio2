from libraries import LedRGB, Servo, Ultrasound, Infrared, WalkerBotV1

SERVOS_RIGHT_PIN_A=15
SERVOS_RIGHT_PIN_B=17
SERVOS_LEFT_PIN_A=16
SERVOS_LEFT_PIN_B=18

servo_derecha_a=Servo(SERVOS_RIGHT_PIN_A, continuous=True)
servo_derecha_b=Servo(SERVOS_RIGHT_PIN_B, continuous=True)
servo_izquierda_a=Servo(SERVOS_LEFT_PIN_A, continuous=True)
servo_izquierda_b=Servo(SERVOS_LEFT_PIN_B, continuous=True)

control = WalkerBotV1()
