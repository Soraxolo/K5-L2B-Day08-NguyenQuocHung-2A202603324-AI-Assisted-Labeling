# Số đo review (det)

- Ảnh tính: 28 (batch,gold); box máy: 414; đối tượng sau duyệt: 414; ngưỡng accepted: IoU >= 0.9
- Đã **loại 22 đối tượng nằm quanh các bẫy** khỏi bảng này: lỗi nhân tạo không phản ánh chất lượng máy.

## 1. Bốn trạng thái (AI error profile)
| Trạng thái | Số | Tỉ lệ | Mẫu số |
|---|---|---|---|
| accepted (giữ nguyên) | 414 | 414/414 = 100.0% | 414 box máy |
| edited (sửa) | 0 | 0/414 = 0.0% | 414 box máy |
| deleted (xoá) | 0 | 0/414 = 0.0% | 414 box máy |
| added (vẽ thêm) | 0 | 0/414 = 0.0% | 414 đối tượng sau duyệt |

Trong số deleted + added, **0 trường hợp là đổi lớp** (máy gán sai lớp, box đúng chỗ): đó không phải máy bỏ sót. Số vật máy **sót thật** ≈ added − đổi lớp = 0.

### Theo lớp
| Lớp | accepted | edited | deleted | added |
|---|---|---|---|---|
| person | 210 | 0 | 0 | 0 |
| bicycle | 14 | 0 | 0 | 0 |
| motorbike | 96 | 0 | 0 | 0 |
| car | 50 | 0 | 0 | 0 |
| bus | 4 | 0 | 0 | 0 |
| truck | 8 | 0 | 0 | 0 |
| three_wheeler | 32 | 0 | 0 | 0 |

## 2. So với gold (nhãn gán tay từ đầu)
Ảnh gold: 4; đối tượng gold: 49 (mẫu số của recall)
| | TP | FP | FN | Precision | Recall |
|---|---|---|---|---|---|
| Máy (pre-label) | 47 | 9 | 2 | 83.9% (KTC 95%: 72–91%) | 95.9% (KTC 95%: 86–99%) |

*Lạc quan: ngưỡng được chọn trên chính các ảnh gold này (in-sample), và chỉ có 4 ảnh. Đọc khoảng tin cậy, đừng đọc con số đơn.*

| Sau duyệt của bạn (4 ảnh gold có trong nhãn cuối) | 47 | 9 | 2 | 83.9% | 95.9% |

- **Residual** (lỗi của máy còn trong nhãn của bạn): 11 (đếm FP + FN; một lỗi sai lớp hoặc lệch vị trí tính 2)
- **New** (lỗi do bạn tạo ra): 0

## 3. Ảnh bẫy
- Bắt được 0/12 = 0.0% (KTC 95%: 0–24%) (ngưỡng đạt: 80%). Chỉ 12 bẫy nên khoảng tin cậy rất rộng: đọc cùng danh sách bẫy lọt, đừng kết luận chỉ từ %.
  - missing: 0/3
  - extra: 0/3
  - wrong_class: 0/3
  - loose: 0/3
  - lọt: img_009.jpg (missing), img_004.jpg (extra), img_022.jpg (wrong_class), img_035.jpg (missing), img_023.jpg (extra), img_014.jpg (loose), img_006.jpg (loose), img_027.jpg (wrong_class), img_024.jpg (extra), img_017.jpg (loose), img_034.jpg (missing), img_013.jpg (wrong_class)

## Gợi ý đọc số
- `deleted` cao → ngưỡng thấp hoặc ánh xạ nhãn sai; `added` cao → máy bỏ sót (xem lớp nào);
- `accepted` thấp (< 50%) → sửa mỗi box lâu hơn vẽ mới: đổi model/ngưỡng hoặc vẽ tay;
- bắt bẫy < 80% → duyệt lại lô, siết checklist (quét ảnh TRƯỚC khi nhìn nhãn máy).
