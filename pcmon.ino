// board file
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27, 16, 2);

// pins
#define butt_pin 13
#define relayPin 12

// values
#define delay_time 1
#define WAIT_CHAR 20 

String command_got;
String argumrnts_got;

int battery_percentage;
bool battery_charge_state;

int pulse_in(uint8_t pin, uint8_t state, int timeout_ms){
    /* new pulse_in function for miliseconds
    returns 0 if timeout or int value ms needed to pulse
    pin - pin;  state - HIGH or LOW;
    timeout_ms -timeout milliseconds;*/
    unsigned long start = millis();
    while (digitalRead(pin) != state){
        delay(10);
        if ((millis()-start) >= timeout_ms){
            return 0;
        }
    }
    return (millis()-start);
}


unsigned long wait_serial(unsigned long limit_ms = 0){
    /* waits for serial data to appear.returns:
           0 - if timeout
           unsigned long - if data appeared */
    
    unsigned long start_time = millis();
    if (limit_ms == 0){
        while (Serial.available() == 0){
            delay(5);
        }
        delay(WAIT_CHAR);  // wait char to send
        return (millis()-start_time);
    } else {  // given timeout
        while (Serial.available() == 0){
            delay(5);
            if (millis()-start_time >= limit_ms){
                return 0;
            }
        }
    }
}


void act(String command_got, String argumrnts_got){
    lcd.clear();
    lcd.print(command_got);
    lcd.setCursor(0, 1);
    lcd.print(argumrnts_got);
    if (command_got == "batt_p"){
        wait_serial();
        battery_percentage = argumrnts_got.toInt();
    } else if (command_got == "charge_pc"){
        if (argumrnts_got == "0"){
            digitalWrite(relayPin, 0);}
        else {
            digitalWrite(relayPin, 1);
        }
    } else if (command_got == "hello python"){
    delay(1);  // pass
    }
}


// ============================================== SETUP
void setup() {
    // pins
    pinMode(butt_pin, INPUT_PULLUP);
    pinMode(relayPin, OUTPUT);

    // lcd
    lcd.init();
    lcd.backlight();
    lcd.clear();
    lcd.print("Please run .py");

    // Serial
    Serial.begin(9600);
    wait_serial();
    command_got = Serial.readStringUntil(';');
    lcd.clear();
    lcd.setCursor(0,1);
    lcd.print(command_got);
    lcd.setCursor(0,0);
    if (command_got=="HELLO_ARDUINO"){
        lcd.print("message got!");
        Serial.print("HELLO_PYTHON");
    } else {
        // if port not python port....
        lcd.print("gotAnotherMesage");
        while (1){delay(100);}
    }
    delay(1000);
}


// ============================================== LOOP
void loop() {
    // =-=-=-=-=-=-=-=-=-=-====-=-=-=-=-==-=-==-=-=-=-=-/
    // output
    lcd.clear();
    lcd.print("loop started!");


    if (wait_serial(400) == 0){  // no data
        // = delay
        // some delay and user interupt analize
        delay(20000);
        Serial.print("hello>python;");
        wait_serial();
        command_got = Serial.readStringUntil('>');
        argumrnts_got = Serial.readStringUntil(';');
        lcd.clear();
        lcd.print("acting");
        act(command_got, argumrnts_got);


    } else {  // data
        // update message got, data analize
        // = update values
        // = update lcd
        command_got = Serial.readStringUntil('>');
        argumrnts_got = Serial.readStringUntil(';');
        act(command_got, argumrnts_got);
    }


    
    // lcd.print(var_battery_percentage);
    // lcd.print("%,");
    // lcd.print(var_charge_state_real);
    // lcd.setCursor(0, 1);
    // lcd.print("lu:");
    // lcd.print(last_updated_sec);


    // act
    delay(100);

    // UPDATING starts here -----
    if (pulse_in(butt_pin, 0, delay_time*1000) != 0){
    // if button interupted:
    // digitalWrite(butt_led_pin, 1);
    // update_all();  // update values
    }
}
