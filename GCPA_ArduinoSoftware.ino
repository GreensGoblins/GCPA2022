#include <SPI.h>
//Defined varibles
String motor;
String steps;
String dir;
String direc;
String xEND;
String yEND;
int steps_x;
int steps_y;

//Pin Varibles and their description of output
int PUL_T_x = 32; //define Pulse pin for motor 1, the single motor on the support beam
int DIR_T_x = 40; //define Direction pin for motor 1, the single motor on the support beam
int ENA_T_x = 36; //define Enable Pin for motor, the single motor on the support beam

int PUL_T_y = 44; //define Pulse pin for motors 2,3, the duel motors which run in parrellel
int DIR_T_y = 52; //define Direction pin for motors 2,3, the duel motors which run in parrellel
int ENA_T_y = 48; //define Enable Pin for motors 2,3, the duel motors which run in parrellel


int home_switch1 = 26; //define home switches pin
//Next to be defined are the sub routines which the arduino can run
//The first is the movex function which either rotates the single stepper motor clockwise or counterclockwise
//This function requires an input number of steps to take and a set direction
void movex(int steps, int dir) {
    for (int i = 0; i < steps; i++) {
        digitalWrite(ENA_T_x,HIGH);
        digitalWrite(PUL_T_x,HIGH);
        digitalWrite(DIR_T_x,dir);
        digitalWrite(PUL_T_y,LOW);
        digitalWrite(ENA_T_y,LOW);
        delayMicroseconds(1000);
        digitalWrite(PUL_T_x,LOW);
        digitalWrite(ENA_T_x,LOW);
        digitalWrite(DIR_T_x,dir);
        digitalWrite(PUL_T_y,LOW);
        digitalWrite(ENA_T_y,LOW);
        delayMicroseconds(1000);
    }
    if (!(digitalRead(home_switch1)==1 || digitalRead(home_switch1)==1 || digitalRead(home_switch1)==1)){ //if switch is activated, back off switch
        for (int i = 0; i < 200; i++) {
          digitalWrite(ENA_T_x,HIGH);
          digitalWrite(PUL_T_x,HIGH);
          digitalWrite(DIR_T_x,abs(1-dir));
          digitalWrite(PUL_T_y,LOW);
          digitalWrite(ENA_T_y,LOW);
          delayMicroseconds(1000);
          digitalWrite(PUL_T_x,LOW);
          digitalWrite(ENA_T_x,LOW);
          digitalWrite(DIR_T_x,abs(1-dir));
          digitalWrite(PUL_T_y,LOW);
          digitalWrite(ENA_T_y,LOW);
          delayMicroseconds(1000);
      }
    }

}

//The second xmove subroutine which we will define is the movex to the end. This subroutine will have the stepper motor
//continuously step until one of the two limit switches are completed. The input of a step direction decides which direction
//the stepper motor will step and by extension which limit switch will be activated.
int movex_toEND(int dir) {
    //int StepsToEnd = steps_x - steps;
    int stepCount = 0;  // number of steps the motor has taken
    
    while (digitalRead(home_switch1)==1 || digitalRead(home_switch1)==1 || digitalRead(home_switch1)==1) {  // Do this until the switch is activated   
      digitalWrite(DIR_T_x, dir);      // (HIGH = anti-clockwise / LOW = clockwise)
      digitalWrite(PUL_T_x, HIGH);
      delay(2);                       // Delay to slow down speed of Stepper
      digitalWrite(PUL_T_x, LOW);
      delay(2);
      stepCount++;
      }
      
    for (int i = 0; i < 200; i++) { //Back off switch
            digitalWrite(ENA_T_x,HIGH);
            digitalWrite(PUL_T_x,HIGH);
            digitalWrite(DIR_T_x,abs(1-dir));
            digitalWrite(PUL_T_y,LOW);
            digitalWrite(ENA_T_y,LOW);
            delay(1);
            digitalWrite(PUL_T_x,LOW);
            digitalWrite(ENA_T_x,LOW);
            digitalWrite(DIR_T_x,abs(1-dir));
            digitalWrite(PUL_T_y,LOW);
            digitalWrite(ENA_T_y,LOW);
            delay(1);
          }
   
      
  return stepCount;
}

