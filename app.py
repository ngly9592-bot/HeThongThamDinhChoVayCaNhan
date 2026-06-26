import streamlit as st
import pandas as pd

# ==========================================
# 1. CẤU HÌNH TRANG & GIAO DIỆN (UI/UX)
# ==========================================
st.set_page_config(
    page_title="Hệ thống Thẩm định Cho vay Cá nhân",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Chèn Logo và Tiêu đề vào Sidebar
try:
    st.sidebar.image("logo.fjfi", use_container_width=True)
except:
    st.sidebar.warning("⚠️ Không tìm thấy file 'logo.png'. Vui lòng kiểm tra lại đường dẫn.")

st.sidebar.title("Điều Hướng Hệ Thống")
menu = st.sidebar.radio(
    "Chọn phân hệ chức năng:",
    ["1. Nhập Liệu Thẩm Định", "2. Báo Cáo & Kết Quả Phê Duyệt", "3. Tra Cứu Quy Định Lãi Suất"]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Hệ thống hỗ trợ quyết định tín dụng nội bộ v1.0**")

# ==========================================
# 2. KHỞI TẠO BIẾN TRẠNG THÁI (SESSION STATE)
# ==========================================
# Giúp lưu trữ dữ liệu khi chuyển đổi giữa các menu
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# ==========================================
# PHÂN HỆ 1: NHẬP LIỆU THẨM ĐỊNH
# ==========================================
if menu == "1. Nhập Liệu Thẩm Định":
    st.title("🏦 HỆ THỐNG THẨM ĐỊNH & PHÊ DUYỆT KHOẢN VAY CÁ NHÂN")
    st.write("Vui lòng điền đầy đủ thông tin dưới đây để hệ thống tính toán điểm số và đưa ra khuyến nghị tín dụng.")
    
    # Sử dụng form để tối ưu hóa việc load lại trang khi nhập liệu
    with st.form("loan_appraisal_form"):
        
        # ------------------------------------------
        # Khu vực 1: Thông tin Khách hàng & CIC
        # ------------------------------------------
        st.subheader("👤 1. Thông tin Khách hàng & Lịch sử Tín dụng (CIC)")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            customer_name = st.text_input("Họ và tên khách hàng:", value="Nguyễn Văn A")
            cif_code = st.text_input("Mã định danh (CIF/CCCD):", value="001205001234")
        with col2:
            cic_status = st.selectbox(
                "Nhóm nợ CIC cao nhất (12 tháng qua):",
                ["Nhóm 1 (Nợ đủ tiêu chuẩn)", "Nhóm 2 (Nợ cần chú ý)", "Nhóm 3 (Nợ dưới tiêu chuẩn)", "Nhóm 4 (Nợ nghi ngờ)", "Nhóm 5 (Nợ có khả năng mất vốn)"]
            )
        with col3:
            dependents = st.number_input("Số người phụ thuộc:", min_value=0, max_value=10, value=0, step=1)
            
        st.markdown("---")
        
        # ------------------------------------------
        # Khu vực 2: Chi tiết Khoản đề nghị vay
        # ------------------------------------------
        st.subheader("💰 2. Chi tiết Khoản vay Đề nghị")
        col4, col5, col6 = st.columns(3)
        
        with col4:
            loan_amount = st.number_input("Số tiền đề nghị vay (VND):", min_value=0.0, value=500000000.0, step=10000000.0, format="%.0f")
        with col5:
            loan_term = st.number_input("Thời gian vay (Tháng):", min_value=1, max_value=360, value=60, step=1)
        with col6:
            interest_rate = st.number_input("Lãi suất cho vay (%/năm):", min_value=0.0, max_value=30.0, value=8.5, step=0.1)

        st.markdown("---")

        # ------------------------------------------
        # Khu vực 3: Nguồn Thu nhập & Nghĩa vụ Tài chính
        # ------------------------------------------
        st.subheader("📊 3. Thu nhập & Nghĩa vụ Tài chính")
        col7, col8 = st.columns(2)
        
        with col7:
            monthly_income = st.number_input("Thu nhập bình quân hàng tháng (VND):", min_value=0.0, value=30000000.0, step=1000000.0, format="%.0f")
            existing_debt_payment = st.number_input("Gốc + lãi khoản vay cũ phải trả hàng tháng (VND):", min_value=0.0, value=2000000.0, step=500000.0, format="%.0f")
        with col8:
            st.markdown("""
            **Ghi chú thẩm định tài chính:**
            * Thu nhập chứng minh qua sao kê lương hoặc nguồn thu từ kinh doanh hợp pháp.
            * Dư nợ khoản vay cũ bao gồm: Vay tiêu dùng, thẻ tín dụng, vay mua nhà/xe tại các TCTD khác tính đến thời điểm hiện tại.
            """)

        st.markdown("---")

        # ------------------------------------------
        # Khu vực 4: Tài sản Đảm bảo (TSĐB)
        # ------------------------------------------
        st.subheader("🏠 4. Tài sản Đảm bảo (Collateral / LAV / LTV)")
        col9, col10 = st.columns(2)
        
        with col9:
            has_collateral = st.radio("Khoản vay có tài sản đảm bảo không?", ["Có", "Không bảo đảm (Vay tín chấp)"])
            collateral_value = st.number_input("Giá trị tài sản đảm bảo (VND):", min_value=0.0, value=800000000.0, step=10000000.0, format="%.0f")
        with col10:
            collateral_type = st.selectbox("Loại tài sản đảm bảo:", ["Bất động sản (Đất, nhà ở)", "Phương tiện vận tải (Ô tô)", "Giấy tờ có giá (Sổ tiết kiệm, trái phiếu)", "Khác"])

        # Nút submit form
        submit_btn = st.form_submit_button("⚡ Tính Toán & Thẩm Định Ngay")
        
        if submit_btn:
            # Lưu các giá trị vào session_state để chuyển tab không bị mất dữ liệu
            st.session_state.customer_name = customer_name
            st.session_state.cif_code = cif_code
            st.session_state.cic_status = cic_status
            st.session_state.dependents = dependents
            st.session_state.loan_amount = loan_amount
            st.session_state.loan_term = loan_term
            st.session_state.interest_rate = interest_rate
            st.session_state.monthly_income = monthly_income
            st.session_state.existing_debt_payment = existing_debt_payment
            st.session_state.has_collateral = has_collateral
            st.session_state.collateral_value = collateral_value
            st.session_state.collateral_type = collateral_type
            st.session_state.submitted = True
            
            st.success("🎉 Đã tính toán xong dữ liệu! Vui lòng chọn menu '2. Báo Cáo & Kết Quả Phê Duyệt' ở thanh bên để xem chi tiết.")

# ==========================================
# PHÂN HỆ 2: BÁO CÁO & KẾT QUẢ PHÊ DUYỆT
# ==========================================
elif menu == "2. Báo Cáo & Kết Quả Phê Duyệt":
    st.title("📋 KẾT QUẢ THẨM ĐỊNH & GỢI Ý PHÊ DUYỆT")
    
    if not st.session_state.submitted:
        st.warning("⚠️ Vui lòng hoàn thành nhập dữ liệu tại menu **'1. Nhập Liệu Thẩm Định'** trước.")
    else:
        # Lấy dữ liệu từ session_state
        r_monthly_rate = (st.session_state.interest_rate / 100) / 12
        n_months = st.session_state.loan_term
        
        # 1. Tính toán gốc lãi hàng tháng (Phương pháp định kỳ đều - Annuity)
        if r_monthly_rate > 0:
            monthly_loan_payment = (st.session_state.loan_amount * r_monthly_rate * (1 + r_monthly_rate)**n_months) / ((1 + r_monthly_rate)**n_months - 1)
        else:
            monthly_loan_payment = st.session_state.loan_amount / n_months
            
        total_monthly_obligation = monthly_loan_payment + st.session_state.existing_debt_payment
        
        # 2. Tính chỉ số DTI (Debt-to-Income)
        dti_ratio = (total_monthly_obligation / st.session_state.monthly_income) * 100 if st.session_state.monthly_income > 0 else 100
        
        # 3. Tính chỉ số LTV / LAV (Loan-to-Value)
        if st.session_state.has_collateral == "Có" and st.session_state.collateral_value > 0:
            ltv_ratio = (st.session_state.loan_amount / st.session_state.collateral_value) * 100
        else:
            ltv_ratio = 100.0  # Tín chấp hoặc không có TSĐB coi như hệ số rủi ro trần

        # ------------------------------------------
        # HIỂN THỊ CHỈ SỐ KINH DOANH CỐT LÕI (KPIs)
        # ------------------------------------------
        st.subheader("📊 Các Chỉ Số Tài Chính Key Metrics")
        kpi1, kpi2, kpi3 = st.columns(3)
        
        with kpi1:
            st.metric(label="Gốc + Lãi Khoản Vay Mới / Tháng", value=f"{monthly_loan_payment:,.0f} VND")
        with kpi2:
            # Đổi màu cảnh báo nếu DTI > 60%
            if dti_ratio > 60:
                st.metric(label="Chỉ số DTI (Nghĩa vụ nợ / Thu nhập)", value=f"{dti_ratio:.2f}%", delta="Vượt ngưỡng an toàn (>60%)", delta_color="inverse")
            else:
                st.metric(label="Chỉ số DTI (Nghĩa vụ nợ / Thu nhập)", value=f"{dti_ratio:.2f}%", delta="An toàn")
        with kpi3:
            if st.session_state.has_collateral == "Có":
                st.metric(label="Chỉ số LTV/LAV (Tỷ lệ cho vay trên TSĐB)", value=f"{ltv_ratio:.2f}%", delta="Mức trần quy định: 70-80%")
            else:
                st.metric(label="Chỉ số LTV/LAV", value="N/A (Tín chấp)")

        st.markdown("---")

        # ------------------------------------------
        # HỆ THỐNG LUẬT PHÊ DUYỆT TỰ ĐỘNG (UNDERWRITING RULE ENGINE)
        # ------------------------------------------
        st.subheader("🤖 Kết Quả Đánh Giá Từ Hệ Thống Tự Động")
        
        reasons = []
        is_approved = True
        
        # Rule 1: Xét CIC
        if st.session_state.cic_status != "Nhóm 1 (Nợ đủ tiêu chuẩn)":
            is_approved = False
            reasons.append(f"❌ Khách hàng có lịch sử nợ xấu/chú ý: {st.session_state.cic_status}")
            
        # Rule 2: Xét DTI (Thông thường ngân hàng chặn ở mức 60-65%)
        if dti_ratio > 60:
            is_approved = False
            reasons.append(f"❌ Chỉ số DTI quá cao ({dti_ratio:.2f}%). Khả năng trả nợ yếu.")
            
        # Rule 3: Xét LTV (Cho vay thế chấp tối đa 75-80% giá trị định giá)
        if st.session_state.has_collateral == "Có" and ltv_ratio > 75:
            is_approved = False
            reasons.append(f"❌ Tỷ lệ LTV ({ltv_ratio:.2f}%) vượt mức an toàn cho phép (75% đối với {st.session_state.collateral_type}).")

        # Hiển thị Quyết định Đề xuất
        if is_approved:
            st.balloons()
            st.success(f"🟢 **ĐỀ XUẤT: PHÊ DUYỆT KHOẢN VAY**\n\nKhách hàng **{st.session_state.customer_name}** đạt đầy đủ các tiêu chuẩn phân tích rủi ro tín dụng hiện hành.")
        else:
            st.error(f"🔴 **ĐỀ XUẤT: TỪ CHỐI HOẶC SỬA ĐỔI CẤU TRÚC KHOẢN VAY**")
            st.write("**Lý do chi tiết:**")
            for reason in reasons:
                st.write(reason)
                
        st.markdown("---")
        
        # ------------------------------------------
        # BẢNG TỔNG HỢP CHI TIẾT ĐỂ XUẤT FILE
        # ------------------------------------------
        st.subheader("📝 Bảng Tổng Hợp Dữ Liệu Thẩm Định")
        
        summary_data = {
            "Chỉ số thẩm định": [
                "Khách hàng", "Mã CIF/CCCD", "Số tiền đề xuất", "Thời hạn", "Lãi suất năm", 
                "Thu nhập tháng", "Nợ cũ hàng tháng", "Nợ mới hàng tháng", "Tỷ lệ DTI", "Loại TSĐB", "Giá trị TSĐB", "Tỷ lệ LTV/LAV", "Tình trạng CIC"
            ],
            "Giá trị thực tế": [
                st.session_state.customer_name,
                st.session_state.cif_code,
                f"{st.session_state.loan_amount:,.0f} VND",
                f"{st.session_state.loan_term} Tháng",
                f"{st.session_state.interest_rate} %",
                f"{st.session_state.monthly_income:,.0f} VND",
                f"{st.session_state.existing_debt_payment:,.0f} VND",
                f"{monthly_loan_payment:,.0f} VND",
                f"{dti_ratio:.2f} %",
                st.session_state.collateral_type if st.session_state.has_collateral == "Có" else "Không có",
                f"{st.session_state.collateral_value:,.0f} VND" if st.session_state.has_collateral == "Có" else "0 VND",
                f"{ltv_ratio:.2f} %" if st.session_state.has_collateral == "Có" else "N/A",
                st.session_state.cic_status
            ]
        }
        
        df_summary = pd.DataFrame(summary_data)
        st.table(df_summary)
        
        # Tính năng download báo cáo nhanh dưới dạng CSV
        csv = df_summary.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 Tải báo cáo thẩm định (.CSV)",
            data=csv,
            file_name=f"Bao_cao_tham_dinh_{st.session_state.cif_code}.csv",
            mime="text/csv"
        )

# ==========================================
# PHÂN HỆ 3: TRA CỨU QUY ĐỊNH
# ==========================================
elif menu == "3. Tra Cứu Quy Định Lãi Suất":
    st.title("📚 QUY ĐỊNH KHUNG TÍN DỤNG & LÃI SUẤT NỘI BỘ")
    st.write("Khung tham chiếu các điều kiện biên phục vụ phê duyệt rủi ro:")
    
    data_rules = {
        "Sản phẩm vay": ["Vay mua nhà ở", "Vay mua Ô tô", "Vay Tiêu dùng thế chấp", "Vay Tín chấp lương"],
        "Lãi suất trần ưu đãi": ["7.5% - 8.5%", "8.0% - 9.0%", "9.0% - 10.5%", "12.0% - 15.5%"],
        "Tỷ lệ LTV tối đa": ["75%", "70%", "65%", "N/A (Không TSĐB)"],
        "Thời hạn tối đa": ["25 năm (300 tháng)", "8 năm (96 tháng)", "10 năm (120 tháng)", "5 năm (60 tháng)"]
    }
    st.dataframe(pd.DataFrame(data_rules), use_container_width=True)
