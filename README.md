#  MINI PROJECT: Phân Cụm Khách Hàng Từ Luật Kết Hợp

##  Thông Tin Nhóm

* **Nhóm**: 10 - CNTT 17-10
* **Thành viên**:
    * Lê Thị Thương
    * Trần Thị Thùy Linh
    * Trần Hải Linh
* **Ngày hoàn thành**: 15/01/2026

---

## 🎯 Mục tiêu
Dự án nhằm mục đích phân khúc khách hàng dựa trên hành vi mua sắm thông qua các luật kết hợp khai phá được bằng thuật toán 
FP-Growth.

---

##  Quy Trình Tổng Quan
1. **Khai phá Luật kết hợp (Association Rule Mining)**
2. **Feature Engineering Cho Phân Cụm Khách Hàng**
3. **Lựa chọn số cụm K và huấn luyện mô hình phân cụm**
4. **Trực quan hóa và đánh giá phân cụm**
5. **So sánh có hệ thống giữa các biến thể đặc trưng**
6. **Profiling và diễn giải cụm khách hàng**
7. **Dashboard Streamlit**

##  1. Khai Phá Luật Kết Hợp (Association Rule Mining)

- Sử dụng **Apriori** (và FP-Growth để so sánh) để khai thác luật kết hợp từ dữ liệu giao dịch.

- Áp dụng các ngưỡng lọc:

   *  min_support
     
   *  min_confidence
   
   *  min_lift > 1

- Các luật được sắp xếp theo Lift và chọn Top-K = 200 luật có chất lượng cao nhất.

- Lift được ưu tiên vì phản ánh mức độ liên kết thực sự giữa các sản phẩm, tránh thiên lệch do sản phẩm phổ biến.

- Tập luật sau lọc được sử dụng làm đầu vào cho bước xây dựng đặc trưng và phân cụm khách hàng.

---

**Bảng 1. Một số luật kết hợp tiêu biểu**
<img width="800" height="300" alt="image" src="https://github.com/user-attachments/assets/ba35775b-b5e0-413d-85a9-0e262d50e01d" />

---

##  2. Feature Engineering Cho Phân Cụm Khách Hàng
   Sau khi lựa chọn được tập luật kết hợp làm đầu vào, nhóm tiến hành bước **feature engineering** nhằm chuyển hóa các luật kết hợp thành **vector
   đặc trưng biểu diễn hành vi mua sắm của từng khách hàng**. Theo yêu cầu của đề bài, nhóm xây dựng **hai biến thể đặc trưn** để so sánh hiệu quả phân cụm: một biến thể baseline và một biến thể nâng cao.

---

  **2.1. Biến thể 1 – Đặc trưng nhị phân theo luật (Baseline)**
  
**Ý tưởng:**

- Mỗi luật kết hợp được xem như một đặc trưng hành vi.

- Một khách hàng “bật” luật nếu đã mua đầy đủ antecedents của luật đó.

- Không xét độ mạnh của luật.

**Cách xây dựng:**

- Với mỗi khách hàng i và luật rⱼ:
  
  <img width="400" height="70" alt="image" src="https://github.com/user-attachments/assets/8de64e36-1774-47ba-bac5-28175f1795d1" />

- Thu được ma trận Customer × Rule (giá trị 0/1).

**Vai trò:**

- Đơn giản, dễ diễn giải

- Là baseline để so sánh hiệu quả của biến thể nâng cao

---

## 2.2. Biến thể 2 – Đặc trưng nâng cao (Weighted rules + RFM)

**2.2.1. Đặc trưng luật có trọng số**

- Thay vì 0/1, luật được gán trọng số theo độ mạnh.

- Nếu khách hàng thỏa antecedent của luật rⱼ:

<img width="107" height="38" alt="image" src="https://github.com/user-attachments/assets/c3750e60-0dc5-491f-8619-9d7ef986105f" />

Trong đó:

<img width="248" height="44" alt="image" src="https://github.com/user-attachments/assets/e7862c5a-1291-4941-8cae-ce01db1749ee" />

**Lý do chọn Lift:**

- Phản ánh mức độ mua kèm thực sự

- Tránh thiên lệch do sản phẩm phổ biến

- Phù hợp với phân cụm theo hành vi

**2.2.2. Kết hợp RFM**

Bổ sung thông tin giá trị khách hàng thông qua:

- **Recency:** số ngày từ lần mua gần nhất

- **Frequency:** số hóa đơn

- **Monetary:** tổng chi tiêu

<img width="471" height="330" alt="image" src="https://github.com/user-attachments/assets/4ac99abc-1dcf-4799-93c5-a5e259749922" />

Các biến RFM được:

- Chuẩn hóa bằng **StandardScaler**

- Ghép với vector đặc trưng từ luật

<img width="352" height="60" alt="image" src="https://github.com/user-attachments/assets/34d513e7-3f14-44e6-bdcb-55f245ffcce9" />

---

**2.2.3. Thiết lập biến thể nâng cao**

### 🛠️ Thiết lập tham số dự án

| Thiết lập | Giá trị |
| :--- | :--- |
| **Weighting cho luật** | Lift |
| **Sử dụng RFM** | Có |
| **Scale RFM** | Có (StandardScaler) |
| **Scale rule-features** | Không |
| **Số luật** | Top-K = 200 |
| **Lọc độ dài antecedent** | Có |

