import streamlit as st
import math

# --- 頁面設定 ---
st.set_page_config(page_title="奇摩拍賣計算機", page_icon="🧮")

# --- 標題與說明 ---
st.title("🧮 奇摩拍賣費用試算 (Web版)")
st.markdown("""
**計費規則依據：**
1. **成交手續費 (商品)**: 2.49% (單件上限 $498)。
2. **交易手續費 (運費)**: 2.49% (一般寄送運費 ≤$300 免收；面交全額收)。
3. **金流服務費**: 信用卡 2% / 非信用卡 1% (最低 $1)。
---
""")

# --- 輸入區塊 (使用 Columns 排版) ---
col1, col2 = st.columns(2)

with col1:
    price = st.number_input("商品成交單價 ($)", min_value=0, value=1000, step=10)
    qty = st.number_input("數量", min_value=1, value=1, step=1)
    shipping = st.number_input("買家支付運費 ($)", min_value=0, value=60, step=10)

with col2:
    ship_method = st.selectbox(
        "運送方式", 
        ["一般寄送 (超商/宅配/郵寄)", "面交/自取"],
        help="面交沒有 $300 免徵運費手續費的優惠"
    )
    
    pay_method = st.selectbox(
        "買家付款方式",
        ["信用卡 (費率 2%)", "非信用卡/ATM/餘額 (費率 1%)"]
    )

# --- 觸發計算 ---
if st.button("開始計算", type="primary", use_container_width=True):
    
    # === 核心計算邏輯 (與 GUI 版本一致) ===
    
    # 1. 成交交易手續費 (商品)
    # 先算單件，四捨五入，檢查上限 498，再乘數量
    single_item_fee_raw = price * 0.0249
    single_item_fee = round(single_item_fee_raw)
    
    is_capped = False
    if single_item_fee > 498:
        single_item_fee = 498
        is_capped = True
    
    fee_1_item = single_item_fee * qty

    # 2. 交易手續費 (運費)
    fee_2_shipping = 0
    shipping_msg = ""
    
    if ship_method == "面交/自取":
        fee_2_shipping = round(shipping * 0.0249)
        shipping_msg = "面交無免徵門檻"
    else:
        if shipping > 300:
            fee_2_shipping = round(shipping * 0.0249)
            shipping_msg = "運費 > $300，全額計收"
        else:
            fee_2_shipping = 0
            shipping_msg = "運費 ≤ $300，免收手續費"

    # 3. 金流服務費
    total_order_amount = (price * qty) + shipping
    
    if "信用卡" in pay_method:
        payment_rate = 0.02
        pay_msg = "2%"
    else:
        payment_rate = 0.01
        pay_msg = "1%"
        
    fee_3_payment_raw = total_order_amount * payment_rate
    fee_3_payment = round(fee_3_payment_raw)
    
    # 最低 $1 限制
    min_fee_msg = ""
    if total_order_amount > 0 and fee_3_payment < 1:
        fee_3_payment = 1
        min_fee_msg = " (觸發最低 $1 限制)"

    # 總結
    total_fees = fee_1_item + fee_2_shipping + fee_3_payment
    final_income = total_order_amount - total_fees

    # === 結果顯示 ===
    st.markdown("### 📊 計算結果")
    
    # 使用 Metric 顯示大字體結果
    m1, m2, m3 = st.columns(3)
    m1.metric("訂單總金額", f"${int(total_order_amount):,}")
    m2.metric("總費用支出", f"${int(total_fees):,}", delta_color="inverse")
    m3.metric("預估實收", f"${int(final_income):,}")
    
    st.divider()
    
    # 詳細明細
    st.info(f"""
    **費用明細詳情：**
    
    1. **成交手續費 (商品): ${fee_1_item}**
       - 單件計算: ${int(price)} x 2.49% = {single_item_fee} 元
       - 上限狀態: {"🔴 已達單件上限 $498" if is_capped else "🟢 未達上限"}
       - 數量: {qty} 件
       
    2. **交易手續費 (運費): ${fee_2_shipping}**
       - 運費金額: ${int(shipping)}
       - 判斷: {shipping_msg}
       
    3. **金流服務費: ${fee_3_payment}**
       - 費率: {pay_msg}
       - 說明: {min_fee_msg if min_fee_msg else "依訂單總額計算"}
    """)
