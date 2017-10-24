#include <SoftwareSerial.h> // для передачи данных на ПК
#include <SPI.h>            // для передачи данных между arduino и ad7714

#define DRDY_pin 9
#define BUFFER_pin 6
#define STANDBY_pin 7
#define RESET_pin 8
#define POL_pin 2
#define SS_pin 10
#define MOSI_pin 11
#define MISO_pin 12
#define SCK_pin 13

int spi_mode = SPI_MODE1;
int bit_FIRST = MSBFIRST;
int spi_clk_div = SPI_CLOCK_DIV2;

char channel = 'Z';
char temp = 'W';



unsigned long my_transfer(byte b)
{
  unsigned long btl;
  boolean DRDY_flag = true;
  digitalWrite(SS_pin, LOW);
  delay(5);
  while (DRDY_flag) {

    if (digitalRead(DRDY_pin) == 0) {
      DRDY_flag = false;
    }
  }

  btl = SPI.transfer(b);

  digitalWrite(SS_pin, HIGH);
  return btl;
}


void my_init(int b) {

  my_transfer(0b00100110);// запись в высокмй регистр
  delay(100);

  my_transfer(0b01001111);
  delay(100);

  my_transfer(0b00110110);
  delay(100);

  my_transfer(0b10100000);
  delay(100);

  my_transfer(0b00010111);
  delay(100);

  my_transfer(b);
  delay(100);
}

void setup() {
  pinMode(DRDY_pin, INPUT);        // 2ой пин - ввод
  pinMode(BUFFER_pin, OUTPUT);      // 6ой пин - вывод
  digitalWrite(BUFFER_pin, LOW);    // Низкий уровень на 6ой пин, чтобы в обычный режим
  pinMode(STANDBY_pin, OUTPUT);    // 7ой пин - вывод
  digitalWrite(STANDBY_pin, HIGH);  // высокий уровень на 7ой пин, чтобы в обычный режим
  pinMode(RESET_pin, OUTPUT);      // 8ой пин - вывод
  digitalWrite(RESET_pin, LOW);    // высокий уровень на 8ой пин, чтобы не было сброса
  pinMode(POL_pin, OUTPUT);        // 9ый пин - вывод
  digitalWrite(POL_pin, HIGH);      // высокий уровень на 9ой пин, выбор полярности
  pinMode(SS_pin, OUTPUT);          // 10ый пин - вывод
  SPI.begin();                        // Начало работы с SPI
  SPI.setClockDivider(spi_clk_div); // делитель тактового сигнала
  SPI.setBitOrder(bit_FIRST);        // левый бит - первый бит LSBFIRST
  SPI.setDataMode(spi_mode);        // полярность приёма
  digitalWrite(SS_pin, LOW);        // низкий уровень на 10ый пин, сразу выбор АЦП
  Serial.begin(9600);                // инициализация СОМ-порта
  delay(100);
  digitalWrite(RESET_pin, HIGH);
  my_init(0x20);
}

void getValue()
{
  unsigned long int bt1;
  unsigned long int bt2;
  unsigned long int bt3;

  bt1 = (unsigned long)my_transfer(0xFF);
  bt1 = bt1 << 16;


  bt2 = (unsigned long)my_transfer(0xFF);
  bt2 = bt2 << 8;

  bt3 = (unsigned long)my_transfer(0xFF);

  bt1 = bt1 | bt2 | bt3;
  Serial.print((bt1 * 5.0 / 16777215) - 2.5, 12);
  Serial.print("A   ");
  Serial.println(analogRead(5));
}

void getCH16()
{
  my_transfer(B01011000);
  getValue();
}

void getCH26()
{
  my_transfer(B01011001);
  getValue();
}

void getCH36()
{
  my_transfer(B01011010);
  getValue();
}

void getCH46()
{
  my_transfer(B01011011);
  getValue();
}

void getCH12()
{
  my_transfer(B01011100);
  getValue();
}

void getCH34()
{
  my_transfer(B01011101);
  getValue();
}

void getCH56()
{
  my_transfer(B01011110);
  getValue();
}

void getCH66()
{
  my_transfer(B01011111);
  getValue();
}

void loop()
{
  
  
  
  temp = Serial.read();
  if (channel != temp)
  {
    delay(1000);
  }
  
  channel = temp;
  switch (channel)
  {
    case 'A': getCH16(); break;
    case 'B': getCH26(); break;
    case 'C': getCH36(); break;
    case 'D': getCH46(); break;
    case 'E': getCH12(); break;
    case 'F': getCH34(); break;
    case 'G': getCH56(); break;
    case 'H': getCH66(); break;
    case '1': my_init(0x20); break;
    case '2': my_init(0x24); break;
    case '3': my_init(0x28); break;
    case '4': my_init(0x2C); break;
    case '5': my_init(0x30); break;
    case '6': my_init(0x34); break;
    case '7': my_init(0x38); break;
    case '8': my_init(0x3C); break;
  }

  Serial.println('D');

  
}


