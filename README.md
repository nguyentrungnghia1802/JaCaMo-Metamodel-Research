# JaCaMo Thesis Workspace

Workspace nghiên cứu metamodel DSML4JaCaMo 2024 và đặc tả chuyển semantic model
JaCaMo sang USE cho validation/thí nghiệm luận văn. Chưa có công cụ chuyển đổi
JaCaMo chạy end-to-end trong repo.

| Vị trí | Vai trò |
| --- | --- |
| [Core/](Core/README.md) | Canonical **[JaCaMo-Metamodel.ecore](Core/JaCaMo-Metamodel.ecore)**, reconstructed theo paper |
| [mapping/](mapping/README.md) | JSON nguồn đặc tả chuyển Ecore-conforming semantic model → USE; không phải output generated |
| [audit/](audit/README.md) | Inventory, validators, final forensic report và kết quả tái lập |
| [Paper](Core/B%C3%A0i%20b%C3%A1o%201.pdf), [Figure 1](Core/Metamodel-2024.jpg) | Source of truth; Figure ưu tiên hơn diễn giải văn bản |
| [Draw.io](Core/JaCaMo-Metamodel.drawio) | Editable trace hỗ trợ lần đường, không phải nguồn tác giả độc lập |
| [validate_dsml4jacamo_ecore.py](validate_dsml4jacamo_ecore.py) | Baseline validator, mutation controls, tùy chọn EMF thật |

```text
Paper / Figure 1
       ↓
Core Ecore (canonical reconstructed baseline)
       ↓
Mapping (nhận semantic model đã parse từ JaCaMo project)
       ↓
USE / validation / thesis experiments (runtime chưa có trong repo)
```

Kiểm tra ngày 2026-09-13: **37 lớp, 67 attribute, 63 reference, 14 kế thừa**;
verdict faithful but partially unresolved. Ba datatype và một default bị che
chưa được đoán. Ngày 2026-09-14, metamodel mapping V1 (schema 1.1.0) đã freeze:
schema/semantic checks và USE metamodel compilation PASS; các role collision và
target keyword đã xử lý. Runtime/binding/resolver vẫn ngoài phạm vi.

Chạy từ root bằng Python 3:

```powershell
python -m pip install -r mapping/requirements-validation.txt
python validate_dsml4jacamo_ecore.py --self-test
python audit/check_mapping.py
python -m unittest discover -s audit -p "test_mapping*.py" -v
```

[audit/README.md](audit/README.md) hướng dẫn EMF/tái tạo audit và phân loại file.
Giữ Core, mapping, README, scripts, final report và JSON/CSV evidence trong Git.
Chỉ ignore crop/render PNG phụ, `.class`, cache/build/temp; không xóa nguồn/evidence.
