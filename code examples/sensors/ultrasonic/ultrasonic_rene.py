const int IO_Pin = 8;         // Pin Nr. der mit dem mit "IO"  gekennzeichneten Pin des Ultraschallsensors verbunden ist:

//*****************************************************************************************
// Ultraschallmessung / Ultrasonic Measurement
//*****************************************************************************************

const unsigned long TRIGGER_PULSE_DURATION = 10; // Dauer des Trigger-Impulses in Mikrosekunden / Duration of trigger pulse in microseconds
const unsigned long MAX_PULSE_DURATION = 23000; // Maximale Dauer des Echopulses in Mikrosekunden (entspricht 4m Entfernung) / Maximum duration of the echo pulse in microseconds (corresponds to 4m distance)
const float DISTANCE_CONVERSION_FACTOR = 0.017; // Umrechnungsfaktor von Zeit zu Entfernung (in Zentimeter pro Mikrosekunde) / Conversion factor from time to distance (in centimetres per microsecond)
const float MAX_DISTANCE = 400; // Maximale Entfernung in Zentimetern (4m) / Maximum distance in centimetres (4m)
const float MIN_DISTANCE = 2; // Minimale Entfernung in Zentimetern (2cm) / Minimum distance in centimetres (2cm)
const float ANGLE_CORRECTION_FACTOR = 1 / cos(15 * PI / 180); // Korrekturfaktor basierend auf dem Abstrahlwinkel (15 Grad) / Correction factor based on the beam angle (15 degrees)


long ultrasound_distance() {
  long duration;
  float distance;

  pinMode(IO_Pin, OUTPUT);
  digitalWrite(IO_Pin, LOW);
  delayMicroseconds(2);
  digitalWrite(IO_Pin, HIGH);
  delayMicroseconds(TRIGGER_PULSE_DURATION);
  digitalWrite(IO_Pin, LOW);

  pinMode(IO_Pin, INPUT);
  duration = pulseIn(IO_Pin, HIGH, MAX_PULSE_DURATION);

  // Umrechnung in Entfernung unter Berücksichtigung des Abstrahlwinkels / Conversion to distance taking into account the angle of radiation
  distance = (duration * DISTANCE_CONVERSION_FACTOR) * ANGLE_CORRECTION_FACTOR;

  // Begrenzung der Entfernung auf den definierten Bereich (2 cm bis 4 m) / Limiting the distance to the defined range (2 cm to 4 m)
  distance = constrain(distance, MIN_DISTANCE, MAX_DISTANCE);

  return (long)distance;
}