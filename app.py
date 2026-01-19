import streamlit as st

# --- 頁面設定 (必須在第一行) ---
st.set_page_config(page_title="馬尼奇摩拍賣計算機", page_icon="🧮", layout="wide")

# --- CSS 樣式微調 (讓系統資訊置底看起來更整齊) ---
st.markdown("""
<style>
    .footer-text {
        font-size: 12px;
        color: #666;
        margin-top: 50px;
        border-top: 1px solid #ddd;
        padding-top: 10px;
    }
    .formula-box {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
        font-family: monospace;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# --- 主標題 ---
st.title("🧮 馬尼奇摩拍賣計算機 GUI版")

# --- 建立三欄位佈局 ---
# 比例配置：說明(0.8) | 輸入(1) | 結果(1.2)
col_info, col_input, col_result = st.columns([0.8, 1, 1.2])

# ==========================================
# 【左欄】：功能說明 & 系統資訊
# ==========================================
with col_info:
    st.subheader("ℹ️ 功能說明")
    st.info("""
    **計費規則依據 (2026持續適用)：**
    
    1. **成交手續費 (商品)**: 
       - 費率 **2.49%**。
       - 單件商品手續費上限 **$498**。
       
    2. **交易手續費 (運費)**: 
       - 費率 **2.49%**。
       - 一般寄送：運費 ≤$300 免收；>$300 全額收。
       - 面交/自取：運費全額收。
       
    3. **金流服務費**: 
       - 信用卡 **2%**。
       - 非信用卡 **1%**。
       - 最低收取 **$1**。
    """)

    # 系統資訊置底
    st.markdown("<br>" * 5, unsafe_allow_html=True) # 增加一些空白間距
    st.markdown("""
    <div class="footer-text">
        <b>⚙️ 系統資訊</b><br>
        版本：v2.0 (2026/01/19)<br>
        更新內容：<br>
        - 新增商品成本與毛利試算<br>
        - 優化三欄式介面體驗<br>
        - 新增詳細公式顯示<br>
        <br>
        <b>© 2026 馬尼奇摩拍賣計算機</b>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 【中欄】：試算輸入
# ==========================================
with col_input:
    st.subheader("⌨️ 試算輸入")
    st.caption("提示：使用 Tab 鍵可快速切換至下一格")

    # 使用 Form 讓輸入更整潔，或者直接使用交互式輸入
    # 這裡直接使用輸入框以便即時反應，不需按Submit
    
    # 1. 成本 (新增)
    cost = st.number_input(
        "1. 商品成本單價 ($)", 
        min_value=0, 
        value=None, 
        step=10, 
        placeholder="請輸入成本..."
    )

    # 2. 售價 (預設無數字)
    price = st.number_input(
        "2. 商品成交單價 ($)", 
        min_value=0, 
        value=None, 
        step=10, 
        placeholder="請輸入售價..."
    )

    # 3. 數量
    qty = st.number_input("3. 數量", min_value=1, value=1, step=1)

    # 4. 運費
    shipping = st.number_input("4. 買家支付運費 ($)", min_value=0, value=60, step=10)

    # 5. 運送方式
    ship_method = st.selectbox(
        "5. 運送方式", 
        ["一般寄送 (超商/宅配/郵寄)", "面交/自取"],
        index=0
    )
    
    # 6. 付款方式 (預設非信用卡 -> index=1)
    pay_method = st.selectbox(
        "6. 買家付款方式",
        ["信用卡 (費率 2%)", "非信用卡/ATM/餘額 (費率 1%)"],
        index=1  # 預設選第二個選項
    )

# ==========================================
# 【右欄】：計算結果
# ==========================================
with col_result:
    st.subheader("📊 計算結果")

    # 只有當售價被輸入時才開始計算
    if price is not None:
        # --- 核心邏輯計算 ---
        
        # A. 商品手續費
        single_item_fee_raw = price * 0.0249
        single_item_fee = round(single_item_fee_raw)
        is_capped = False
        if single_item_fee > 498:
            single_item_fee = 498
            is_capped = True
        fee_1_item = single_item_fee * qty

        # B. 運費手續費
        fee_2_shipping = 0
        if ship_method == "面交/自取":
            fee_2_shipping = round(shipping * 0.0249)
        else:
            if shipping > 300:
                fee_2_shipping = round(shipping * 0.0249)
            else:
                fee_2_shipping = 0

        # C. 金流服務費
        total_order_amount = (price * qty) + shipping
        if "信用卡" in pay_method:
            payment_rate = 0.02
        else:
            payment_rate = 0.01
            
        fee_3_payment_raw = total_order_amount * payment_rate
        fee_3_payment = round(fee_3_payment_raw)
        if total_order_amount > 0 and fee_3_payment < 1:
            fee_3_payment = 1

        # D. 總結數據
        total_fees = fee_1_item + fee_2_shipping + fee_3_payment
        final_income = total_order_amount - total_fees
        
        # E. 毛利計算
        total_cost = (cost * qty) if cost is not None else 0
        gross_profit = final_income - total_cost

        # --- 顯示四大公式與結果 ---
        
        # 1. 訂單總金額
        st.markdown("**1. 訂單總金額**")
        st.code(f"({price} × {qty}) + {shipping} = ${int(total_order_amount):,}")
        
        # 2. 總平台費用
        st.markdown("**2. 總平台費用 (Yahoo + 金流)**")
        st.code(f"{fee_1_item} (商品) + {fee_2_shipping} (運費) + {fee_3_payment} (金流) = ${total_fees:,}")
        
        # 3. 預估實收
        st.markdown("**3. 預估實收金額**")
        st.code(f"{int(total_order_amount)} - {total_fees} = ${int(final_income):,}")
        
        # 4. 預估毛利 (如果有輸入成本)
        st.markdown("**4. 預估毛利 (實收 - 成本)**")
        if cost is not None:
            profit_color = "green" if gross_profit > 0 else "red"
            st.code(f"{int(final_income)} - ({cost} × {qty}) = ${int(gross_profit):,}")
            
            # 使用 Metric 顯示最終毛利，帶顏色
            st.metric(
                label="最終預估毛利", 
                value=f"${int(gross_profit):,}", 
                delta=f"利潤率: {round((gross_profit/total_order_amount)*100, 1)}%" if total_order_amount > 0 else None
            )
        else:
            st.warning("⚠️ 請輸入「商品成本」以計算毛利")

        st.divider()

        # --- 費用明細詳情 (Expander 收合) ---
        with st.expander("🔻 查看詳細費用明細", expanded=True):
            st.markdown(f"""
            * **成交手續費**: `${fee_1_item}` 
                * 單件 `${single_item_fee}` {"(已達上限 $498)" if is_capped else ""} × {qty}
            * **運費手續費**: `${fee_2_shipping}`
                * {"面交全額收" if ship_method == "面交/自取" else ("運費 > $300 全額收" if shipping > 300 else "運費 ≤ $300 免收")}
            * **金流服務費**: `${fee_3_payment}`
                * 費率 {int(payment_rate*100)}% (最低 $1)
            """)

    else:
        # 等待輸入畫面
        st.info("👈 請在中間欄位輸入「成本」與「售價」開始試算")
