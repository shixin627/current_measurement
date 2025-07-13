#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CS1237 電流測量數據記錄器
Current Measurement Data Logger for CS1237 ADC System

此腳本用於與Arduino微控制器通訊，接收ADC和電流測量數據，
並將數據與時間戳記錄到CSV文件中。

使用方法:
1. 確保Arduino已連接並運行CS1237測量程式
2. 執行此腳本
3. 按 Ctrl+C 停止記錄

作者: GitHub Copilot
日期: 2025-07-13
"""

import serial
import csv
import time
import datetime
import os
import sys
import re
import signal
from pathlib import Path

class CS1237DataLogger:
    def __init__(self, port='COM9', baudrate=115200, timeout=1):
        """
        初始化數據記錄器
        
        Args:
            port (str): 序列埠名稱 (Windows: COM9, Linux/Mac: /dev/ttyUSB0)
            baudrate (int): 波特率
            timeout (float): 序列埠超時時間(秒)
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection = None
        self.csv_file = None
        self.csv_writer = None
        self.data_count = 0
        self.start_time = None
        
        # 設定信號處理器以優雅地關閉程式
        signal.signal(signal.SIGINT, self.signal_handler)
        
    def signal_handler(self, signum, frame):
        """處理 Ctrl+C 信號"""
        print(f"\n\n🔴 接收到停止信號，正在安全關閉...")
        self.close()
        sys.exit(0)
        
    def create_csv_file(self):
        """創建新的CSV文件，使用當前時間作為文件名"""
        # 獲取專案目錄路徑
        project_dir = Path(__file__).parent
        
        # 創建data資料夾(如果不存在)
        data_dir = project_dir / "data"
        data_dir.mkdir(exist_ok=True)
        
        # 生成文件名：格式為 current_measurement_YYYYMMDD_HHMMSS.csv
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"current_measurement_{timestamp}.csv"
        filepath = data_dir / filename
        
        # 創建CSV文件並寫入標題行
        self.csv_file = open(filepath, 'w', newline='', encoding='utf-8')
        self.csv_writer = csv.writer(self.csv_file)
        
        # 寫入CSV標題
        headers = [
            'Timestamp',           # 時間戳
            'ADC_Raw_Value',      # ADC原始值
            'Current_A'           # 電流值(安培)
        ]
        self.csv_writer.writeheader if hasattr(self.csv_writer, 'writeheader') else None
        self.csv_writer.writerow(headers)
        self.csv_file.flush()
        
        print(f"📁 CSV文件已創建: {filepath}")
        return filepath
        
    def connect_serial(self):
        """連接到序列埠"""
        try:
            print(f"🔗 嘗試連接到序列埠: {self.port} (波特率: {self.baudrate})")
            self.serial_connection = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE
            )
            
            # 等待Arduino重新啟動
            print("⏳ 等待Arduino初始化...")
            time.sleep(2)
            
            # 清空輸入緩衝區
            self.serial_connection.flushInput()
            
            print(f"✅ 成功連接到 {self.port}")
            return True
            
        except serial.SerialException as e:
            print(f"❌ 序列埠連接失敗: {e}")
            return False
        except Exception as e:
            print(f"❌ 未知錯誤: {e}")
            return False
            
    def parse_data_line(self, line):
        """
        解析Arduino發送的數據行
        
        預期格式: "ADC: 12345 | Current: 0.00123 A"
        
        Args:
            line (str): 從Arduino接收的數據行
            
        Returns:
            tuple: (adc_value, current_value) 或 (None, None) 如果解析失敗
        """
        try:
            # 使用正規表達式解析數據
            pattern = r'ADC:\s*(-?\d+)\s*\|\s*Current:\s*([-+]?\d*\.?\d+)\s*A'
            match = re.search(pattern, line)
            
            if match:
                adc_value = int(match.group(1))
                current_value = float(match.group(2))
                return adc_value, current_value
            else:
                return None, None
                
        except (ValueError, AttributeError) as e:
            print(f"⚠️ 數據解析錯誤: {line.strip()} - {e}")
            return None, None
            
    def log_data(self, adc_value, current_value):
        """
        將數據記錄到CSV文件
        
        Args:
            adc_value (int): ADC原始值
            current_value (float): 電流值
        """
        now = datetime.datetime.now()
        
        # 準備CSV行數據 - 只記錄三個欄位
        row_data = [
            now.isoformat(),                    # ISO格式時間戳
            adc_value,                         # ADC原始值
            f"{current_value:.6f}"             # 電流值(6位小數)
        ]
        
        # 寫入CSV
        self.csv_writer.writerow(row_data)
        self.csv_file.flush()  # 立即寫入磁碟
        
        self.data_count += 1
        
        # 顯示進度
        print(f"📊 [{self.data_count:4d}] {now.strftime('%H:%M:%S')} | "
              f"ADC: {adc_value:8d} | Current: {current_value:8.5f} A")
              
    def run(self):
        """主要運行函式"""
        print("=" * 60)
        print("🚀 CS1237 電流測量數據記錄器啟動")
        print("=" * 60)
        
        # 創建CSV文件
        csv_filepath = self.create_csv_file()
        
        # 連接序列埠
        if not self.connect_serial():
            print("❌ 無法連接序列埠，程式結束")
            return
            
        self.start_time = datetime.datetime.now()
        print(f"⏰ 開始時間: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("📝 開始記錄數據... (按 Ctrl+C 停止)")
        print("-" * 60)
        
        try:
            while True:
                if self.serial_connection.in_waiting > 0:
                    try:
                        # 讀取一行數據
                        line = self.serial_connection.readline().decode('utf-8', errors='ignore').strip()
                        
                        if line:
                            # 解析數據
                            adc_value, current_value = self.parse_data_line(line)
                            
                            if adc_value is not None and current_value is not None:
                                # 記錄有效數據
                                self.log_data(adc_value, current_value)
                            else:
                                # 顯示非數據行(如配置資訊)
                                if any(keyword in line for keyword in ['ADC', '配置', '錯誤', '啟動', '開始']):
                                    print(f"ℹ️  {line}")
                                    
                    except UnicodeDecodeError:
                        print("⚠️ 字符解碼錯誤，跳過此行")
                        continue
                        
                # 短暫休眠以避免占用過多CPU
                time.sleep(0.01)
                
        except KeyboardInterrupt:
            print(f"\n\n🔴 使用者中斷程式")
        except Exception as e:
            print(f"\n\n❌ 程式運行錯誤: {e}")
        finally:
            self.close()
            
    def close(self):
        """關閉所有連接和文件"""
        end_time = datetime.datetime.now()
        
        if self.csv_file:
            self.csv_file.close()
            print(f"💾 CSV文件已保存")
            
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            print(f"🔌 序列埠連接已關閉")
            
        if self.start_time:
            duration = (end_time - self.start_time).total_seconds()
            print(f"⏱️  總記錄時間: {duration:.1f} 秒")
            print(f"📈 總記錄筆數: {self.data_count}")
            
        print("✅ 數據記錄器已安全關閉")

def list_available_ports():
    """列出可用的序列埠"""
    import serial.tools.list_ports
    
    ports = serial.tools.list_ports.comports()
    if ports:
        print("🔍 可用的序列埠:")
        for port in ports:
            print(f"   - {port.device}: {port.description}")
    else:
        print("❌ 未找到可用的序列埠")
    return [port.device for port in ports]

def main():
    """主函式"""
    # 檢查可用序列埠
    available_ports = list_available_ports()
    
    if not available_ports:
        print("請檢查Arduino是否已連接並正確安裝驅動程式")
        return
        
    # 使用預設埠或讓使用者選擇
    default_port = 'COM9' if 'COM9' in available_ports else available_ports[0]
    
    print(f"\n🎯 使用序列埠: {default_port}")
    print("   (如需使用其他埠，請修改腳本中的port參數)")
    
    # 創建並運行數據記錄器
    logger = CS1237DataLogger(port=default_port)
    logger.run()

if __name__ == "__main__":
    main()
