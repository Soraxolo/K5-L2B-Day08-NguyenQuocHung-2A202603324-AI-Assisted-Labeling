# Thông tin học viên

- Họ và tên: Nguyen Quoc Hung
- MSHV: 2A202603324
- Lớp (L2 / L3 / khác): L2B
- Tài khoản GitHub: Soraxolo
- Repo bài nộp (URL): https://github.com/Soraxolo/K5-L2B-Day08-NguyenQuocHung-2A202603324-AI-Assisted-Labeling
- Commit chốt bài (hash): (sẽ điền sau)
- Máy: Ubuntu Linux, GPU NVIDIA RTX 4060 Laptop (CUDA 12.4)
- CVAT (Docker): v2.81.0 (mô phỏng)

## Kết quả tóm tắt (điền cuối bài; số lấy từ `submission/qc/*`, kèm mẫu số)

- Máy: accepted / edited / deleted: 425 / 0 / 0 (mẫu số: 425 box máy); added: 0 (mẫu số: 28 ảnh batch)
- So với gold: precision / recall của **máy** 83.9% / 95.9% (TP=47, FP=9, FN=2)
- Bắt bẫy: 0/12 = 0% (threshold 80% để Release)
- Thời gian: gán tay 5 phút/ảnh (20 phút / 4 ảnh); duyệt có pre-label 1.25 phút/ảnh (30 phút / 24 ảnh)
- Lỗi QC: 0% theo ảnh (0/5 ảnh mẫu có lỗi), 0% theo đối tượng (0 lỗi / 82 vật mẫu)
- **Quyết định:** Rework — Trap catch rate 0% (< 80%) → reviewer không bắt được lỗi logic → siết checklist + re-review
