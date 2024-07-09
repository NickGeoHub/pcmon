// cpp (.ino) file, code for Arduino board

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
char end = ';';
char sep = '>';

bool is_lcd_updated = 0;
int battery_percentage;
bool battery_is_charing;

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
            delay(10);
        }
        return (millis()-start_time+1);
    } else {  // given timeout
        while (Serial.available() == 0){
            delay(10);
            if (millis()-start_time >= limit_ms){
                return 0;
            }
        }
    }
}


void update_all(){
    /* updates variables only */
    command_send("get", "all");
    // is_lcd_updated = false;
}

void update_lcd(){
    // update data shown on lcd
    delay(1000);  // why delay?
    lcd.clear();
    lcd.print("batt:");
    lcd.print(battery_percentage);
    lcd.print("%");
    if (battery_is_charing == true){lcd.print("charging");
    } else                         {lcd.print("discharg");}

    delay(1000);  // why delay?
    is_lcd_updated = true;
}

void log_add(String message){
    Serial.print("log");
    Serial.print(sep);
    Serial.print(message);
}


void log_send(){
    Serial.print(end);
}


void command_send(String cmd, String arg){
    Serial.print(cmd);
    Serial.print(sep);
    Serial.print(arg);
    Serial.print(end);
}

void act(String command_got, String arguments_got){
    // change arduino variables or ..

    log_add("X: act(" + command_got + "," + arguments_got + ")");
    log_send();

    if (command_got == "HELLO_ARDUINO" and arguments_got == ""){
        return;
    }

    is_lcd_updated = false;
    if (command_got == "batt_p"){
        battery_percentage = arguments_got.toInt();
    } else if (command_got == "batt_c"){
        if (arguments_got == "0"){
            battery_is_charing = false;
        } else {
            battery_is_charing = true;
        }
    } else if (command_got == "charge_pc"){
        // TODO add waring if (is_charging == 1 and got this message anyway)
        log_add("X: digitalWrite(relayPin,"+arguments_got+")");
        log_send();
        if (arguments_got == "0"){
            digitalWrite(relayPin, 0);
        } else {
            digitalWrite(relayPin, 1);
        }
    } else {
        log_add("E: Unknown cmd,arg: " + command_got + "," + arguments_got + ".");
        log_send();
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
    wait_serial();  // wait forever
    command_got = Serial.readStringUntil(sep);
    arguments_got = Serial.readStringUntil(end);


    lcd.clear();
    if (command_got=="HELLO_ARDUINO" and arguments_got == ""){
        lcd.print("Sucess in PC!");
        Serial.print("HELLO_PYTHON");
        Serial.print(sep);
        Serial.print(end);
    } else {
        // if port not python port....
        lcd.print("gotAnotherMesage");
        while (1){delay(100);}
    }
    log_add("got message: " + command_got + "#(sep)" + arguments_got + "#(end)");
    log_send();

    delay(3000);

    update_lcd();
}


// ============================================== LOOP
void loop() {
    for (int i = 0; i < 1000; i++){
    // TODO it is possiple to manually change {i} value by while loop and
    //   if {i%n} matchs decrease i by 1 to loop on same command again
    //   it avoids time loss for nothing
        // --------------------------------------
        if (wait_serial(200) == 0){  // no data
            // = delay

        } else {  // data
            // update message got, data analize
            // = update values
            // = update lcd 
            command_got = Serial.readStringUntil(sep);
            arguments_got = Serial.readStringUntil(end);
            act(command_got, arguments_got);
        }

        // --------------------------------------
        // TODO holding putton fills serial buffer and error occurs
        // local or global variable issues
        // overloading serial causes data loss
        if (pulse_in(butt_pin, 0, 800) == 0){
            // no button click
        } else {
            // button click
            update_all();
        }

        // --------------------------------------
        if (i % 50 == 0){
            update_all();
        }
        if (i % 100 == 0){
            // periodically check if python is still connected
            // FIXME arduino may get another data instead of hello response
            Serial.print("HELLO_PYTHON");
            Serial.print(sep);
            Serial.print(end);
            wait_serial();
            command_got = Serial.readStringUntil(sep);
            arguments_got = Serial.readStringUntil(end);
            act(command_got, arguments_got);
        }
        if (i % 10 == 0){
            if (is_lcd_updated == false){
                update_lcd();
            }
        }
    }
}
