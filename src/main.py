

# ---------------------------------------------------------------------------- #
#                                                                              #
#   Module:       main.py                                                      #
#   Author:       sandr                                                        #
#   Created:      3/3/2026, 2:49:56 PM                                         #
#   Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# git test
# Library imports
from vex import *


brain = Brain()
controller = Controller()


# Initial program actions
brain.screen.clear_screen()


# sensors
inertial = Inertial(Ports.PORT20)


# drivetrain motors
motorL1 = Motor(Ports.PORT1, GearSetting.RATIO_6_1, True)
motorL2 = Motor(Ports.PORT2, GearSetting.RATIO_6_1, True)
motorL3 = Motor(Ports.PORT3, GearSetting.RATIO_6_1, True)
motorR1 = Motor(Ports.PORT10, GearSetting.RATIO_6_1, False)
motorR2 = Motor(Ports.PORT9, GearSetting.RATIO_6_1, False)
motorR3 = Motor(Ports.PORT8, GearSetting.RATIO_6_1, False)


drivetrainRight = MotorGroup(motorR1, motorR2, motorR3)
drivetrainLeft = MotorGroup(motorL1, motorL2, motorL3)

# the purpose of this function is to take the target heading and find the direction with the smaller degree, so it can get there
# faster
def getAlpha(targetHeading):
   alpha0 = targetHeading - inertial.heading()
   alpha1 = alpha0 + 360
   alpha_min = min(abs(alpha0), abs(alpha1))  
   if alpha_min == abs(alpha0):
       return alpha0
   else:
       return alpha1
  
def turnTo(targetDegrees):
  
   #proportionalCoefficient = 0.395
   #new kp
   proportionalCoefficient = 0.39
   minSpeed = 2


   t = 3


   while True:


       errorDegrees = getAlpha(targetDegrees)
      


       # print to screen for debugging


       brain.screen.set_cursor(1, 0)
       brain.screen.clear_row(1, Color.RED)
       brain.screen.clear_row(2, Color.GREEN)
       brain.screen.clear_row(3, Color.BLUE)


       brain.screen.print("Heading = ", inertial.heading(), "Degrees", opaque=False)
       brain.screen.next_row()
       brain.screen.print("Error = ", errorDegrees, "Degrees", opaque=False)


       speed = proportionalCoefficient * errorDegrees

# flips the sign of the minimum speed based on the direction of the error
       errorSign = errorDegrees / abs(errorDegrees)



       minSpeedCorrected = errorSign * minSpeed



       drivetrainLeft.set_velocity(minSpeedCorrected + speed,PERCENT)
       drivetrainRight.set_velocity(-(minSpeedCorrected + speed),PERCENT)


       if abs(errorDegrees) < 0.5: #if error is small
           t += -1
       else:
           t = 3
      
       if t == 0:
           drivetrainLeft.set_velocity(0,PERCENT) #stop motors
           drivetrainRight.set_velocity(0,PERCENT)
           return #end loop and function


       wait(20, MSEC)


def autonomous():
   brain.screen.clear_screen()
   brain.screen.print("autonomous code")
   # place automonous code here


def user_control():






   drivetrainLeft.set_velocity(0,PERCENT)
   drivetrainRight.set_velocity(0,PERCENT)


   drivetrainLeft.spin(FORWARD)
   drivetrainRight.spin(FORWARD)
  


   brain.screen.clear_screen()
   brain.screen.print("driver control")
   # place driver control in this while loop


   inertial.calibrate()


   while inertial.is_calibrating() == True:
       wait(20, MSEC)


   inertial.set_heading(0,DEGREES)


   turnTo(90)
   wait(1000)
   turnTo(0)
   wait(1000)








# create competition instance
comp = Competition(user_control, autonomous)


# actions to do when the program starts
brain.screen.clear_screen()
