#include <Arduino.h>
#include <math.h>

constexpr uint8_t ADC_BITS = 16; // ADC resolution in bits

void setup()
{
	analogReadResolution(ADC_BITS); // Set ADC resolution to 16 bits
	pinMode(LED_BUILTIN, OUTPUT);
	Serial.begin(1000000, SERIAL_8N1);
	digitalWrite(LED_BUILTIN, HIGH);
	while(!Serial); // Wait for Serial Monitor to open
	Serial.flush();
	digitalWrite(LED_BUILTIN, LOW);


}

bool led_state = false;

constexpr uint32_t frequency = 1u; // Hz
constexpr uint32_t period = 1000000u/frequency; // us
constexpr double adc_max = (double)(pow(2, ADC_BITS)-1); // 16-bit ADC max value
float maxTanAlpha = std::tan(59.2 * PI / 180); //maximum angle in both axes



void loop()
{
	uint32_t start = micros();
	digitalWrite(LED_BUILTIN, led_state=!led_state);
	int q1 = analogRead(A0);
	int q2 = analogRead(A1);
	int q3 = analogRead(A2);
	int q4 = analogRead(A3);
	float Qtot = q1 + q2 + q3 + q4;
	float tanalpha = (q1+ q4 - q2 -q3)/Qtot * maxTanAlpha; // y direction 
	float tanbeta = (q1+ q2 - q3 - q4)/Qtot * maxTanAlpha; // x direction
	float alpha = std::atan(tanalpha) * 180 / PI;
	float beta = std::atan(tanbeta) * 180 / PI;
	Serial.print(start);
	Serial.print("\t");
	Serial.print(q1);
	Serial.print("\t");
	Serial.print(q2);
	Serial.print("\t");
	Serial.print(q3);
	Serial.print("\t");
	Serial.print(q4);
	Serial.print("\t");
	Serial.print(Qtot);
	Serial.print("\t");
	Serial.print(tanalpha);
	Serial.print("\t");
	Serial.print(tanbeta);
	Serial.print("\t");
	Serial.print(alpha);
	Serial.print("\t");
	Serial.println(beta);
	

	uint32_t elapsed = micros() - start;
	if (elapsed < period)
	{
		delayMicroseconds(period - elapsed);
	}
}