---

**2.2.4. Thử nghiệm lọc độ dài antecedent**

- Loại các luật có antecedent quá ngắn

- Giảm luật phổ biến, tăng tính phân biệt

- Ảnh hưởng rõ rệt đến chất lượng phân cụm (silhouette score)

**2.3. So sánh hai biến thể đặc trưng**

### 📈 Đánh giá phương pháp Phân cụm

| Tiêu chí | Baseline (Binary) | Nâng cao (Weighted + RFM) |
| :--- | :---: | :---: |
| **Phản ánh độ mạnh luật** | ❌ | ✅ |
| **Phản ánh giá trị khách hàng** | ❌ | ✅ |
| **Dễ diễn giải** | ✅ | ✅ |
| **Khả năng phân biệt cụm** | Trung bình | **Tốt hơn** |

---

## 3. Lựa chọn số cụm K và huấn luyện mô hình phân cụm

- Sau khi xây dựng vector đặc trưng cho từng khách hàng, nhóm sử dụng K-Means clustering để phân khúc khách hàng.

- Số cụm K được khảo sát trong khoảng 2–10 bằng Silhouette score, nhằm đánh giá mức độ tách biệt giữa các cụm.

- Silhouette score càng cao cho thấy các điểm trong cùng cụm càng tương đồng và các cụm càng tách biệt rõ ràng.

- Nhóm lựa chọn K tối ưu không chỉ dựa trên giá trị silhouette, mà còn cân nhắc:

* Khả năng diễn giải hành vi

* Tính khả thi trong ứng dụng marketing

- Với K quá nhỏ, cụm quá tổng quát; với K quá lớn, cụm nhỏ và khó diễn giải.

- Sau khi chọn K, mô hình K-Means được huấn luyện trên tập đặc trưng cuối cùng và gán nhãn cụm cho từng khách hàng.

- Kết quả phân cụm được lưu lại dưới dạng bảng (CustomerID, Cluster label, …) để phục vụ các bước phân tích cụm và đề xuất chiến lược marketing.

<img width="175" height="355" alt="image" src="https://github.com/user-attachments/assets/691575c2-e665-4fbd-bdd1-bc45f0b7250c" />

---

## 4. Trực quan hóa và đánh giá phân cụm

- Do vector đặc trưng có số chiều lớn, nhóm sử dụng PCA để giảm chiều dữ liệu xuống 2D nhằm phục vụ trực quan hóa.

- PCA giúp giữ lại phần lớn thông tin quan trọng và cho phép quan sát cấu trúc phân cụm trong không gian 2 chiều.

- Sau khi giảm chiều, nhóm vẽ biểu đồ scatter, trong đó mỗi điểm là một khách hàng và được tô màu theo nhãn cụm.

  <img width="921" height="739" alt="image" src="https://github.com/user-attachments/assets/8cd67d2d-392f-4d3a-a966-0754a4a1eb3e" />


- Quan sát biểu đồ cho thấy:

* Các cụm có xu hướng phân bố thành những vùng tương đối riêng biệt

* Một số mức chồng lấn giữa các cụm vẫn tồn tại, phản ánh tính giao thoa tự nhiên của hành vi mua sắm

- Việc sử dụng đặc trưng nâng cao (luật có trọng số + RFM) giúp các cụm tách biệt rõ ràng hơn so với đặc trưng nhị phân.

- Kết quả trực quan cho thấy mô hình phân cụm tạo ra các nhóm khách hàng hợp lý và có thể diễn giải, đủ tốt để phục vụ bước đề xuất chiến lược marketing.

## 5. So sánh có hệ thống giữa các biến thể đặc trưng

Thực hiện so sánh giữa các cấu hình:

- Rule-only vs Rule + RFM

  <img width="474" height="217" alt="image" src="https://github.com/user-attachments/assets/284d8f84-7a4b-466c-85fa-b66599997f02" />


- Binary rules vs Weighted rules

- Top-K nhỏ vs Top-K lớn

Sử dụng Silhouette score và khả năng diễn giải để đánh giá.

Kết quả được tổng hợp trong bảng so sánh cấu hình, từ đó lựa chọn cấu hình cuối cùng tối ưu.

## 6. Profiling và diễn giải cụm khách hàng

Với mỗi cụm, nhóm thực hiện:

- Thống kê số lượng khách hàng theo cụm

- Báo cáo trung bình RFM theo cụm (nếu dùng RFM)

- Xác định dấu hiệu đặc trưng hành vi thông qua: Top 10 luật / rule-features được kích hoạt nhiều nhất

- Đặt tên cụm:

* 1 tên tiếng Anh

* 1 tên tiếng Việt

- Mô tả persona của cụm trong 1 câu

- Đề xuất chiến lược marketing cụ thể (bundle, cross-sell, upsell, chăm sóc VIP, kích hoạt khách ngủ đông…), gắn trực tiếp với đặc trưng dữ liệu của cụm.

## 7. Dashboard Streamlit

- Xây dựng dashboard bằng Streamlit để trực quan hóa kết quả.

- Dashboard đọc file output, không chạy lại model.

- Chức năng chính:

* Lọc khách hàng theo cụm

* Xem top rule-features theo cụm

* Gợi ý bundle / cross-sell theo cụm

- Dashboard giúp chuyển kết quả phân tích thành công cụ hỗ trợ marketing thực tế.
