#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CS1237 電流測量數據分析器
Current Measurement Data Analyzer for CS1237 ADC System

此腳本用於分析由data_logger.py生成的CSV數據文件，
提供基本的統計分析和視覺化功能。

使用方法:
python data_analyzer.py [csv_file_path]

作者: GitHub Copilot
日期: 2025-07-13
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
from pathlib import Path
import argparse

class CS1237DataAnalyzer:
    def __init__(self, csv_file_path):
        """
        初始化數據分析器
        
        Args:
            csv_file_path (str): CSV文件路徑
        """
        self.csv_file_path = Path(csv_file_path)
        self.data = None
        
    def load_data(self):
        """載入CSV數據"""
        try:
            print(f"📁 載入數據文件: {self.csv_file_path}")
            self.data = pd.read_csv(self.csv_file_path)
            
            # 轉換時間戳列為datetime格式
            self.data['Timestamp'] = pd.to_datetime(self.data['Timestamp'])
            
            print(f"✅ 成功載入 {len(self.data)} 筆數據")
            return True
            
        except FileNotFoundError:
            print(f"❌ 找不到文件: {self.csv_file_path}")
            return False
        except Exception as e:
            print(f"❌ 載入數據時發生錯誤: {e}")
            return False
            
    def basic_statistics(self):
        """計算基本統計數據"""
        if self.data is None:
            print("❌ 請先載入數據")
            return
            
        print("\n" + "="*60)
        print("📊 基本統計分析")
        print("="*60)
        
        # 數據概覽
        print(f"📈 數據點數量: {len(self.data)}")
        print(f"⏰ 記錄時間範圍: {self.data['Timestamp'].min()} 到 {self.data['Timestamp'].max()}")
        
        # 計算總記錄時長
        start_time = self.data['Timestamp'].min()
        end_time = self.data['Timestamp'].max()
        duration = (end_time - start_time).total_seconds()
        print(f"⌛ 總記錄時長: {duration:.2f} 秒")
        
        # ADC數據統計
        adc_stats = self.data['ADC_Raw_Value'].describe()
        print(f"\n🔢 ADC原始值統計:")
        print(f"   平均值: {adc_stats['mean']:,.0f}")
        print(f"   中位數: {adc_stats['50%']:,.0f}")
        print(f"   標準差: {adc_stats['std']:,.0f}")
        print(f"   最小值: {adc_stats['min']:,.0f}")
        print(f"   最大值: {adc_stats['max']:,.0f}")
        
        # 電流數據統計
        current_stats = self.data['Current_A'].describe()
        print(f"\n⚡ 電流值統計 (安培):")
        print(f"   平均值: {current_stats['mean']:.6f} A")
        print(f"   中位數: {current_stats['50%']:.6f} A")
        print(f"   標準差: {current_stats['std']:.6f} A")
        print(f"   最小值: {current_stats['min']:.6f} A")
        print(f"   最大值: {current_stats['max']:.6f} A")
        
        # 數據穩定性分析
        current_cv = (current_stats['std'] / abs(current_stats['mean'])) * 100
        print(f"   變異係數: {current_cv:.2f}%")
        
    def plot_data(self, save_plot=True):
        """繪製數據圖表"""
        if self.data is None:
            print("❌ 請先載入數據")
            return
            
        print("\n📈 生成數據圖表...")
        
        # 設定中文字體
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 創建子圖
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('CS1237 電流測量數據分析', fontsize=16, fontweight='bold')
        
        # 計算經過時間 (以秒為單位)
        start_time = self.data['Timestamp'].min()
        elapsed_seconds = (self.data['Timestamp'] - start_time).dt.total_seconds()
        
        # 圖1: 電流隨時間變化
        ax1.plot(elapsed_seconds, self.data['Current_A'], 'b-', linewidth=1, alpha=0.7)
        ax1.set_xlabel('時間 (秒)')
        ax1.set_ylabel('電流 (A)')
        ax1.set_title('電流隨時間變化')
        ax1.grid(True, alpha=0.3)
        
        # 圖2: ADC原始值隨時間變化
        ax2.plot(elapsed_seconds, self.data['ADC_Raw_Value'], 'r-', linewidth=1, alpha=0.7)
        ax2.set_xlabel('時間 (秒)')
        ax2.set_ylabel('ADC原始值')
        ax2.set_title('ADC原始值隨時間變化')
        ax2.grid(True, alpha=0.3)
        
        # 圖3: 電流值直方圖
        ax3.hist(self.data['Current_A'], bins=50, alpha=0.7, color='green', edgecolor='black')
        ax3.set_xlabel('電流 (A)')
        ax3.set_ylabel('頻次')
        ax3.set_title('電流值分布直方圖')
        ax3.grid(True, alpha=0.3)
        
        # 圖4: ADC vs 電流散點圖
        ax4.scatter(self.data['ADC_Raw_Value'], self.data['Current_A'], alpha=0.6, s=1)
        ax4.set_xlabel('ADC原始值')
        ax4.set_ylabel('電流 (A)')
        ax4.set_title('ADC原始值 vs 電流關係')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_plot:
            # 生成圖表文件名
            plot_filename = self.csv_file_path.stem + '_analysis.png'
            plot_path = self.csv_file_path.parent / plot_filename
            
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            print(f"💾 圖表已保存: {plot_path}")
        
        plt.show()
        
    def export_summary(self):
        """匯出分析摘要"""
        if self.data is None:
            print("❌ 請先載入數據")
            return
            
        summary_filename = self.csv_file_path.stem + '_summary.txt'
        summary_path = self.csv_file_path.parent / summary_filename
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("CS1237 電流測量數據分析摘要\n")
            f.write("="*50 + "\n\n")
            
            f.write(f"數據文件: {self.csv_file_path.name}\n")
            f.write(f"分析時間: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write(f"數據點數量: {len(self.data)}\n")
            f.write(f"記錄時間範圍: {self.data['Timestamp'].min()} 到 {self.data['Timestamp'].max()}\n")
            
            # 計算總記錄時長
            start_time = self.data['Timestamp'].min()
            end_time = self.data['Timestamp'].max()
            duration = (end_time - start_time).total_seconds()
            f.write(f"總記錄時長: {duration:.2f} 秒\n\n")
            
            # ADC統計
            adc_stats = self.data['ADC_Raw_Value'].describe()
            f.write("ADC原始值統計:\n")
            f.write(f"  平均值: {adc_stats['mean']:,.2f}\n")
            f.write(f"  標準差: {adc_stats['std']:,.2f}\n")
            f.write(f"  最小值: {adc_stats['min']:,.0f}\n")
            f.write(f"  最大值: {adc_stats['max']:,.0f}\n\n")
            
            # 電流統計
            current_stats = self.data['Current_A'].describe()
            f.write("電流值統計 (安培):\n")
            f.write(f"  平均值: {current_stats['mean']:.6f}\n")
            f.write(f"  標準差: {current_stats['std']:.6f}\n")
            f.write(f"  最小值: {current_stats['min']:.6f}\n")
            f.write(f"  最大值: {current_stats['max']:.6f}\n")
            
            current_cv = (current_stats['std'] / abs(current_stats['mean'])) * 100
            f.write(f"  變異係數: {current_cv:.2f}%\n")
            
        print(f"📄 分析摘要已保存: {summary_path}")
        
    def run_analysis(self):
        """執行完整分析"""
        if not self.load_data():
            return
            
        self.basic_statistics()
        self.plot_data()
        self.export_summary()
        
        print(f"\n✅ 分析完成！")

def list_csv_files():
    """列出data資料夾中的CSV文件"""
    data_dir = Path("data")
    if not data_dir.exists():
        return []
        
    csv_files = list(data_dir.glob("current_measurement_*.csv"))
    return sorted(csv_files, key=lambda x: x.stat().st_mtime, reverse=True)

def main():
    parser = argparse.ArgumentParser(description='CS1237電流測量數據分析器')
    parser.add_argument('csv_file', nargs='?', help='CSV數據文件路徑')
    args = parser.parse_args()
    
    if args.csv_file:
        csv_file_path = args.csv_file
    else:
        # 如果沒有指定文件，列出可用的CSV文件
        csv_files = list_csv_files()
        
        if not csv_files:
            print("❌ 在data資料夾中找不到CSV文件")
            print("請先運行data_logger.py來生成數據文件")
            return
            
        print("🔍 找到以下CSV數據文件:")
        for i, csv_file in enumerate(csv_files, 1):
            file_size = csv_file.stat().st_size / 1024  # KB
            mod_time = pd.Timestamp.fromtimestamp(csv_file.stat().st_mtime)
            print(f"   {i}. {csv_file.name} ({file_size:.1f} KB, {mod_time.strftime('%Y-%m-%d %H:%M:%S')})")
            
        try:
            choice = input(f"\n請選擇要分析的文件 (1-{len(csv_files)}) [預設: 1]: ").strip()
            if not choice:
                choice = "1"
            index = int(choice) - 1
            
            if 0 <= index < len(csv_files):
                csv_file_path = csv_files[index]
            else:
                print("❌ 無效的選擇")
                return
                
        except (ValueError, KeyboardInterrupt):
            print("\n❌ 操作已取消")
            return
    
    # 執行分析
    analyzer = CS1237DataAnalyzer(csv_file_path)
    analyzer.run_analysis()

if __name__ == "__main__":
    main()
