// board file
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27, 16, 2);

// pins
#define butt_pin 13
#define relayPin 12

// values
#define delay_time 1
#define WAIT_CHAR 30 

String command_got;
String arguments_got;

bool is_lcd_updated = 0;

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
    return (millis()-start + 1);
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
        return (millis()-start_time+1);
    } else {  // given timeout
        while (Serial.available() == 0){
            delay(5);
            if (millis()-start_time >= limit_ms){
                return 0;
            }
        }
    }
}


void update_all(){
    // update variables only
    Serial.print("get>all;");
    // is_lcd_updated = false;
}

void update_lcd(){
    // update data shown on lcd
    delay(1000);
    lcd.clear();
    lcd.print("batt:");
    lcd.print(battery_percentage);
    lcd.print("%");
    if (battery_charge_state == true){lcd.print("charging");
    } else                           {lcd.print("discharg");}

    delay(1000);
    is_lcd_updated = true;
}

void send_log(String message){
    // act("log", message);
    Serial.print("log>");
    Serial.print(message);
    Serial.print(";");
}

void act(String command_got, String arguments_got){
    lcd.clear();
    lcd.print("act:");
    lcd.print(command_got);
    lcd.setCursor(0, 1);
    lcd.print(arguments_got);
    delay(1000);

    send_log("Acting c: " + command_got + " & a: " + arguments_got + ";");

    if (command_got == "HELLO_" and arguments_got == "ARDUINO"){
        delay(1);  // pass
        return;
    }

    is_lcd_updated = false;
    if (command_got == "batt_p"){
        battery_percentage = arguments_got.toInt();
        // lcd.clear();
        // lcd.print("bt_p>");
        // lcd.print(battery_percentage);
        // delay(1000);
    } else if (command_got == "batt_c"){
        if (arguments_got == "0"){
            battery_charge_state = false;
        } else {
            battery_charge_state = true;
        }
    } else if (command_got == "charge_pc"){
        if (arguments_got == "0"){
            digitalWrite(relayPin, 0);
            send_log("Relay turned of.");
        } else {
            digitalWrite(relayPin, 1);
            send_log("Relay turned on.");
        }
    } else {
        send_log("unknown command: " + command_got + "and arguments: " + arguments_got + ";");
        lcd.clear();
        lcd.print("c:");
        lcd.print(command_got);
        lcd.print("|a:");
        lcd.print(arguments_got);
        lcd.setCursor(0, 1);
        lcd.print("none act!");
        delay(2000);
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
    if (command_got=="HELLO_>ARDUINO"){
        lcd.print("message got!");
        Serial.print("HELLO_PYTHON");
    } else {
        // if port not python port....
        lcd.print("gotAnotherMesage");
        while (1){delay(100);}
    }
    delay(3000);

    update_all();
    update_lcd();
}


// ============================================== LOOP
void loop() {
    // =-=-=-=-=-=-=-=-=-=-====-=-=-=-=-==-=-==-=-=-=-=-/
    // output


    for (int i = 0; i < 1000; i++){
        // lcd.clear();
        // lcd.print("loop!");
        // lcd.print(Serial.available());
        // lcd.print(";i=");
        // lcd.print(i);

        // -------------------------------------
        if (pulse_in(butt_pin, 0, 800) == 0){
            // no button click
        } else {
            // button click
            update_all();
        }

        // --------------------------------------
        if (i % 100 == 0){
            Serial.print("HELLO_>PYTHON;");
            wait_serial();
            command_got = Serial.readStringUntil('>');
            arguments_got = Serial.readStringUntil(';');
            act(command_got, arguments_got);
        }
        if (is_lcd_updated == false){
            update_lcd();
        }
        if (wait_serial(200) == 0){  // no data
            // = delay
            // some delay and user interupt analize (# garet gavitane ^)

        } else {  // data
            // update message got, data analize
            // = update values
            // = update lcd
            command_got = Serial.readStringUntil('>');
            arguments_got = Serial.readStringUntil(';');
            act(command_got, arguments_got);
        }
    }
}



