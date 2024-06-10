// board file
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27, 16, 2);

// pins
#define butt_pin 13

// values
#define delay_time 1

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


void wait_serial(int limit_ms = 0){
    // waits serial data to appear
    if (limit_ms == 0){
        while (Serial.available() == 0){delay(5);}
    } else {
        int start_time = millis();
        while (Serial.available() == 0){
            delay(10);
            if (millis()-start_time >= limit_ms*1000){
                delay(20);
                return (millis()-start_time);
            }
        }
    }
    delay(20);
    return 0;
}



// ============================================== SETUP
void setup() {
    // pins
    pinMode(butt_pin, INPUT_PULLUP);

    // lcd
    lcd.init();
    lcd.backlight();
    lcd.clear();
    lcd.print("Please run .py");

    // Serial
    Serial.begin(9600);
    wait_serial();
    String a = Serial.readStringUntil(";");
    lcd.clear();
    lcd.setCursor(0,1);
    lcd.print(a);
    lcd.setCursor(0,0);
    if (a=="HELLO_ARDUINO;"){
        lcd.print("message got!");
        Serial.print("HELLO_PYTHON;");
    } else {
        // if port not python port....
        lcd.print("gotAnotherMesage");
        while (1){delay(100);}
    }
    delay(1000);
}


// ============================================== LOOP
void loop() {

// output
    lcd.clear();
    lcd.print("batt:");
    wait_serial(100);
    if (Serial.readStringUntil(";") == "charge_pc;"){
        lcd.clear();
        lcd.print("pc is carging!");
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
