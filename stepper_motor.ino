const int dirPin = 2;
const int stepPin = 3;
const int stepsPerRevolution = 200;

void setup()
{
    // Declare pins as Outputs
    pinMode(stepPin, OUTPUT);
    pinMode(dirPin, OUTPUT);
    digitalWrite(dirPin, LOW);
    Serial.begin(115200);
}

void loop()
{
    // Read serial from Python
    String data = Serial.readStringUntil('\n');
    
    // Start motor if it's a start message and motor is not already running
    if (data == "start") {
       spinMotor();
    }
}

// Method to spin motor
void spinMotor() {
    // Spin motor slowly
    Serial.println("running");
    for (int x = 0; x < stepsPerRevolution; x++) {
        digitalWrite(stepPin, HIGH);
        delayMicroseconds(2000);
        digitalWrite(stepPin, LOW);
        delayMicroseconds(2000);
    }
    Serial.println("stopped");
}
