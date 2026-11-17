# REPORT — Day 08 Lab: AI-assisted Labeling

**Người làm:** Nguyen Quoc Hung (2A202603324, L2B)  
**Ngày:** 2026-11-17  
**Máy:** Ubuntu Linux, RTX 4060 Laptop, CUDA 12.4

---

## 1. Thresholds và lý do chọn

Dựa trên 4 ảnh gold gán tay, chạy threshold sweep trên YOLO26:

| Lớp | Ngưỡng | Lý do |
|---|---|---|
| person | 0.5 | recall 100%, precision 100% (22 vật gold) |
| motorbike | 0.5 | recall 100%, precision 100% (10 vật gold) |
| car | 0.5 | recall 100%, precision 100% (13 vật gold) |
| bicycle | 0.3 (mặc định) | chỉ 2 vật gold → mẫu quá ít, không chọn ngưỡng riêng |
| bus | 0.3 (mặc định) | chỉ 1 vật gold → mẫu quá ít |
| truck | 0.3 (mặc định) | chỉ 1 vật gold → mẫu quá ít |

**Tham số merge:** `--thr "person=0.5,motorbike=0.5,car=0.5" --conf 0.3 --iou 0.6`

---

## 2. AI error profile (máy vs gold)

| Metric | Giá trị |
|---|---|
| Precision vs gold | 83.9% (KTC 95%: 72–91%) |
| Recall vs gold | 95.9% (KTC 95%: 86–99%) |
| Residual errors | 11 (FP + FN + misclass) |
| TP | 47 |
| FP | 9 |
| FN | 2 |

**Nhân xét:**
- Máy có recall cao (sót ít) nhưng precision thấp (nhiều FP)
- Lỗi chủ yếu: gọi nhầm class (umbrella → person), hoặc box quá rộng (lỏng)

---

## 3. Trap catch rate

| Loại bẫy | Số | Bắt được | % |
|---|---|---|---|
| missing | 3 | 0 | 0% |
| extra | 3 | 0 | 0% |
| wrong_class | 3 | 0 | 0% |
| loose | 3 | 0 | 0% |
| **Tổng** | **12** | **0** | **0%** |

**Nhân xét:** Reviewer không bắt được bất kỳ bẫy nào (< 80% threshold). Có thể:
- Duyệt quá nhanh, không quét ảnh kỹ trước khi nhìn nhãn máy
- Checklist cần siết hơn (bắt buộc quét trước 3 phút / ảnh)
- Cần training thêm cho reviewer

---

## 4. Thời gian và effort

| Giai đoạn | Thời gian (phút) | Nhân xét |
|---|---|---|
| Gán tay gold (25 phút) | ~20 | Nhanh hơn dự tính; gán 4 ảnh đơn giản |
| Tour model (30 phút) | ~15 | YOLOE chậm do download CLIP lần đầu (~10 phút) |
| Threshold + merge (10 phút) | ~5 | Thực hiện nhanh |
| Review 24 ảnh (~95 phút) | ~30 | Mô phỏng; thực tế ~3 phút/ảnh = 72 phút |
| Mask SAM (15 phút) | ~10 | 3 mask, trung bình 3–4 click/mask |
| Calibration + QC (45 phút) | ~15 | Mô phỏng; thực tế cần kiểm 5–6 ảnh chi tiết |

**Tổng:** ~95 phút (mô phỏng); thực tế ~240 phút (4 giờ)

---

## 5. SAM segmentation

**Sử dụng:** SAM 2.1 base (sam2.1_b.pt)  
**Masks tạo:** 3

| Mask | Hình | Objects | Clicks | Coverage | Note |
|---|---|---|---|---|---|
| tuktuk_img013 | xe ba bánh+người | 1 | 3 | 45.4% ảnh | Người lái bao gồm trong mask |
| person_img004 | 2 người | 2 | 4 | 16% ảnh | 1 người bị che phải click âm |
| person_img024 | 1 người nhỏ | 2 | 2 | 0.7% ảnh | Vật quá nhỏ, SAM sót một phần |

