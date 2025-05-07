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
	Serial.print("A0:");
	int a0 = analogRead(A0);
	double a0f = (((double)a0)/adc_max) * 3.3d;
	Serial.print(a0);
	Serial.print(" ");
	Serial.println(a0f);
	Serial.print("A1:");
	int a1 = analogRead(A1);
	double a1f = (((double)a1)/adc_max) * 3.3d;
	Serial.print(a1);
	Serial.print(" ");
	Serial.println(a1f);
	Serial.print("A2:");
	int a2 = analogRead(A2);
	double a2f = (((double)a2)/adc_max) * 3.3d;
	Serial.print(a2);
	Serial.print(" ");
	Serial.println(a2f);
	Serial.print("A3:");
	int a3 = analogRead(A3);
	double a3f = (((double)a3)/adc_max) * 3.3d;
	Serial.print(a3);
	Serial.print(" ");
	Serial.println(a3f);
	// Calculate sunangles
	Serial.print("Sunangle alpha:");
	float Qtot = a0 + a1 + a2 + a3;
	float tanalpha = (a3 + a0 - a1 - a2)/Qtot * maxTanAlpha; // y direction 
	float tanbeta = (a0 + a1 - a2 - a3)/Qtot * maxTanAlpha; // x direction
	Serial.print(" ");
	Serial.println(tanalpha);
	Serial.print("Sunangle beta");
	Serial.print(" ");
	Serial.println(tanbeta);
	Serial.flush();
	uint32_t elapsed = micros() - start;
	if (elapsed < period)
	{
		delayMicroseconds(period - elapsed);
	}
}