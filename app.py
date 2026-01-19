import streamlit as st
import streamlit.components.v1 as components

# --- 頁面設定 ---
st.set_page_config(page_title="馬尼奇摩拍賣計算機", page_icon="🧮", layout="wide")

# --- CSS 美化與版面調整 ---
st.markdown("""
<style>
    /* 1. 輸入框優化 (卡片式風格) */
    .input-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }
    
    /* 2. 輸入框文字強制加粗、加大 */
    div[data-baseweb="input"] > div > input {
        font-weight: bold !important;
        font-size: 18px !important;
        color: #333 !important;
    }
    .stNumberInput label {
        font-weight: bold;
        color: #555;
    }

    /* 3. 結果區塊樣式 (緊湊版) */
    .result-box-income {
        background-color: #e3f2fd; /* 淺藍底 */
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #90caf9;
    }
    .result-box-profit {
        background-color: #e8f5e9; /* 淺綠底 */
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #a5d6a7;
    }
    .result-box-loss {
        background-color: #ffebee; /* 淺紅底 */
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #ef9a9a;
    }
    
    .label-text { font-size: 14px; color: #666; font-weight: bold; margin-bottom: 5px; display: block;}
    .value-text { font-size: 32px; font-weight: 900; margin: 0; line-height: 1.2; }
    
    /* 4. 頁尾 */
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

# --- JavaScript: 嘗試實現 Enter 跳下一格 (Focus Next) ---
# 注意：這是透過 JS 模擬 Tab 行為，視瀏覽器安全性設定而定
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
# 調整比例讓中間輸入區更寬一點點，右邊結果區緊湊一點
col_info, col_input, col_result = st.columns([0.8, 1.1, 1.1])

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
    st.caption("操作提示：已開啟 Enter 跳格功能 (部分瀏覽器支援)，或請使用 Tab 鍵切換。")

# ==========================================
# 【中欄】：試算輸入 (美化卡片區)
# ==========================================
with col_input:
    st.subheader("⌨️ 試算輸入")
    
    # 開始輸入卡片容器
    st.markdown('<div class="input-card">', unsafe_allow_html=True)

    # 1. 成本
    cost = st.number_input("1. 商品成本 ($)", min_value=0, value=None, step=10)

    # 2. 售價
    price = st.number_input("2. 商品售價 ($)", min_value=0, value=None, step=10)

    # 3. 數量 & 4. 運費 (並排以節省空間)
    c1, c2 = st.columns(2)
    with c1:
        qty = st.number_input("3. 數量", min_value=1, value=1, step=1, format="%d")
    with c2:
        shipping = st.number_input("4. 運費 ($)", min_value=0, value=60, step=10, format="%d")

    # 5. 運送 & 6. 付款 (並排)
    c3, c4 = st.columns(2)
    with c3:
        ship_method = st.selectbox("5. 運送", ["一般寄送", "面交/自取"])
    with c4:
        pay_method = st.selectbox("6. 付款", ["信用卡 (2%)", "非信用卡 (1%)"], index=1)
        
    st.markdown('</div>', unsafe_allow_html=True) # 結束卡片

# ==========================================
# 【右欄】：計算結果 (緊湊置頂版)
# ==========================================
with col_result:
    st.subheader("📊 計算結果")

    if price is not None:
        # --- 核心邏輯 (v2.1 完全保留) ---
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

        # --- 視覺優化：重點數據置頂 (2x2 Grid) ---
        
        # 第一排：【預估實收】 與 【預估毛利】 (最重要)
        r1_col1, r1_col2 = st.columns(2)
        
        with r1_col1:
            # 實收區塊
            st.markdown(f"""
            <div class="result-box-income">
                <span class="label-text">預估實收金額</span>
                <p class="value-text" style="color:#1565c0;">${int(final_income):,}</p>
            </div>
            """, unsafe_allow_html=True)
            
        with r1_col2:
            # 毛利區塊
            if cost is not None:
                profit_style = "result-box-profit" if gross_profit > 0 else "result-box-loss"
                profit_color = "#2e7d32" if gross_profit > 0 else "#c62828"
                st.markdown(f"""
                <div class="{profit_style}">
                    <span class="label-text">預估毛利 (淨賺)</span>
                    <p class="value-text" style="color:{profit_color};">${int(gross_profit):,}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("請輸入成本")

        # 第二排：公式補充 (字體縮小，節省空間)
        st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
        
        # 使用 Columns 顯示次要資訊
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            st.markdown(f"**訂單總額**: `${int(total_order_amount):,}`")
            st.caption(f"({price}×{qty}) + {shipping}")
        with f_col2:
            st.markdown(f"**平台費用**: `${total_fees:,}`")
            st.caption("Yahoo手續費 + 金流費")

        # 利潤率顯示
        if cost is not None and total_order_amount > 0:
            margin_rate = (gross_profit / total_order_amount) * 100
            st.progress(max(0, min(100, int(margin_rate))))
            st.caption(f"當前利潤率: {margin_rate:.1f}%")

        # --- 詳細費用 (Expander 收合) ---
        with st.expander("詳細費用明細 (點擊展開)", expanded=False):
            st.markdown(f"""
            1. **成交手續費**: `${fee_1_item}` 
               (單件${single_item_fee} × {qty})
            2. **運費手續費**: `${fee_2_shipping}`
            3. **金流服務費**: `${fee_3_payment}` ({int(payment_rate*100)}%)
            """)

    else:
        # 等待輸入畫面 (高度佔位，保持版面穩定)
        st.markdown("""
        <div style="text-align:center; padding: 40px; color:#aaa; border: 2px dashed #ddd; border-radius:10px;">
            請在左側輸入<br><b>成本</b> 與 <b>售價</b><br>以查看結果
        </div>
        """, unsafe_allow_html=True)

# --- 頁尾 ---
st.markdown("""
<div class="footer-text">
    <b>© 2026 馬尼奇摩拍賣計算機 v2.2</b> | 邏輯核心 v2.1 | 介面優化版
</div>
""", unsafe_allow_html=True)
