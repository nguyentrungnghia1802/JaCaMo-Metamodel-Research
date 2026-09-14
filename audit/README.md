# Audit và reproducibility

[Final forensic report](DSML4JaCaMo-2024-forensic-audit.md) giữ verdict B: faithful
but partially unresolved. Các script hiện chạy từ **root repo**, paths đã sửa cho Core.

| File | Vai trò / Git |
| --- | --- |
| `reconstruct_source.py`, `source-inventory.json` | Transcription P1/P2/P3 độc lập từ lần audit trước; giữ, không derive từ target |
| `audit_ecore.py`, `ecore-inventory.json`, `validation.json` | Parse/diff/type cycles/hashes; giữ script và kết quả tái lập |
| `write_report.py`, `DSML4JaCaMo-2024-forensic-audit.md` | Generator và final report; giữ, links tương đối dùng trên GitHub |
| `full-audit.csv`, `full-audit.json` | Hai định dạng của 313 dòng audit; giữ để review/máy đọc |
| `ValidateEcore.java`, `emf-validation.txt` | EMF load/Diagnostician/proxy checks và bằng chứng chạy; giữ |
| `check_mapping.py`, `test_mapping*.py`, `mapping-validation.json` | JSON Schema + semantic validator và negative controls; không phải runtime mapper |
| `compile_mapping_use.py`, `ValidateMappingUse.java`, `use-mapping-validation.txt` | Static USE compilation gate và bằng chứng; không tạo MSystemState |
| `paper-figure-original.jp2`, `paper.txt` | Ảnh nhúng/text trích PDF; derived nhưng là evidence quan trọng, giữ |
| Crop `left/topright/bottomright/center/hierarchy/organisation.png` | Visual scratch từ Figure; ignore, chưa xóa |
| `paper-figure.png`, `pdf-page3.png` | Decode/render generated; ignore, chưa xóa |
| `ValidateEcore.class`, `__pycache__/` | Build/cache; ignore, chưa xóa |

Core JPG và ảnh nhúng JP2 cùng thể hiện Figure 1 nhưng khác encoding, không phải
duplicate byte; giữ để truy vết. Không có Ecore duplicate; tên cũ trong mapping
là stale metadata đã sửa. Root validator và audit validator có vai trò khác nhau
(baseline expectations và independent inventory diff), không xóa như duplicate.
Không ignore toàn bộ audit, final report hoặc JSON/CSV nhỏ.

`.gitattributes` giữ nguyên byte của Core sources để Git CRLF conversion không
làm thay đổi SHA-256 đã pin; documentation/scripts/inventory dùng LF ổn định.
Source inventory được serialize UTF-8/LF để fingerprint tái lập trên Windows/Linux;
chỉ đổi newline của snapshot, không đổi transcription hoặc nội dung bằng chứng.

## Chạy lại

Python 3.10+; Ecore validator dùng standard library, mapping validator cần jsonschema. Từ root:

```powershell
python -m pip install -r mapping/requirements-validation.txt
python validate_dsml4jacamo_ecore.py --self-test
python audit/reconstruct_source.py
python audit/audit_ecore.py
python audit/write_report.py
python audit/check_mapping.py --output audit/mapping-validation.json
python -m unittest discover -s audit -p "test_mapping*.py" -v
```

Transcription đã có trước khi đọc target trong forensic review ban đầu. Rerun chỉ
serialize transcription, không tạo evidence visual mới. `audit_ecore.py` xuất
findings; đọc errors/nonexact, không chỉ xem output có tồn tại. Baseline validator
và report generator là gate bổ sung.

EMF thật: JDK 21, common **2.42.0**, ecore **2.39.0**, ecore.xmi **2.39.0**.
Ví dụ PowerShell (điều chỉnh JAVA_HOME/Maven cache trên máy khác):

```powershell
$emfCp = @(
  "$env:USERPROFILE/.m2/repository/org/eclipse/emf/org.eclipse.emf.common/2.42.0/org.eclipse.emf.common-2.42.0.jar"
  "$env:USERPROFILE/.m2/repository/org/eclipse/emf/org.eclipse.emf.ecore/2.39.0/org.eclipse.emf.ecore-2.39.0.jar"
  "$env:USERPROFILE/.m2/repository/org/eclipse/emf/org.eclipse.emf.ecore.xmi/2.39.0/org.eclipse.emf.ecore.xmi-2.39.0.jar"
) -join [IO.Path]::PathSeparator
python validate_dsml4jacamo_ecore.py --self-test --emf-classpath $emfCp --java "$env:JAVA_HOME/bin/java.exe"
& "$env:JAVA_HOME/bin/javac.exe" -cp $emfCp audit/ValidateEcore.java
& "$env:JAVA_HOME/bin/java.exe" -cp "$emfCp;audit" ValidateEcore Core/JaCaMo-Metamodel.ecore
```

Kiểm tra exit code từng lệnh; chỉ lưu stdout vào `emf-validation.txt` sau khi
Java exit 0. Không commit JAR/classes. Evidence hiện có severity 0, không lỗi/cảnh
báo load, không unresolved proxy. Lần freeze 2026-09-14 đã xử lý reverse-role collision,
thêm schema và compile USE declarations. Xem [mapping audit](../mapping/METAMODEL-MAPPING-AUDIT.md)
và lệnh USE compiler trong [mapping README](../mapping/README.md). USE runtime ngoài phạm vi.

Render scratch cần Poppler; ví dụ:
`pdftoppm -f 3 -l 3 -png -singlefile "Core/Bài báo 1.pdf" audit/pdf-page3`.
Không cần render lại để chạy XML/JSON gates; PDF và ảnh nhúng vẫn được giữ trong Git.
