import tkinter as tk
from tkinter import ttk
import locale

# 設定數字格式 (譬如加上千分位逗號)
try:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
except:
    locale.setlocale(locale.LC_ALL, '')

class SalesCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("馬尼通訊 - 銷售業績試算工具 v2.1")
        self.root.geometry("450x600")
        
        # 設定全域字型 (微軟正黑體)
        self.default_font = ("Microsoft JhengHei", 11)
        self.bold_font = ("Microsoft JhengHei", 11, "bold")      # 輸入框用
        self.result_font = ("Microsoft JhengHei", 16, "bold")    # 結果顯示用
        
        # 1. 【Enter 跳下一格】的核心邏輯
        # 綁定所有 Entry 元件，按下 Return (Enter) 時觸發 focus_next_window
        root.bind_class("Entry", "<Return>", self.focus_next_widget)

        # 建立 UI
        self.create_widgets()

    def focus_next_widget(self, event):
        """按下 Enter 跳到下一個 widget"""
        event.widget.tk_focusNext().focus()
        return "break"  # 阻止預設的行為 (例如發出系統提示音)

    def create_widgets(self):
        # 標題
        title_label = tk.Label(self.root, text="業績與獎金試算", font=("Microsoft JhengHei", 14, "bold"))
        title_label.pack(pady=15)

        # --- 輸入區塊 (Frame) ---
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10, padx=20, fill="x")

        # 欄位列表 (標籤文字, 變數名稱)
        self.entries = {}
        fields = [
            ("本月業績目標 (Target):", "target"),
            ("目前實際業績 (Actual):", "actual"),
            ("毛利率 % (Margin):", "margin"),
            ("加權係數 (選填):", "factor")
        ]

        for idx, (label_text, key) in enumerate(fields):
            # 標籤
            lbl = tk.Label(input_frame, text=label_text, font=self.default_font)
            lbl.grid(row=idx, column=0, sticky="w", pady=8)
            
            # 輸入框
            # 3. 【試算輸入】數字加粗 -> 使用 self.bold_font
            ent = tk.Entry(input_frame, font=self.bold_font, justify="right")
            ent.grid(row=idx, column=1, sticky="e", pady=8, padx=5)
            self.entries[key] = ent

        # 按鈕區
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=15)

        calc_btn = tk.Button(btn_frame, text="開始計算", command=self.calculate, 
                             font=self.bold_font, bg="#4CAF50", fg="white", width=15)
        calc_btn.pack(side="left", padx=10)
        
        # 綁定 Enter 鍵也可以觸發按鈕 (如果焦點在按鈕上)
        calc_btn.bind("<Return>", lambda event: self.calculate())

        clear_btn = tk.Button(btn_frame, text="清除", command=self.clear_fields, 
                              font=self.default_font, width=10)
        clear_btn.pack(side="left", padx=10)

        # 分隔線
        ttk.Separator(self.root, orient='horizontal').pack(fill='x', padx=20, pady=10)

        # --- 結果顯示區塊 ---
        result_frame = tk.Frame(self.root)
        result_frame.pack(pady=10, padx=20, fill="x")

        # 結果標籤
        tk.Label(result_frame, text="【計算結果】", font=self.default_font).pack(anchor="w")
        
        # 2. 【計算結果】加粗放大 -> 使用 self.result_font，並設定顏色
        self.result_label = tk.Label(result_frame, text="$0", 
                                     font=self.result_font, fg="#0055AA", pady=10)
        self.result_label.pack()

        self.info_label = tk.Label(result_frame, text="", font=("Microsoft JhengHei", 10), fg="gray")
        self.info_label.pack()

    def get_value(self, key):
        """安全取得數值，若為空則回傳 0"""
        val = self.entries[key].get().replace(",", "") # 去除可能輸入的逗號
        try:
            return float(val) if val else 0.0
        except ValueError:
            return 0.0

    def calculate(self):
        # 取得輸入值
        target = self.get_value("target")
        actual = self.get_value("actual")
        margin = self.get_value("margin")
        factor = self.get_value("factor")
        if factor == 0: factor = 1.0 # 預設係數

        # --- v2.0 核心邏輯維持不變 ---
        # 範例邏輯：(實際業績 * 毛利) * 係數 = 預估獎金/收益
        # 您可以替換回您真實的 v2.0 運算公式
        estimated_bonus = (actual * (margin / 100)) * factor
        
        achievement_rate = 0
        if target > 0:
            achievement_rate = (actual / target) * 100

        # 格式化輸出
        formatted_bonus = locale.format_string("%d", int(estimated_bonus), grouping=True)
        formatted_rate = f"{achievement_rate:.1f}%"

        # 更新顯示
        self.result_label.config(text=f"${formatted_bonus}")
        
        # 根據達成率顯示不同提示文字
        if achievement_rate >= 100:
            msg = f"恭喜達標！達成率：{formatted_rate}"
            self.result_label.config(fg="#d32f2f") # 達標顯示紅色慶祝
        else:
            msg = f"目前達成率：{formatted_rate}，請繼續加油！"
            self.result_label.config(fg="#0055AA") # 一般顯示藍色
            
        self.info_label.config(text=msg)

    def clear_fields(self):
        for ent in self.entries.values():
            ent.delete(0, tk.END)
        self.result_label.config(text="$0")
        self.info_label.config(text="")
        # 重置焦點回第一個格子
        self.entries["target"].focus_set()

if __name__ == "__main__":
    root = tk.Tk()
    app = SalesCalculatorApp(root)
    root.mainloop()
