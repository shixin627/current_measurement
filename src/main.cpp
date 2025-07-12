#include <Arduino.h>
#include <iarduino_ADC_CS1237.h>                                               // 引入基於CS1237晶片的ADC函式庫
iarduino_ADC_CS1237 adc(6,5);                                                // 建立函式庫iarduino_ADC_CS1237的物件，指定腳位(SCLK, DATA)。可以使用任何Arduino腳位。
                                                                               // 除了begin以外的所有函式庫功能都是選用的，如果預設值符合您的需求。
void setup(){                                                                  //
     bool i;                                                                   //
     Serial.begin(115200);         while( !Serial );                             //
//   設定(配置)ADC：                                                            //
     i=adc.setPulseWidth(30);    if( !i ){ Serial.println("寬度錯誤"  ); }     // 設定SCL線上的脈衝寬度。預設為5微秒。只有在長線路時才需要增加。此函式必須在begin()初始化之前調用。
     i=adc.begin();              if( !i ){ Serial.println("初始化錯誤"  ); }    // 初始化ADC。
     i=adc.setPinVrefOut(true);  if( !i ){ Serial.println("VrefOut錯誤"); }    // 開啟VrefOut輸出。可能的值：true=開啟(預設)，false=關閉。開啟的VrefOut輸出將會輸出平滑的晶片供電電壓(Vcc)，可以連接到VrefIn輸入。
     i=adc.setVrefIn(5.09);       if( !i ){ Serial.println("VrefIn錯誤" ); }    // 設定VrefIn輸入的參考電壓。預設為5V。VrefIn輸入可以接收1.5V到Vcc+0.1V的外部電壓，或是來自VrefOut的晶片供電電壓(Vcc)。
     i=adc.setSpeed(10);         if( !i ){ Serial.println("速度錯誤"  ); }     // 設定轉換速率為10Hz。可能的值：10, 40, 640, 1280 Hz。這是新數據可讀取的頻率。預設為10 Hz。
     i=adc.setPGA(128);            if( !i ){ Serial.println("增益錯誤"   ); }    // 設定增益係數。可能的值：1, 2, 64, 128。預設為128。可測量的電壓範圍為 ±0.5 VrefIn / PGA。
     i=adc.setChannel(0);        if( !i ){ Serial.println("通道錯誤"); }      // 選擇ADC通道。可能的值：0, 2, 3。0-通道A(預設)，1-保留，2-溫度，3-內部短路。
//   讀取ADC設定：                                                              //
     bool     pin   = adc.getPinVrefOut();                                     // 獲取VrefOut輸出狀態。函式返回true-開啟或false-關閉。
     uint16_t speed = adc.getSpeed();                                          // 獲取當前轉換速率(Hz)。函式返回新數據的更新頻率：10, 40, 640, 或 1280 Hz。
     uint8_t  gain  = adc.getPGA();                                            // 獲取當前增益係數。函式返回值：1, 2, 64, 或 128。
     uint8_t  chan  = adc.getChannel();                                        // 獲取使用中的ADC通道。函式返回其中一個通道：0, 2, 或 3。
     uint16_t width = adc.getPulseWidth();                                     // 獲取脈衝寬度(微秒)。函式返回庫當前使用的SCL線上的脈衝和暫停時間(微秒)。
     float    Vref  = adc.getVrefIn();                                         // 獲取VrefIn參考電壓值，用於getVoltage()函式計算電壓。
//   顯示讀取的ADC設定：                                                         //
     Serial.println( (String) "VrefOut輸出 "+(pin?"開":"關")+"啟。"    );       //
     Serial.println( (String) "數據更新速率 "+speed+" Hz。"    );               //
     Serial.println( (String) "增益係數 "+gain+"x。"             );             //
     Serial.println( (String) "使用ADC通道 "+chan+"。"            );            //
     Serial.println( (String) "SCL線上的脈衝寬度 "+width+" 微秒。");            //
     Serial.println( (String) "VrefIn參考電壓 "+Vref+" V。"       );           //
}                                                                              //
                                                                               //
void loop(){                                                                   //
//   在顯示器上顯示ADC值和電壓：                                                 //
     int32_t i=adc.analogRead(); Serial.print("ADC="); Serial.print(i);        // 讀取並顯示ADC的帶符號值，範圍從0到±8388607
     float   j=adc.getVoltage(); Serial.print(", V="); Serial.print(j,5);      // 獲取並顯示ADC輸入電壓，範圍從0到±0.5 VrefIn。Vin = ADC*VrefIn/(2^24-1)/PGA
     Serial.println("A."); delay(1000);                                        //
}                                                                              //