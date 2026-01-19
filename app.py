import streamlit as st

# 1. 頁面基礎設定
st.set_page_config(page_title="馬尼通訊 - 業績試算 v2.1", layout="centered")

# 2. CSS 樣式注入：強制「輸入框數字加粗」與「結果文字特大」
st.markdown("""
    <style>
    /* 輸入框內的數字：加粗 + 放大 */
    div[data-baseweb="input"] > div > input {
        font-weight: bold !important;
        font-size: 18px !important;
        color: #000000 !important; 
    }
    /* 調整標籤 Label 的清晰度 */
    .stNumberInput label {
        font-weight: bold;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# 標題
st.markdown("## 業績與獎金試算 (v2.1)")

# --- 3. 輸入區塊 (嚴格對應 v2.0 欄位) ---

# 【欄位 1】本月業績目標 (整數)
# 修正重點：min_value, value 設為 int (0)，對應 format="%d"
target = st.number_input(
    "本月業績目標 (Target):", 
    min_value=0, 
    value=0, 
    step=1000, 
    format="%d"
)

# 【欄位 2】目前實際業績 (整數)
actual = st.number_input(
    "目前實際業績 (Actual):", 
    min_value=0, 
    value=0, 
    step=1000, 
    format="%d"
)

# 【欄位 3】毛利率 % (浮點數)
# 修正重點：min_value 設為 float (0.0)，對應 format="%.1f"
margin = st.number_input(
    "毛利率 % (Margin):", 
    min_value=0.0, 
    value=0.0, 
    step=0.5, 
    format="%.1f"
)

# 【欄位 4】加權係數 (浮點數)
factor = st.number_input(
    "加權係數 (選填):", 
    min_value=0.0, 
    value=1.00, 
    step=0.1, 
    format="%.2f"
)

# --- 4. 核心運算邏輯 (v2.0) ---
if factor == 0: 
    factor = 1.0

# 計算：(實際業績 * (毛利 / 100)) * 係數
estimated_bonus = (actual * (margin / 100.0)) * factor

# 達成率計算
achievement_rate = 0.0
if target > 0:
    achievement_rate = (actual / target) * 100.0

# --- 5. 結果顯示區塊 (加粗/放大/變色) ---
st.markdown("---")
st.markdown("### 【計算結果】")

# 顏色邏輯：達標(>=100%)顯示紅色，未達標顯示藍色
result_color = "#d32f2f" if achievement_rate >= 100 else "#0055AA"
msg = ""

if achievement_rate >= 100:
    msg = f"恭喜達標！達成率：{achievement_rate:.1f}%"
else:
    msg = f"目前達成率：{achievement_rate:.1f}%，請繼續加油！"

# 使用 HTML 呈現極大化數字 (比照您要求的視覺強化)
st.markdown(f"""
    <div style="text-align: center;">
        <span style="font-size: 50px; font-weight: 900; color: {result_color};">
            ${int(estimated_bonus):,}
        </span>
        <br>
        <span style="font-size: 18px; font-weight: bold; color: {result_color};">
            {msg}
        </span>
    </div>
""", unsafe_allow_html=True)
