# CS1237 電流測量專案

這是一個基於 CS1237 ADC 晶片的高精度電流測量專案，使用 Arduino 和 PlatformIO 開發環境。

## 專案概述

本專案使用 CS1237 24位元精密 ADC 晶片來進行高精度的電流測量。CS1237 是一個低雜訊、高解析度的類比數位轉換器。

## 硬體需求

- Arduino Uno (或相容板)
- CS1237 ADC 模組
- 電流感測器/分流電阻
- 跳線

## 腳位連接

| CS1237 模組 | Arduino Uno |
|-------------|-------------|
| SCLK        | Digital Pin 6 |
| DATA        | Digital Pin 5 |
| VCC         | 5V |
| GND         | GND |

## 軟體需求

### Arduino開發環境
- [PlatformIO](https://platformio.org/) IDE 或 VS Code with PlatformIO extension
- Arduino Framework

### Python數據記錄環境 (可選)
- Python 3.7 或更高版本
- pyserial 套件 (用於序列埠通訊)
- pandas, matplotlib 套件 (用於數據分析，可選)

## 安裝與設定

1. 複製或下載此專案到本地端
2. 在 PlatformIO 中開啟專案資料夾
3. 依賴函式庫會自動安裝（iarduino_ADC_CS1237）
4. 連接硬體元件
5. 編譯並上傳程式碼到 Arduino

## 使用說明

### 編譯專案
```bash
platformio run
```

### 上傳到開發板
```bash
platformio run --target upload
```

### 監控序列輸出
```bash
platformio device monitor --baud 115200
```

## 🐍 Python 數據記錄器

本專案包含完整的Python數據記錄和分析工具，可以自動記錄Arduino發送的測量數據。

### 快速開始

1. **安裝Python依賴套件**
   ```bash
   pip install -r requirements.txt
   ```

2. **方法一：使用便利腳本 (Windows)**
   ```bash
   run_logger.bat
   ```

3. **方法二：直接運行Python腳本**
   ```bash
   python data_logger.py
   ```

### 數據記錄功能

- 🔗 **自動序列埠連接**：自動檢測可用的COM埠
- 📊 **實時數據記錄**：解析並記錄ADC原始值和電流數據
- 📁 **自動文件管理**：以時間戳命名CSV文件
- ⏰ **時間戳記錄**：每筆數據包含精確的時間資訊
- 🛡️ **錯誤處理**：優雅處理連接中斷和數據錯誤

### CSV輸出格式

| 欄位 | 說明 | 範例 |
|------|------|------|
| Timestamp | ISO格式時間戳 | 2025-07-13T14:30:25.123456 |
| ADC_Raw_Value | ADC原始值 | 12345 |
| Current_A | 電流值(安培) | 0.001234 |

### 數據分析工具

專案包含數據分析腳本，提供：

```bash
python data_analyzer.py
```

- 📈 **統計分析**：平均值、標準差、變異係數等
- 📊 **圖表生成**：時間序列圖、分布直方圖、散點圖
- 📄 **摘要報告**：自動生成分析摘要文件
- 🎨 **視覺化**：高質量的數據圖表

### 數據文件說明

所有數據文件都存儲在 `data/` 資料夾中：

- `current_measurement_YYYYMMDD_HHMMSS.csv` - 原始測量數據
- `current_measurement_YYYYMMDD_HHMMSS_analysis.png` - 分析圖表
- `current_measurement_YYYYMMDD_HHMMSS_summary.txt` - 分析摘要

## 程式碼功能

### setup() 函式
- 初始化序列通訊 (115200 baud)
- 配置 CS1237 ADC 參數：
  - 脈衝寬度：30 微秒
  - 參考電壓：5.09V
  - 轉換速率：10Hz
  - 增益係數：128倍
  - ADC 通道：0 (通道A)
- 顯示所有配置參數

### loop() 函式
- 每秒讀取一次 ADC 值
- 顯示原始 ADC 數值和對應電壓值
- 輸出格式：`ADC=數值, V=電壓A.`

## ADC 規格

- **解析度**：24位元
- **測量範圍**：±8388607 (ADC 原始值)
- **電壓範圍**：±0.5 VrefIn / PGA
- **轉換速率**：10, 40, 640, 1280 Hz
- **增益選項**：1x, 2x, 64x, 128x

## 輸出示例

```
VrefOut輸出 開啟。
數據更新速率 10 Hz。
增益係數 128x。
使用ADC通道 0。
SCL線上的脈衝寬度 30 微秒。
VrefIn參考電壓 5.09 V。
ADC=12345, V=0.00123A.
ADC=12350, V=0.00124A.
...
```

## 檔案結構

```
current_measurement/
├── src/
│   └── main.cpp              # 主程式碼
├── lib/                      # 自定義函式庫
├── include/                  # 標頭檔
├── test/                     # 測試檔案
├── data/                     # 數據記錄資料夾
│   ├── current_measurement_*.csv     # 測量數據文件
│   ├── *_analysis.png               # 分析圖表
│   └── *_summary.txt               # 分析摘要
├── platformio.ini            # PlatformIO 專案配置
├── requirements.txt          # Python依賴套件清單
├── data_logger.py           # Python數據記錄器
├── data_analyzer.py         # Python數據分析器
├── run_logger.bat          # Windows便利啟動腳本
└── README.md               # 專案說明文件
```

## 配置參數說明

| 參數 | 預設值 | 可選值 | 說明 |
|------|--------|--------|------|
| 脈衝寬度 | 5μs | 5-255μs | SCL 線上的脈衝寬度，長線路時需增加 |
| 參考電壓 | 5V | 1.5V-Vcc+0.1V | VrefIn 輸入的參考電壓 |
| 轉換速率 | 10Hz | 10/40/640/1280Hz | 新數據的更新頻率 |
| 增益係數 | 128x | 1x/2x/64x/128x | 可程式化增益放大器 |
| 通道選擇 | 0 | 0/2/3 | 0=通道A, 2=溫度, 3=內部短路 |

## 故障排除

### 常見錯誤訊息
- **初始化錯誤**：檢查硬體連接和電源
- **寬度錯誤**：脈衝寬度參數超出範圍
- **VrefOut錯誤**：參考電壓輸出設定失敗
- **VrefIn錯誤**：參考電壓輸入超出範圍
- **速度錯誤**：轉換速率參數無效
- **增益錯誤**：增益係數參數無效
- **通道錯誤**：ADC 通道選擇無效

### Python數據記錄器問題
- **序列埠連接失敗**：
  - 檢查Arduino是否正確連接
  - 確認COM埠號碼 (可在裝置管理員中查看)
  - 關閉其他可能使用序列埠的程式
- **數據解析錯誤**：
  - 確認Arduino程式正在運行
  - 檢查串列輸出格式是否正確
- **Python套件安裝失敗**：
  - 更新pip: `python -m pip install --upgrade pip`
  - 使用管理員權限運行命令提示字元
- **無法創建CSV文件**：
  - 檢查資料夾寫入權限
  - 確保磁碟空間充足

### 除錯步驟
1. 確認硬體連接正確
2. 檢查電源供應穩定
3. 驗證 CS1237 模組是否正常工作
4. 查看序列監控器的錯誤訊息

## 授權

此專案使用 MIT 授權條款。

## 參考資料

- [CS1237 晶片規格書](https://www.chipsemi.com/)
- [iarduino_ADC_CS1237 函式庫](https://github.com/iarduino/iarduino_ADC_CS1237)
- [PlatformIO 官方文件](https://docs.platformio.org/)

## 版本歷史

- v1.0.0 - 初版發布，基本 CS1237 ADC 功能實作

## 聯絡資訊

如有問題或建議，請透過 GitHub Issues 回報。
