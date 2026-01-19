import streamlit as st
import streamlit.components.v1 as components

# --- 頁面設定 ---
st.set_page_config(page_title="馬尼奇摩拍賣計算機", page_icon="🧮", layout="wide")

# --- CSS 美化與版面調整 (維持 v2.7 風格) ---
st.markdown("""
<style>
    /* 1. 輸入框數字強制加粗、加大 */
    div[data-baseweb="input"] > div > input {
        font-weight: bold !important;
        font-size: 18px !important;
        color: #333 !important;
    }
    .stNumberInput label {
        font-weight: bold;
        color: #555;
    }
    
    /* 左側設定區的小標題優化 */
    .setting-label {
        font-size: 14px;
        font-weight: bold;
        color: #0055AA;
        margin-bottom: -10px; /* 緊湊一點 */
    }

    /* 2. 結果區塊樣式 (字體特大版) */
    .result-box-income {
        background-color: #e3f2fd; /* 實收-藍底 */
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        border: 2px solid #90caf9;
    }
    .result-box-fee {
        background-color: #fff3e0; /* 費用-橘底 */
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        border: 2px solid #ffe0b2;
    }
    .result-box-profit {
        background-color: #e8f5e9; /* 獲利-綠底 */
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        border: 2px solid #a5d6a7;
    }
    .result-box-loss {
        background-color: #ffebee; /* 虧損-紅底 */
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        border: 2px solid #ef9a9a;
    }
    
    .label-text { 
        font-size: 16px; 
        color: #444; 
        font-weight: bold; 
        margin-bottom: 5px; 
        display: block;
    }
    
    /* 結果數字：42px 超粗體 */
    .value-text { 
        font-size: 42px; 
        font-weight: 900; 
        margin: 0; 
        line-height: 1.1; 
        font-family: 'Arial', sans-serif;
    }
    
    /* 3. 頁尾 */
    .footer-text {
        font-size: 12px;
        color: #999;
        margin-top: 30px;
        border-top: 1px solid #eee;
        padding-top: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- JavaScript: Enter 跳下一格 ---
js_code = """
<script>
function bindEnterKey() {
    const inputs = parent.document.querySelectorAll('input[type="number"], input[type="text"]');
    inputs.forEach((input, index) => {
        input.removeEventListener('keydown', handleEnter); 
        input.addEventListener('keydown', handleEnter);
        
        function handleEnter(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                const nextInput = inputs[index + 1];
                if (nextInput) {
                    nextInput.focus();
                    nextInput.select();
                }
            }
        }
    });
}
setTimeout(bindEnterKey, 1000);
setInterval(bindEnterKey, 1500);
</script>
"""
components.html(js_code, height=0, width=0)

# --- 主標題 ---
st.title("🧮 馬尼奇摩拍賣計算機 GUI版")

# --- 建立三欄位佈局 (左側為設定區) ---
col_info, col_input, col_result = st.columns([0.6, 1.4, 1.2])

# ==========================================
# 【左欄】：規則說明 & 參數設定 (互動式)
# ==========================================
with col_info:
    st.subheader("⚙️ 費率設定 (可調整)")
    
    # 使用 Expander 包裹，讓畫面預設看起來整潔，展開後可修改細項
    with st.expander("📝 點此修改計費規則", expanded=True):
        
        st.markdown('<p class="setting-label">1. 商品成交手續費</p>', unsafe_allow_html=True)
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            # 輸入 2.49 代表 2.49%
            user_rate_item = st.number_input("費率 (%)", value=2.49, step=0.01, format="%.2f")
        with col_s2:
            user_max_fee = st.number_input("上限 ($)", value=498, step=1)
            
        st.markdown('<hr style="margin:5px 0;">', unsafe_allow_html=True)
        
        st.markdown('<p class="setting-label">2. 運費手續費</p>', unsafe_allow_html=True)
        col_s3, col_s4 = st.columns(2)
        with col_s3:
            user_rate_shipping = st.number_input("運費費率 (%)", value=2.49, step=0.01, format="%.2f")
        with col_s4:
            user_ship_threshold = st.number_input("免收門檻 ($)", value=300, step=50)

        st.markdown('<hr style="margin:5px 0;">', unsafe_allow_html=True)
        
        st.markdown('<p class="setting-label">3. 金流費率設定 (%)</p>', unsafe_allow_html=True)
        # 為了節省空間，將金流設定稍微緊湊排列
        user_rate_pay_other = st.number_input("其他/非信用卡", value=1.0, step=0.1, format="%.1f")
        user_rate_credit_1 = st.number_input("信用卡一次付清", value=2.0, step=0.1, format="%.1f")
        
        # 進階分期費率 (可折疊，或直接顯示)
        with st.expander("更多分期費率設定"):
            user_rate_credit_3 = st.number_input("3期0利率", value=3.0, step=0.5)
            user_rate_credit_6 = st.number_input("6期0利率", value=3.5, step=0.5)
            user_rate_credit_12 = st.number_input("12期0利率", value=6.0, step=0.5)
            user_rate_credit_24 = st.number_input("24期0利率", value=6.0, step=0.5)

    # 將使用者輸入的百分比轉為小數點 (例如 2.49 -> 0.0249)
    RATE_ITEM_FEE = user_rate_item / 100.0
    MAX_ITEM_FEE = user_max_fee
    RATE_SHIPPING_FEE = user_rate_shipping / 100.0
    SHIPPING_FREE_THRESHOLD = user_ship_threshold
    
    RATE_PAY_OTHER = user_rate_pay_other / 100.0
    RATE_PAY_CREDIT_1 = user_rate_credit_1 / 100.0
    RATE_PAY_CREDIT_3 = user_rate_credit_3 / 100.0
    RATE_PAY_CREDIT_6 = user_rate_credit_6 / 100.0
    RATE_PAY_CREDIT_12 = user_rate_credit_12 / 100.0
    RATE_PAY_CREDIT_24 = user_rate_credit_24 / 100.0
    MIN_PAYMENT_FEE = 1

    st.caption("💡 修改上方數字，右側計算將即時更新。")

# ==========================================
# 【中欄】：試算輸入
# ==========================================
with col_input:
    st.subheader("⌨️ 試算輸入")
    
    with st.container(border=True):
        
        # 1. 成本
        cost = st.number_input(
            "1. 商品成本 ($)", 
            min_value=0, 
            value=None, 
            step=10, 
            placeholder="請輸入商品成本..."
        )

        # 2. 售價
        price = st.number_input(
            "2. 商品售價 ($)", 
            min_value=0, 
            value=None, 
            step=10, 
            placeholder="請輸入平台售價..."
        )

        # 3. 數量 & 4. 運費
        c1, c2 = st.columns(2)
        with c1:
            qty = st.number_input("3. 數量", min_value=1, value=1, step=1, format="%d")
        with c2:
            shipping = st.number_input("4. 運費 ($)", min_value=0, value=60, step=10, format="%d")

        # 5. 運送 & 6. 付款
        c3, c4 = st.columns(2)
        with c3:
            ship_method = st.selectbox("5. 運送", ["一般寄送", "面交/自取"])
        with c4:
            # 這裡的選項名稱會根據左側設定的費率「動態生成」！
            # 使用 :g 格式化去除多餘的0
            payment_options = [
                f"其他付款(非信用卡){float(user_rate_pay_other):g}%",
                f"信用卡一次付清︰{float(user_rate_credit_1):g}%",
                f"信用卡3期0利率︰{float(user_rate_credit_3):g}%",
                f"信用卡6期0利率︰{float(user_rate_credit_6):g}%",
                f"信用卡12期0利率︰{float(user_rate_credit_12):g}%",
                f"信用卡24期0利率︰{float(user_rate_credit_24):g}%"
            ]
            pay_method = st.selectbox("6. 付款", payment_options, index=0)

# ==========================================
# 【右欄】：計算結果
# ==========================================
with col_result:
    st.subheader("📊 計算結果")

    if price is not None:
        # --- 核心邏輯 (使用左側動態變數) ---
        single_item_fee_raw = price * RATE_ITEM_FEE
        single_item_fee = round(single_item_fee_raw)
        is_capped = False
        if single_item_fee > MAX_ITEM_FEE:
            single_item_fee = MAX_ITEM_FEE
            is_capped = True
        fee_1_item = single_item_fee * qty

        fee_2_shipping = 0
        if ship_method == "面交/自取":
            fee_2_shipping = round(shipping * RATE_SHIPPING_FEE)
        else:
            if shipping > SHIPPING_FREE_THRESHOLD:
                fee_2_shipping = round(shipping * RATE_SHIPPING_FEE)
            else:
                fee_2_shipping = 0

        total_order_amount = (price * qty) + shipping
        
        # --- 金流費率判斷 ---
        # 透過檢查字串來匹配費率 (因為字串現在是動態的)
        if "其他付款" in pay_method:
            payment_rate = RATE_PAY_OTHER
        elif "一次付清" in pay_method:
            payment_rate = RATE_PAY_CREDIT_1
        elif "3期" in pay_method:
            payment_rate = RATE_PAY_CREDIT_3
        elif "6期" in pay_method:
            payment_rate = RATE_PAY_CREDIT_6
        elif "12期" in pay_method:
            payment_rate = RATE_PAY_CREDIT_12
        elif "24期" in pay_method:
            payment_rate = RATE_PAY_CREDIT_24
        else:
            payment_rate = RATE_PAY_OTHER 

        fee_3_payment_raw = total_order_amount * payment_rate
        fee_3_payment = round(fee_3_payment_raw)
        if total_order_amount > 0 and fee_3_payment < MIN_PAYMENT_FEE:
            fee_3_payment = MIN_PAYMENT_FEE

        total_fees = fee_1_item + fee_2_shipping + fee_3_payment
        final_income = total_order_amount - total_fees
        
        total_cost = (cost * qty) if cost is not None else 0
        gross_profit = final_income - total_cost

        # --- 視覺優化 ---
        r_col1, r_col2, r_col3 = st.columns(3)
        
        with r_col1:
            st.markdown(f"""
            <div class="result-box-income">
                <span class="label-text">預估實收</span>
                <p class="value-text" style="color:#1565c0;">${int(final_income):,}</p>
            </div>
            """, unsafe_allow_html=True)
            
        with r_col2:
            st.markdown(f"""
            <div class="result-box-fee">
                <span class="label-text">平台總手續費</span>
                <p class="value-text" style="color:#ef6c00;">${int(total_fees):,}</p>
            </div>
            """, unsafe_allow_html=True)
            
        with r_col3:
            if cost is not None:
                profit_style = "result-box-profit" if gross_profit > 0 else "result-box-loss"
                profit_color = "#2e7d32" if gross_profit > 0 else "#c62828"
                st.markdown(f"""
                <div class="{profit_style}">
                    <span class="label-text">預估毛利</span>
                    <p class="value-text" style="color:{profit_color};">${int(gross_profit):,}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-box-income" style="background-color:#f5f5f5; border-color:#ddd;">
                    <span class="label-text">預估毛利</span>
                    <p class="value-text" style="color:#ccc; font-size:24px; line-height:1.7;">待輸入<br>成本</p>
                </div>
                """, unsafe_allow_html=True)

        # --- 次要資訊 ---
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        st.markdown(f"**訂單總金額**: `${int(total_order_amount):,}`")
        
        if cost is not None and total_order_amount > 0:
            margin_rate = (gross_profit / total_order_amount) * 100
            st.progress(max(0, min(100, int(margin_rate))))
            st.caption(f"當前利潤率: {margin_rate:.1f}%")

        # --- 詳細公式與費用 ---
        with st.expander("📝 查看詳細計算公式與費用明細", expanded=False):
            st.markdown("#### 1. 費用明細")
            current_rate_display = f"{float(payment_rate*100):g}%"
            
            # 使用 user_rate_item 等變數顯示當前設定
            st.markdown(f"""
            * **成交手續費**: `${fee_1_item}` (費率 {user_rate_item}%, 上限 ${user_max_fee})
            * **運費手續費**: `${fee_2_shipping}` (費率 {user_rate_shipping}%)
            * **金流服務費**: `${fee_3_payment}` (費率 {current_rate_display})
            """)
            
            st.markdown("#### 2. 計算公式驗算")
            st.code(f"""
[訂單總額] = ({price} × {qty}) + {shipping} = {int(total_order_amount)}
[平台費用] = {fee_1_item} + {fee_2_shipping} + {fee_3_payment} = {total_fees}
[預估實收] = {int(total_order_amount)} - {total_fees} = {int(final_income)}
            """.strip())
            
            if cost is not None:
                st.code(f"""
[總成本]   = {cost} × {qty} = {total_cost}
[預估毛利] = {int(final_income)} - {total_cost} = {int(gross_profit)}
                """.strip())

    else:
        st.markdown("""
        <div style="text-align:center; padding: 50px; color:#aaa; border: 2px dashed #ddd; border-radius:10px; background-color:#fafafa;">
            <h3 style="color:#bbb;">👈 等待輸入</h3>
            請在左側輸入 <b>成本</b> 與 <b>售價</b><br>
            系統將自動計算結果
        </div>
        """, unsafe_allow_html=True)

# --- 頁尾 ---
st.markdown("""
<div class="footer-text">
    <b>© 2026 馬尼奇摩拍賣計算機 v2.9</b> | 動態費率設定版
</div>
""", unsafe_allow_html=True)
