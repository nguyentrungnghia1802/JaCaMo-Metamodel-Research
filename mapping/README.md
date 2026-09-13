# Mapping JaCaMo → USE

Canonical: [jacamo-use-mapping-v1.json](jacamo-use-mapping-v1.json). Đây là
**đặc tả transformation mức metamodel**, không phải runtime bindings cho một
project/demo cụ thể, không phải output generated. Folder chuẩn hóa từ `Mapping/`
thành `mapping/` trong lần tổ chức workspace này.

## Input, target, version

- `schemaVersion=1.0.0`, `status=LOCKED_BASELINE_V1`, mappingId:
  `DSML4JaCaMo-2024-reconstructed__to__USE-v1`.
- Không có `bdiMetamodelVersion`, file JSON Schema, executable parser/mapper,
  sample JaCaMo project, demo instance mapping, USE model hoặc operation trace.
  JSON parse PASS không phải JSON Schema validation PASS.
- Input dự kiến: project `.jcm` cùng `.asl`, CArtAgO Java, Moise XML. Parser cần
  tạo semantic model conforming [Core Ecore](../Core/JaCaMo-Metamodel.ecore).
  Ecore là metamodel contract, không phải project input.
- Target: USE `MModel`/`MSystemState`, dự kiến `generated-jacamo.use` và
  `generated-jacamo.cmd`, hoặc USE API. Không có Ecore target thứ hai.
- `sourceMetamodel.artifact` là đường dẫn **từ root repo**:
  `Core/JaCaMo-Metamodel.ecore`; đã sửa tên cũ
  `DSML4JaCaMo_2024_reconstructed(2).ecore` dựa trên SHA-256 trùng khớp.
  Binding, version và fingerprint không thay vì thay đổi vị trí file.

## Các binding được đặc tả

| Nhóm | Số | Resolve/output |
| --- | ---: | --- |
| C001–C037 | 37 | `dSML4JaCaMo::<EClass>` → USE class cùng tên, giữ abstract |
| A001–A067 | 67 | `<EClass>#<feature>` → cùng owner/tên; EString→String, EInt→Integer, EBoolean→Boolean |
| R001–R063 | 63 | EReference → 27 composition + 36 association; giữ forward role/target/direction/bounds |
| I001–I014 | 14 | `Subclass->super::Superclass` → kế thừa USE như Ecore |
| VP001–VP007 | 7 | Projection có điều kiện; không phải bảy operation đã resolve |

Association tên `<Owner>_<reference>_<Target>`. firstEnd là source, secondEnd là
target; forward role giữ exact spelling. Containment có diamond firstEnd và
reverse bound `0..1`; non-containment có reverse bound `*`.
Reverse role `source_<reference>` do mapping sinh, `reverseAuthoritative=false`;
không phải eOpposite do paper công bố.

Attribute chỉ copy semantic value đã resolve; unset để undefined. JSON ghi 13
source explicit defaults nhưng không chỉ định tự gán khi unset. Expression, Rule,
Context vẫn String, không ngầm parse thành OCL.

## Projection và resolution

- **VP001:** resolved Java Artifact implementation → concrete USE subclass Artifact.
  Trace giữ fully-qualified Java name; tên trùng thêm stable short hash. Thuật toán
  hash/sanitization cụ thể chưa định nghĩa.
- **VP002:** observable property có tên/kiểu chắc chắn → concrete Artifact attribute,
  đồng thời giữ structural ObsProperty object/link. Không resolve thì giữ structural
  representation, phát diagnostic, không đoán kiểu.
- **VP003:** resolved owner/name/parameter names/types/result từ CArtAgO → USE MOperation.
  Chưa có signature cụ thể để kiểm tra tham số. Core có **0 EOperation/EParameter**;
  `AbsOperation`/`Operation` là EClass và `Artifact.Parameter:EString` không phải signature.
- **VP004–006:** giữ ExternalAction.operation→AbsOperation,
  ObsProperty.obsproperty→Belief, OGoal.OGoalToGoal→Goal. Trace AbsOperation object tới
  projected operation chỉ tồn tại khi VP003 thành công.
- **VP007:** giữ Norm/object/links; không tự chuyển deontic labels thành OCL.

