#include <Arduino.h>
#include <iarduino_ADC_CS1237.h>

/**
 * CS1237 Current Measurement System
 * 基於CS1237晶片的高精度電流測量系統
 * 
 * Hardware Connections 硬體連接:
 * - CS1237 SCLK -> Arduino Pin 6
 * - CS1237 DATA -> Arduino Pin 5
 * - VCC -> 5V
 * - GND -> GND
 */

// 初始化 CS1237 ADC 物件，指定腳位 (SCLK=6, DATA=5)
iarduino_ADC_CS1237 adc(6, 5);

void setup() {
  // 初始化序列通訊
  Serial.begin(115200);
  while (!Serial) {
    ; // 等待序列埠連接
  }
  
  Serial.println("=== CS1237 電流測量系統啟動 ===");
  Serial.println();
  
  // ADC 配置結果檢查變數
  bool configResult;
  
  // ==================== ADC 參數配置 ====================
  
  // 設定 SCL 線上的脈衝寬度 (長線路時需要增加，此設定必須在 begin() 之前)
  configResult = adc.setPulseWidth(30);
  if (!configResult) {
    Serial.println("❌ 錯誤: 脈衝寬度設定失敗");
  }
  
  // 初始化 ADC
  configResult = adc.begin();
  if (!configResult) {
    Serial.println("❌ 錯誤: ADC 初始化失敗");
    return; // 初始化失敗則停止執行
  }
  
  // 開啟 VrefOut 輸出 (輸出平滑的晶片供電電壓)
  configResult = adc.setPinVrefOut(true);
  if (!configResult) {
    Serial.println("❌ 錯誤: VrefOut 輸出設定失敗");
  }
  
  // 設定參考電壓 (範圍: 1.5V 到 Vcc+0.1V)
  configResult = adc.setVrefIn(5.09);
  if (!configResult) {
    Serial.println("❌ 錯誤: 參考電壓設定失敗");
  }
  
  // 設定轉換速率 (可選: 10, 40, 640, 1280 Hz)
  configResult = adc.setSpeed(10);
  if (!configResult) {
    Serial.println("❌ 錯誤: 轉換速率設定失敗");
  }
  
  // 設定增益係數 (可選: 1, 2, 64, 128)
  configResult = adc.setPGA(128);
  if (!configResult) {
    Serial.println("❌ 錯誤: 增益係數設定失敗");
  }
  
  // 選擇 ADC 通道 (0=通道A, 2=溫度, 3=內部短路)
  configResult = adc.setChannel(0);
  if (!configResult) {
    Serial.println("❌ 錯誤: ADC 通道選擇失敗");
  }
  
  // ==================== 讀取並顯示 ADC 配置 ====================
  
  // 讀取當前配置參數
  bool vrefOutStatus = adc.getPinVrefOut();
  uint16_t currentSpeed = adc.getSpeed();
  uint8_t currentGain = adc.getPGA();
  uint8_t currentChannel = adc.getChannel();
  uint16_t pulseWidth = adc.getPulseWidth();
  float referenceVoltage = adc.getVrefIn();
  
  // 顯示配置資訊
  Serial.println("📋 當前 ADC 配置:");
  Serial.println("┌─────────────────────────────────────┐");
  Serial.println("│ 參數               │ 值            │");
  Serial.println("├─────────────────────────────────────┤");
  Serial.print("│ VrefOut 輸出        │ ");
  Serial.println(vrefOutStatus ? "開啟           │" : "關閉           │");
  Serial.print("│ 數據更新速率        │ ");
  Serial.print(currentSpeed);
  Serial.println(" Hz         │");
  Serial.print("│ 增益係數           │ ");
  Serial.print(currentGain);
  Serial.println("x            │");
  Serial.print("│ ADC 通道           │ ");
  Serial.print(currentChannel);
  Serial.println("             │");
  Serial.print("│ 脈衝寬度           │ ");
  Serial.print(pulseWidth);
  Serial.println(" μs        │");
  Serial.print("│ 參考電壓           │ ");
  Serial.print(referenceVoltage, 2);
  Serial.println(" V         │");
  Serial.println("└─────────────────────────────────────┘");
  Serial.println();
  Serial.println("🔄 開始測量... (每秒更新一次)");
  Serial.println();
}

/**
 * 主循環函式 - 持續讀取並顯示電流測量值
 */
void loop() {
  // 讀取 ADC 原始數值 (24位元有符號整數，範圍: ±8388607)
  int32_t adcRawValue = adc.analogRead();
  
  // 計算對應的電壓值 (公式: Vin = ADC × VrefIn / (2^24-1) / PGA)
  float voltageValue = adc.getVoltage();
  
  // 顯示測量結果
  Serial.print("ADC: ");
  Serial.print(adcRawValue);
  Serial.print(" | Current: ");
  Serial.print(voltageValue, 9);
  Serial.println(" A");
  
  // 等待 1 秒後進行下次測量
  delay(1000);
}