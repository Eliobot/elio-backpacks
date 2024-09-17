void setup()
{
  pinMode(6, OUTPUT); // Set pin 6 as an output
}

void loop() // Run over and over again
{
  digitalWrite(6, HIGH); // Set pin 6 high
  delay(1000); // Wait for 1000 millisecond(s)
  digitalWrite(6, LOW); // Set pin 6 low
  delay(1000); // Wait for 1000 millisecond(s)
}