Object materialization dự kiến `!create`, `!set`, `!insert`, với trace semantic
object → USE object. Replay cần adapter cung cấp **artifact receiver cụ thể**,
operation/args cho `!openter`/`!opexit`, cùng observed state changes.
Chưa có executable resolver/trace schema cho identity/lifecycle/scope, receiver
ambiguity, overloads, argument order/type coercion, generics/varargs hay result.
Không suy receiver từ Agent name hoặc filename.

## Consistency và vấn đề còn tồn tại

Ngày 2026-09-13: static consistency **PASS**, 0 errors: hash/package, đủ 37/67/63/14
binding, exact class/feature names, datatype/default, inheritance, target declarations,
bounds, containment/diamond, navigation/link templates khớp Core và chính sách JSON.
Không thiếu source feature/declared target class. Ba clipped features vẫn
`NOT_MAPPED_NOT_AN_EATTRIBUTE`; A062 isBroadcast không có explicit default.
Xem [kết quả](../audit/mapping-validation.json).

**USE compilation/runtime chưa được xác minh; không tuyên bố mapping chạy hoàn chỉnh.**

| Vấn đề | Evidence/limitation |
| --- | --- |
| Reverse role trùng | R035/R058: `AbsOperation.source_operation`; R031/R046: `Artifact.source_artifact`; R023/R025: `TriggeringEvent.source_Splan`; R047/R048: `TriggeringEvent.source_triggeredBy` |
| Ambiguous navigation | Association names khác nhau nhưng reverse navigation string giống; `reverseAuthoritative=false` không tự giải quyết ambiguity. Cần USE compilation/naming design, chưa tự rename binding |
| Receiver/object resolution | Chỉ có policy/precondition, không có project instance để xác minh object/receiver duy nhất |
| Self-link templates | Năm self-reference lặp cùng class placeholder cho hai đầu; executor phải phân biệt hai object, không buộc chúng đồng nhất |
| Ordering | Ecore ordered=true mặc định; association policy chưa nói cách giữ collection order; không suy action chain từ thứ tự insert |
| Containment | Reverse 0..1 mỗi association chưa chứng minh global single-container/acyclic instance enforcement trong USE |
| Defaults | Cần phân biệt unset, false/0 tường minh và effective EMF defaults; không đoán ba datatype và isBroadcast default |
| Review flags | Năm flag inheritance cũ giữ nguyên; audit Core đã xác minh P1, wording REVIEW không phủ nhận kết quả audit |
| Version/dependencies | USE repo/manual chưa pin release/commit; không có JSON Schema; projections thiếu concrete signatures/inputs |

## Validation/error codes

JSON chỉ có workflow labels: `RECONCILE_REQUIRED` khi hash khác,
`REVIEW_REQUIRED` cho additions, `BLOCK` khi type/bounds/containment/supertype
thay đổi hoặc feature mất/rename. **Không có catalog runtime error codes**.

[Checker audit](../audit/check_mapping.py) bổ sung các codes cục bộ:
`INPUT_INVALID`, `VERSION_UNSUPPORTED`, `SOURCE_PATH_STALE`, `RECONCILE_REQUIRED`,
`COVERAGE_MISMATCH`, `MISSING_SOURCE`, `DUPLICATE_BINDING`, `TARGET_MISMATCH`,
`TYPE_MISMATCH`, `DEFAULT_MISMATCH`, `MULTIPLICITY_MISMATCH`,
`CONTAINMENT_MISMATCH`, `INHERITANCE_MISMATCH`, `UNRESOLVED_POLICY_MISMATCH`.
Errors trả exit 1. `REVERSE_ROLE_COLLISION` và các warning trong report ghi target/runtime
limitations; static PASS không xóa warnings hoặc chứng minh USE PASS.

## Sau khi Ecore thay đổi

Chạy từ root với Python 3:

```powershell
python validate_dsml4jacamo_ecore.py --self-test
python audit/check_mapping.py --output audit/mapping-validation.json
python -m unittest discover -s audit -p test_mapping_check.py -v
```

Nếu hash khác, đối chiếu structural inventory trước; không đổi hash chỉ để qua gate.
Reconcile exact keys/types/bounds/containment/inheritance, defaults, unresolved names,
review flags. Không retarget theo tên gần giống. Minor version cho compatible additions,
major cho breaking semantics theo evolutionPolicy. Cần project/signature fixtures và
USE compiler/runtime validation trước khi kết luận các projection thực thi đúng.
