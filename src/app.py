import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ============================================================
# 1. CẤU HÌNH GIAO DIỆN (CHỮ LỚN - HIỆN ĐẠI - NHÓM 10)
# ============================================================
st.set_page_config(
    page_title="Hệ thống Phân khúc Khách hàng - Nhóm 10",
    layout="wide"
)

# Tùy chỉnh CSS để đạt giao diện như bản mẫu: Chữ to, bỏ icon, màu sắc chuyên nghiệp
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        font-size: 22px; /* Kích thước chữ nền lớn */
        color: #1E293B;
    }
    
    /* Tiêu đề chính cực đại */
    .tieu-de-chinh {
        font-size: 55px;
        font-weight: 900;
        letter-spacing: -1.5px;
        color: #1E3A8A;
        margin-bottom: 25px;
        text-transform: uppercase;
    }

    h2 {
        font-size: 38px !important;
        font-weight: 800 !important;
        color: #334155 !important;
        border-left: 8px solid #3B82F6;
        padding-left: 20px !important;
        margin-top: 40px !important;
    }

    /* Thẻ chỉ số phẳng hiện đại */
    [data-testid="stMetric"] {
        background-color: #F8FAFC;
        border: 2px solid #E2E8F0;
        border-radius: 20px;
        padding: 30px !important;
    }

    /* Thanh điều hướng tối giản giống bản mẫu */
    .stRadio [role="radiogroup"] {
        background-color: #F1F5F9;
        padding: 20px;
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================
# 2. TẢI DỮ LIỆU
# ============================================================
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "notebooks" / "data" / "processed"
CLUSTERS_PATH = DATA_DIR / "customer_clusters_from_rules.csv"

@st.cache_data
def load_data():
    if not CLUSTERS_PATH.exists(): return None
    return pd.read_csv(CLUSTERS_PATH)

df = load_data()

if df is None:
    st.error("Không tìm thấy dữ liệu. Vui lòng kiểm tra file kết quả phân cụm.")
    st.stop()

# ============================================================
# 3. ĐIỀU HƯỚNG BÊN TRÁI (SIDEBAR) - NHÓM 10
# ============================================================
with st.sidebar:
    st.markdown("<p style='font-weight: 900; font-size: 32px; color: #1E3A8A;'>NHÓM 10</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 18px; color: #64748B;'>FIT - DNU</p>", unsafe_allow_html=True)
    st.markdown("---")
    # Điều hướng hoàn toàn bằng Tiếng Việt
    menu = st.radio("DANH MỤC QUẢN LÝ", ["TỔNG QUAN", "PHÂN TÍCH CỤM", "CHIẾN LƯỢC"])

# ============================================================
# TRANG 1: TỔNG QUAN
# ============================================================
if menu == "TỔNG QUAN":
    st.markdown("<div class='tieu-de-chinh'>PHÂN KHÚC KHÁCH HÀNG</div>", unsafe_allow_html=True)
    
    # Thẻ tóm tắt chỉ số
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Tổng Khách hàng", f"{len(df):,}")
    c2.metric("Số Phân khúc", df['cluster'].nunique())
    c3.metric("Chi tiêu TB", f"${df['Monetary'].mean():,.0f}")
    c4.metric("Tần suất TB", f"{df['Frequency'].mean():.1f}")

    st.markdown("---")
    
    col_trai, col_phai = st.columns([6, 4])
    with col_trai:
        st.markdown("<h2>Không gian RFM (3D)</h2>", unsafe_allow_html=True)
        # Sửa lỗi màu bằng bảng màu G10 ổn định
        fig_3d = px.scatter_3d(df, x='Recency', y='Frequency', z='Monetary',
                               color='cluster', opacity=0.8, height=750,
                               template="plotly_white",
                               color_discrete_sequence=px.colors.qualitative.G10)
        st.plotly_chart(fig_3d, use_container_width=True)
        
    with col_phai:
        st.markdown("<h2>Tỷ lệ các Nhóm</h2>", unsafe_allow_html=True)
        fig_pie = px.pie(df, names='cluster', hole=0.5, 
                         color_discrete_sequence=px.colors.sequential.Blues_r)
        fig_pie.update_traces(textinfo='percent+label', textfont_size=22)
        st.plotly_chart(fig_pie, use_container_width=True)

# ============================================================
# TRANG 2: PHÂN TÍCH CỤM
# ============================================================
elif menu == "PHÂN TÍCH CỤM":
    st.markdown("<div class='tieu-de-chinh'>ĐẶC TÍNH CHI TIẾT</div>", unsafe_allow_html=True)
    
    cluster_id = st.select_slider("Khảo sát Phân khúc số:", options=sorted(df['cluster'].unique()))
    
    # Chuẩn hóa dữ liệu để vẽ biểu đồ Radar
    stats = df.groupby('cluster')[['Recency', 'Frequency', 'Monetary']].mean()
    norm_stats = (stats - stats.min()) / (stats.max() - stats.min())
    
    t1, t2 = st.columns([4, 6])
    with t1:
        st.markdown(f"<h2>Chân dung Nhóm {cluster_id}</h2>", unsafe_allow_html=True)
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=norm_stats.loc[cluster_id].values,
            theta=['Ngày mua cuối', 'Tần suất', 'Chi tiêu'],
            fill='toself', fillcolor='rgba(59, 130, 246, 0.3)', line_color='#2563EB'
        ))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=False)), showlegend=False)
        st.plotly_chart(fig_radar, use_container_width=True)
        
    with t2:
        st.markdown("<h2>So sánh Phân phối</h2>", unsafe_allow_html=True)
        tieu_chi = st.radio("Chọn tiêu chí so sánh:", ["Monetary", "Frequency", "Recency"], horizontal=True)
        fig_box = px.box(df, x='cluster', y=tieu_chi, color='cluster', template="plotly_white")
        st.plotly_chart(fig_box, use_container_width=True)

