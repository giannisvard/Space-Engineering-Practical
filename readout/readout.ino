#include <Arduino.h>
#include <math.h>
#include <AccelStepper.h>

constexpr int DIR_PIN = 2;	// Direction pin
constexpr int STEP_PIN = 3; // Step pin

AccelStepper stepper(AccelStepper::DRIVER, STEP_PIN, DIR_PIN);

constexpr uint8_t ADC_BITS = 16; // ADC resolution in bits

char buffer[100];
int i = 0;

uint32_t last_time = 0;

void setup()
{
	analogReadResolution(ADC_BITS); // Set ADC resolution to 16 bits
	pinMode(LED_BUILTIN, OUTPUT);
	Serial.begin(1000000, SERIAL_8N1);
	digitalWrite(LED_BUILTIN, HIGH);
	while (!Serial)
		; // Wait for Serial Monitor to open
	digitalWrite(LED_BUILTIN, LOW);
	stepper.setMaxSpeed(1000);
	stepper.setAcceleration(1000);
	memset(buffer, 0, sizeof(buffer));
	last_time = micros();
}

bool led_state = false;
bool moving = false;

#define SEP ",\t"

constexpr uint32_t frequency = 100u;						   // Hz
constexpr uint32_t period = 1000000u / frequency;		   // us
constexpr uint32_t average_samples = 100u;			   // number of samples to average
constexpr double adc_max = (double)(pow(2, ADC_BITS) - 1); // 16-bit ADC max value
float maxTanAlpha = std::tan(59.2 * PI / 180);			   // maximum angle in both axes

void loop()
{
	uint32_t start = micros();
	if (last_time + period <= start)
	{
		digitalWrite(LED_BUILTIN, led_state = !led_state);
		uint32_t q1 = 0;
		uint32_t q2 = 0;
		uint32_t q3 = 0;
		uint32_t q4 = 0;
		for(uint32_t i = 0; i < average_samples; i++) {
			q1 += analogRead(0); // Read ADC channel 0
			q2 += analogRead(1); // Read ADC channel 1
			q3 += analogRead(2); // Read ADC channel 2
			q4 += analogRead(3); // Read ADC channel 3
		}
		double Qtot = q1 + q2 + q3 + q4;
		double tanalpha = (q1 + q4 - q2 - q3) / Qtot * maxTanAlpha; // y direction
		double tanbeta = (q1 + q2 - q3 - q4) / Qtot * maxTanAlpha;  // x direction
		double alpha = std::atan(tanalpha) * 180 / PI;
		double beta = std::atan(tanbeta) * 180 / PI;
		Serial.print(start);
		Serial.print(SEP);
		Serial.print(stepper.currentPosition());
		Serial.print(SEP);
		Serial.print(q1);
		Serial.print(SEP);
		Serial.print(q2);
		Serial.print(SEP);
		Serial.print(q3);
		Serial.print(SEP);
		Serial.print(q4);
		Serial.print(SEP);
		Serial.print(Qtot);
		Serial.print(SEP);
		Serial.print(tanalpha);
		Serial.print(SEP);
		Serial.print(tanbeta);
		Serial.print(SEP);
		Serial.print(alpha);
		Serial.print(SEP);
		Serial.println(beta);
		last_time += period;
	}
	while (Serial.available())
	{
		stepper.run();
		buffer[i] = Serial.read();
		if (buffer[i] == '\n' || i >= 100)
		{
			if (strncmp(buffer, "move:", 5) == 0)
			{
				int pos = atoi(buffer + 5);
				stepper.moveTo(pos);
				Serial.print("Moving to: ");
				Serial.println(pos);
				moving = true;
			}
			else if (strncmp(buffer, "rst", 3) == 0)
			{
				stepper.setCurrentPosition(0);
				Serial.println("Resetting position to 0");
			}
			i = 0;
			memset(buffer, 0, sizeof(buffer));
		}
		else
		{
			i++;
		}
	}
	if (moving)
	{
		if (stepper.distanceToGo() == 0)
		{
			moving = false;
			Serial.println("Movement completed");
		}
	}
	else
	{
		stepper.setSpeed(0);
	}
	stepper.run();
}