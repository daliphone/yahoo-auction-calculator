import streamlit as st
import streamlit.components.v1 as components

# --- 頁面設定 ---
st.set_page_config(page_title="馬尼奇摩拍賣計算機", page_icon="🧮", layout="wide")

# --- CSS 美化與版面調整 ---
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

    /* 2. 結果區塊樣式 (三欄位配色 - 字體加大版) */
    .result-box-income {
        background-color: #e3f2fd; /* 實收-藍底 */
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        border: 2px solid #90caf9; /* 邊框加粗 */
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
    
    /* 重點：將結果數字調整為 42px 且超粗體 */
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

# --- JavaScript: Enter 跳下一格 (Focus Next) ---
js_code = """
<script>
document.addEventListener('DOMContentLoaded', function() {
    const inputs = parent.document.querySelectorAll('input[type="number"], input[type="text"]');
    inputs.forEach((input, index) => {
        input.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                const nextInput = inputs[index + 1];
                if (nextInput) {
                    nextInput.focus();
                    nextInput.select();
                }
            }
        });
    });
});
</script>
"""
components.html(js_code, height=0, width=0)

# --- 主標題 ---
st.title("🧮 馬尼奇摩拍賣計算機 GUI版")

# --- 建立三欄位佈局 ---
# 左(說明) | 中(輸入) | 右(結果)
col_info, col_input, col_result = st.columns([0.8, 1, 1.4])

# ==========================================
# 【左欄】：功能說明
# ==========================================
with col_info:
    st.subheader("ℹ️ 規則說明")
    st.info("""
    **2026 計費規則：**
     
    1. **成交手續費 (商品)**: 
       - 費率 **2.49%** (上限 $498)。
       
    2. **交易手續費 (運費)**: 
       - 費率 **2.49%**。
       - 一般寄送：運費 >$300 才收。
       - 面交/自取：全額收。
       
    3. **金流服務費**: 
       - 信用卡 **2%** / 其他 **1%**。
       - 最低收取 **$1**。
    """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("操作提示：已開啟 Enter 跳格功能 (依瀏覽器而定)，或請使用 Tab 鍵切換。")

# ==========================================
# 【中欄】：試算輸入
# ==========================================
with col_input:
    st.subheader("⌨️ 試算輸入")
    
    with st.container(border=True):
        
        # 1. 成本 (加入 placeholder)
        cost = st.number_input(
            "1. 商品成本 ($)", 
            min_value=0, 
            value=None, 
            step=10, 
            placeholder="請輸入商品成本..."
        )

        # 2. 售價 (加入 placeholder)
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
            pay_method = st.selectbox("6. 付款", ["信用卡 (2%)", "非信用卡 (1%)"], index=1)

# ==========================================
# 【右欄】：計算結果
# ==========================================
with col_result:
    st.subheader("📊 計算結果")

    if price is not None:
        # --- 核心邏輯 (v2.3 保持不變) ---
        single_item_fee_raw = price * 0.0249
        single_item_fee = round(single_item_fee_raw)
        is_capped = False
        if single_item_fee > 498:
            single_item_fee = 498
            is_capped = True
        fee_1_item = single_item_fee * qty

        fee_2_shipping = 0
        if ship_method == "面交/自取":
            fee_2_shipping = round(shipping * 0.0249)
        else:
            if shipping > 300:
                fee_2_shipping = round(shipping * 0.0249)
            else:
                fee_2_shipping = 0

        total_order_amount = (price * qty) + shipping
        if "信用卡" in pay_method:
            payment_rate = 0.02
        else:
            payment_rate = 0.01
            
        fee_3_payment_raw = total_order_amount * payment_rate
        fee_3_payment = round(fee_3_payment_raw)
        if total_order_amount > 0 and fee_3_payment < 1:
            fee_3_payment = 1

        total_fees = fee_1_item + fee_2_shipping + fee_3_payment
        final_income = total_order_amount - total_fees
        
        total_cost = (cost * qty) if cost is not None else 0
        gross_profit = final_income - total_cost

        # --- 視覺優化：三個重點數據 (字體加大版) ---
        
        r_col1, r_col2, r_col3 = st.columns(3)
        
        # 1. 預估實收
        with r_col1:
            st.markdown(f"""
            <div class="result-box-income">
                <span class="label-text">預估實收</span>
                <p class="value-text" style="color:#1565c0;">${int(final_income):,}</p>
            </div>
            """, unsafe_allow_html=True)
            
        # 2. 平台總費用
        with r_col2:
            st.markdown(f"""
            <div class="result-box-fee">
                <span class="label-text">平台總手續費</span>
                <p class="value-text" style="color:#ef6c00;">${int(total_fees):,}</p>
            </div>
            """, unsafe_allow_html=True)
            
        # 3. 預估毛利
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

        # --- 詳細公式與費用 (將公式移入此處) ---
        with st.expander("📝 查看詳細計算公式與費用明細", expanded=False):
            st.markdown("#### 1. 費用明細")
            st.markdown(f"""
            * **成交手續費**: `${fee_1_item}` (單件${single_item_fee} × {qty})
            * **運費手續費**: `${fee_2_shipping}`
            * **金流服務費**: `${fee_3_payment}` ({int(payment_rate*100)}%)
            """)
            
            st.markdown("#### 2. 計算公式驗算")
            # 顯示詳細算式
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
        # 等待輸入畫面
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
    <b>© 2026 馬尼奇摩拍賣計算機 v2.4</b> | 視覺強化版
</div>
""", unsafe_allow_html=True)
