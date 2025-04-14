const int buttonPin = A0;  // Пин, куда подключены кнопки

void setup() {
  Serial.begin(9600);
}

void loop() {
  int buttonValue = analogRead(buttonPin);  // Чтение значения
  int button = getPressedButton(buttonValue);  // Определение кнопки
  
  if (button != 0) {
    Serial.println(button);  // Отправка номера кнопки (1-5)
  }
  // Serial.println(buttonValue);
  delay(50);  // Небольшая задержка для стабильности
}

// Функция для определения кнопки (настрой под свои значения!)
int getPressedButton(int value) {
  if (value < 400)   return 0;
  if (value < 477)   return 4;
  if (value < 533)   return 3;
  if (value < 584)   return 5;
  if (value < 639)   return 2;
  if (value < 700)   return 1;
  else               return 0;  // 0 = не нажато
}