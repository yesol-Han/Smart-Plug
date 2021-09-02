#include <SoftwareSerial.h> // Arduino IDE <1.6.6>
#include <PZEM004T.h>

PZEM004T pzem(11, 12); // (RX,TX) connect to TX,RX of PZEM
SoftwareSerial mySerial(5, 4); //블루투스의 Tx, Rx핀을 4번 5번핀으로 설정
IPAddress ip(192, 168, 1, 1); // required by pzem but not used
const int LED_R = 8;
const int LED_G = 7;
const int LED_B = 2;

float time_A = 0, time_B = 0;
int number = 0;
String number_S = "";
byte n_byte[8];
char order;

void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ; //시리얼통신이 연결되지 않았다면 코드 실행을 멈추고 무한 반복
  }
  while (true) {
    Serial.println("Connecting...");
    if (pzem.setAddress(ip)) break;
    delay(1000);
  }
  mySerial.begin(9600);

  pinMode(LED_R, OUTPUT);
  pinMode(LED_G, OUTPUT);
  pinMode(LED_B, OUTPUT);
  Serial.println("Hello World!");//실행됬는지 확인
}

void loop() {
  time_B = millis();
  while (time_B - time_A >= 2000) {
    time_A = time_B;

    number = pzem.energy(ip);
    Serial.println(number);
    number_S = String(number);  //number = power
    
    for(int i=0; i < number_S.length() ;i++){
      n_byte[i] = number_S.charAt(i);
      mySerial.write(n_byte[i]);
    }
    mySerial.write('/');
  }
  
  mySerial.listen();
  while (mySerial.available()) {  //블루투스를 통해 입력된 데이터 수신
    order = mySerial.read();
    Serial.print(order);

    //LED동작
    switch (int(order)){
      case 48: {
        digitalWrite(LED_R, 0);
        break;
      }
      case 49: {
        digitalWrite(LED_R, 1);
        break;
      }
      case 50: {
        digitalWrite(LED_G, 0);
        break;
      }
      case 51: {
        digitalWrite(LED_G, 1);
        break;
      }
      case 52: {
        digitalWrite(LED_B, 0);
        break;
      }
      case 53: {
        digitalWrite(LED_B, 1);
        break;
      }
    }
  }
}