# ============================================================
# TRANG 3: CHIẾN LƯỢC (VIỆT HÓA THEO BẢN MẪU)
# ============================================================
elif menu == "CHIẾN LƯỢC":
    st.markdown("<div class='tieu-de-chinh'>ĐỀ XUẤT HÀNH ĐỘNG</div>", unsafe_allow_html=True)
    
    nhom_chon = st.selectbox("Chọn nhóm khách hàng mục tiêu:", sorted(df['cluster'].unique()))
    
    tb_m = df[df['cluster'] == nhom_chon]['Monetary'].mean()
    tb_r = df[df['cluster'] == nhom_chon]['Recency'].mean()

    st.markdown(f"<h2>Phân tích chiến lược Nhóm {nhom_chon}</h2>", unsafe_allow_html=True)
    
    # Thiết kế thẻ chiến lược giống bản mẫu
    b1, b2 = st.columns(2)
    with b1:
        if tb_m > df['Monetary'].mean():
            st.markdown("<div style='padding:30px; border-radius:15px; background:#EBF5FF; border-left:10px solid #2563EB;'><b>Khách hàng Giá trị cao (VIP)</b><br><br>Nhóm mang lại doanh thu lớn. Cần các chương trình tri ân và ưu đãi đặc quyền để giữ chân lâu dài.</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='padding:30px; border-radius:15px; background:#F8FAFC; border-left:10px solid #94A3B8;'><b>Khách hàng Tiềm năng</b><br><br>Chi tiêu mức trung bình. Khuyến khích tăng giá trị giỏ hàng bằng các gợi ý từ Luật kết hợp.</div>", unsafe_allow_html=True)
            
    with b2:
        if tb_r > df['Recency'].mean():
            st.markdown("<div style='padding:30px; border-radius:15px; background:#FFF1F2; border-left:10px solid #EF4444;'><b>Cảnh báo Rời bỏ</b><br><br>Khách hàng đã lâu chưa quay lại. Cần gửi thông báo nhắc nhở hoặc tặng Voucher tái kích hoạt.</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='padding:30px; border-radius:15px; background:#F0FDF4; border-left:10px solid #22C55E;'><b>Đang hoạt động Tốt</b><br><br>Mua sắm gần đây thường xuyên. Phù hợp để giới thiệu các bộ sưu tập hoặc sản phẩm mới nhất.</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Dữ liệu khách hàng tiêu biểu")
    st.dataframe(df[df['cluster'] == nhom_chon].head(20), use_container_width=True)