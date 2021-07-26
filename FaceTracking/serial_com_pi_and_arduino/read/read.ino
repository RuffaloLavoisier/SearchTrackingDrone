int i=0;

void setup() {
	Serial.begin(9600);
}

void loop() {
float data = Serial.parseFloat();
//int i_data = data;
Serial.println((data*10));	


}
