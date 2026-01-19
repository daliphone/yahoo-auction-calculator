import streamlit as st

# 1. 設定頁面基本資訊
st.set_page_config(
    page_title="馬尼通訊 - 銷售業績試算工具 v2.1",
    layout="centered"
)

# 自訂 CSS 樣式：用來實現「數字加粗」與「結果放大」
st.markdown("""
    <style>
    /* 輸入框內的數字加粗 */
    .stInput input {
        font-weight: bold;
        font-size: 18px;
    }
    /* 調整標籤文字大小 */
    .stNumberInput label {
        font-size: 16px;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# 標題
st.title("📱 馬尼通訊 - 業績試算")
st.markdown("---")

# 2. 建立輸入區塊 (使用 Form 讓 Enter 鍵體驗更好)
# 使用 st.form 可以讓用戶輸入完按 Enter 就像跳下一格或直接計算
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        # 試算輸入：目標與實際
        target = st.number_input("本月業績目標 (Target)", min_value=0.0, step=1000.0, format="%d")
        actual = st.number_input("目前實際業績 (Actual)", min_value=0.0, step=1000.0, format="%d")
        
    with col2:
        # 試算輸入：毛利與係數
        margin = st.number_input("毛利率 % (Margin)", min_value=0.0, max_value=100.0, step=0.1, format="%.1f")
        factor = st.number_input("加權係數 (Factor)", value=1.0, step=0.1, format="%.2f")

# 3. 核心邏輯 (維持 v2.0 不變)
if factor == 0: 
    factor = 1.0

# 計算公式
estimated_bonus = (actual * (margin / 100)) * factor

achievement_rate = 0
if target > 0:
    achievement_rate = (actual / target) * 100

# 4. 結果顯示區塊
st.markdown("### 【計算結果】")

# 根據達成率設定顏色 (達標紅色，未達標藍色)
result_color = "#d32f2f" if achievement_rate >= 100 else "#0055AA"
result_msg = ""

if achievement_rate >= 100:
    result_msg = f"🎉 恭喜達標！達成率：{achievement_rate:.1f}%"
else:
    result_msg = f"💪 目前達成率：{achievement_rate:.1f}%，請繼續加油！"

# 使用 HTML 語法來實現「極大字體」與「加粗」
st.markdown(f"""
    <div style="
        background-color: #f0f2f6; 
        padding: 20px; 
        border-radius: 10px; 
        text-align: center; 
        border-left: 5px solid {result_color};">
        <p style="color: gray; margin: 0; font-size: 16px;">預估收益/獎金</p>
        <p style="
            color: {result_color}; 
            font-size: 50px; 
            font-weight: 900; 
            margin: 0;">
            ${int(estimated_bonus):,}
        </p>
        <p style="color: {result_color}; font-weight: bold; margin-top: 10px;">
            {result_msg}
        </p>
    </div>
""", unsafe_allow_html=True)

# 底部簡單說明
st.caption("v2.1 Streamlit Cloud 版本 | 邏輯核心：(實際業績 × 毛利率) × 係數")