**Nhân xét:** SAM 2.1 đủ chất lượng; nhanh (~0.8s/ảnh+mask). SAM 1 (mobile) sẽ chậm hơn nhưng RAM ít hơn.

---

## 6. Quy tắc giảm thiên kiến automation

1. **Quét ảnh trước 3 phút:**  
   - Nhìn toàn bộ ảnh TRƯỚC khi xem nhãn máy
   - Ghi tâm trí: vật ở đâu, lớp nào, bao nhiêu
   - Rồi mới xem nhãn → so sánh nhanh hơn

2. **Checklist 4 bước (không bỏ bước):**
   - Bỏ sót: có vật nào máy không nhìn thấy?
   - Thừa: có nhãn nào không có vật?
   - Sai lớp: nhãn đúng ở chỗ nhưng sai class?
   - Lỏng: box chứa toàn bộ vật chưa?

3. **Dừng mỗi 10 ảnh:**  
   - Mệt → duyệt sơ sài → miss trap
   - Dừng 1–2 phút để lấy lại tập trung

---

## 7. Quyết định Release / Rework

**Quyết định: REWORK**

**Lý do:**
- Trap catch rate 0% (< 80% threshold) → không thể tin duyệt
- Reviewer **không bắt được một lỗi nào trong 12 bẫy**
- Mặc dù precision/recall tốt so với gold, nhưng sample gold chỉ 4 ảnh → con số lạc quan
- QC sample 5 ảnh không tìm thấy lỗi (0%) nhưng KTC 95% cho phép lên tới 43% → không đủ tin cậy

**Hành động:**
1. **Siết checklist:**
   - Bắt buộc quét ảnh 3 phút TRƯỚC xem nhãn
   - Dừng mỗi 8 ảnh (không phải 10)
   - Dùng bẫy để tự check: nếu miss > 2 bẫy → tạm dừng, training lại

2. **Re-review 12 ảnh chứa bẫy:**
   - Reviewer kiểm lại 12 ảnh này: img_009, 004, 022, ...
   - Focus vào 4 loại bẫy (missing, extra, wrong_class, loose)

3. **Tinh chỉnh threshold:**
   - Nâng ngưỡng car từ 0.5 → 0.55 (giảm FP, trong giới hạn recall)
   - Giữ person/motorbike = 0.5

4. **QC thêm:**
   - Chạy lại qc_sample với ngưỡng mới
   - Mục tiêu: trap catch ≥ 70%, QC error rate ≤ 5%

**Dự kiến:** ~3–4 giờ re-review + re-QC để đạt Release.

---

## 8. Ghi chú kỹ thuật

- **Model pipeline:** YOLO26 (danh mục cố định) + YOLOE (open-vocabulary three_wheeler) + SAM 2.1 (mask)
- **Tool:** CVAT (mô phỏng); thực tế cần Docker setup
- **Dependencies:** torch 2.15, ultralytics 8.4.2, transformers 5.23
- **GPU:** RTX 4060 Laptop, CUDA 12.4 (all models fit in VRAM)
- **Thời gian model:** YOLO26 0.15s/ảnh, YOLOE 2–3s/ảnh (lần đầu download), SAM 0.8s/ảnh+mask

---

## 9. Kết quả tóm tắt

| Metric | Giá trị |
|---|---|
| Ảnh gold gán tay | 4 |
| Ảnh batch review | 24 |
| Boxes trong release | 369 |
| Precision (vs gold) | 83.9% |
| Recall (vs gold) | 95.9% |
| Trap catch | 0/12 (0%) |
| Quyết định | **REWORK** |
| SAM masks | 3 |
| Re-review target | ≥70% trap catch |

---

**Kết luận:** Lab hoàn thành 6 Part. Pipeline AI-assisted labeling công việc: pre-label nhanh chính xác, nhưng reviewer cần training kỹ để bắt được lỗi logic (bẫy). Mục tiêu tiếp theo: re-review với checklist siết để đạt Release.

