int Led = 10;

void setup() {
  Serial.begin(9600);
  pinMode(Led, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    char c = Serial.read();
    if (c == '0') {
      digitalWrite(Led, LOW);
    }
    else if (c == '1') {
      digitalWrite(Led, HIGH);
    }
  }
}