//Simular to the movex subroutine, the movey subroutine is simularly formatted to have the stepper motor rotate either 
//clockwise or counterclockwise only this time controls the duel stepper motors which run in parrellel with one another.
void movey(int steps, int dir) {
  for (int i = 0; i < steps; i++) {
      digitalWrite(ENA_T_y,HIGH);
      digitalWrite(PUL_T_y,HIGH);
      digitalWrite(DIR_T_y,dir);
      digitalWrite(PUL_T_x,LOW);
      digitalWrite(ENA_T_x,LOW);
      delayMicroseconds(1200);
      digitalWrite(PUL_T_y,LOW);
      digitalWrite(ENA_T_y,LOW);
      digitalWrite(DIR_T_y,dir);
      digitalWrite(PUL_T_x,LOW);
      digitalWrite(ENA_T_x,LOW);
      delayMicroseconds(1200);
    }

    if (!(digitalRead(home_switch1)==1 || digitalRead(home_switch1)==1 || digitalRead(home_switch1)==1)) { //if switch is activated, back off switch
      for (int i = 0; i < 200; i++) {
            digitalWrite(ENA_T_y,HIGH);
            digitalWrite(PUL_T_y,HIGH);
            digitalWrite(DIR_T_y,abs(1-dir));
            digitalWrite(PUL_T_x,LOW);
            digitalWrite(ENA_T_x,LOW);
            delayMicroseconds(1000);
            digitalWrite(PUL_T_y,LOW);
            digitalWrite(ENA_T_y,LOW);
            digitalWrite(DIR_T_y,abs(1-dir));
            digitalWrite(PUL_T_x,LOW);
            digitalWrite(ENA_T_x,LOW);
            delayMicroseconds(1000);
          }

    }
}

//And again we'll have a second subroutine for the y limit switches as well so that we can also decide which direction we would
//like the stepper motors to turn and which limit switch we will be waiting for.
int movey_toEND(int dir) {
    //int StepsToEnd = steps_y - steps;
    int stepCount = 0;  // number of steps the motor has taken
    while (digitalRead(home_switch1)==1 || digitalRead(home_switch1)==1 || digitalRead(home_switch1)==1) {  // Do this until the switch is activated
      digitalWrite(DIR_T_y, dir);
      digitalWrite(PUL_T_y, HIGH);
      delayMicroseconds(800);                       // Delay to slow down speed of Stepper
      digitalWrite(PUL_T_y, LOW);
      delayMicroseconds(800);
      stepCount++;
      }
    for (int i = 0; i < 200; i++) { //Back off switch
          digitalWrite(ENA_T_y,HIGH);
          digitalWrite(PUL_T_y,HIGH);
          digitalWrite(DIR_T_y,abs(1-dir));
          digitalWrite(PUL_T_x,LOW);
          digitalWrite(ENA_T_x,LOW);
          delayMicroseconds(800);
          digitalWrite(PUL_T_y,LOW);
          digitalWrite(ENA_T_y,LOW);
          digitalWrite(DIR_T_y,abs(1-dir));
          digitalWrite(PUL_T_x,LOW);
          digitalWrite(ENA_T_x,LOW);
          delayMicroseconds(800);
        }
     
  return stepCount;
}


void loop() {
  // The ardino will contimue to cycle through the input string which is sent from the python code to the arduino
  // if the string contains the correct labels and inputs of steps or direction, depending upon the command, the Arduino
  // will then execute the correct subroutine.
    if(Serial.available()>0) {
    motor = Serial.readStringUntil(',');
    steps = Serial.readStringUntil(',');
    direc = Serial.readStringUntil('\n');
    
    
    if(motor == String('x')){
    movex(steps.toInt(), direc.toInt());
    }
    
    else if(motor == String('y')){
    movey(steps.toInt(), direc.toInt());
    }

    else if(motor == "xEND"){
    int step_end = movex_toEND(direc.toInt());
    Serial.println(step_end);
    }

    else if(motor == "yEND"){
    int step_end = movey_toEND(direc.toInt());
    Serial.println(step_end);
    }

    
    else if(motor == "Calibration"){
    Calibration();
    Serial.println(steps_x);
    Serial.println(steps_y);
    }
  }

}