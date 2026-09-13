import json,csv,hashlib
from pathlib import Path
from collections import Counter

base=Path.cwd()
s=json.loads(Path('audit/source-inventory.json').read_text(encoding='utf-8'))
e=json.loads(Path('audit/ecore-inventory.json').read_text(encoding='utf-8'))
v=json.loads(Path('audit/validation.json').read_text(encoding='utf-8'))
em={cat:{(x['name'] if cat=='classes' else x['owner']+'.'+x['name']):x for x in e[cat]} for cat in ['classes','attributes','references']}
rows=[]
def add(cat,element,source,current,status='EXACT',confidence='HIGH',action='Giữ nguyên.'):
    rows.append([cat,element,source,current,status,confidence,action])
def b(x): return str(x).lower()
def bounds(x): return f"{x['lowerBound']}..{'*' if x['upperBound']==-1 else x['upperBound']}"
def ref(x): return f"{x['owner']}.{x['name']} -> {x['target']} [{bounds(x)}]; containment={b(x['containment'])}"
def classes(x): return f"abstract={b(x['abstract'])}; eSuperTypes="+(', '.join(x['eSuperTypes']) or '[]')
def lit(x): return 'null (không có literal tường minh)' if x is None else repr(x)
for c in s['classes']:
    add('EClass',c['name'],'P1: hộp '+c['name']+'; '+classes(c),classes(em['classes'][c['name']]))
for a in s['attributes']:
    key=a['owner']+'.'+a['name']; actual=em['attributes'].get(key)
    shown='P1: '+key+' : '+(a['EType'] or 'UNRESOLVED (bị che)')
    if a['defaultValueLiteral'] not in ('NOT_SHOWN','UNRESOLVED'): shown+=' = '+a['defaultValueLiteral']
    if actual:
        current=f"{actual['EType']} [{bounds(actual)}]; defaultValueLiteral={lit(actual['defaultValueLiteral'])}"
        add('EAttribute',key,shown,current)
    else:
        ann=[an for an in em['classes'][a['owner']]['annotations'] if an['details'].get('visibleAttribute')==a['name']]
        assert len(ann)==1
        add('EAttribute',key,shown,'Không có EAttribute; có EAnnotation urn:reconstruction:unresolved, visibleAttribute='+a['name'],'UNRESOLVED_FROM_SOURCE',action='Giữ annotation; không gán EType/default; chỉ bổ sung khi có bằng chứng nguồn.')
for r in s['references']:
    key=r['owner']+'.'+r['name']
    add('EReference',key,'P1: '+ref(r)+'; '+('diamond đen tại source' if r['containment'] else 'không có diamond tại source'),ref(em['references'][key])+'; eOpposite=null')
for c in s['classes']:
    for sup in c['eSuperTypes']:
        add('Generalization',c['name']+' -> '+sup,'P1: đường xám, hollow triangle trỏ vào '+sup,'eSuperTypes chứa #//'+sup)
# These field rows prevent EXACT on observed attribute names/types from implying
# unsupported recovery of author bounds or unshown author defaults.
for a in s['attributes']:
    key=a['owner']+'.'+a['name']; actual=em['attributes'].get(key)
    add('Attribute bounds',key,'P1 không in lowerBound/upperBound; P2/P3 không xác định.',bounds(actual)+' theo mặc định Ecore' if actual else 'Không áp dụng: chưa khai báo EAttribute','INFERRED_NOT_PROVEN' if actual else 'UNRESOLVED_FROM_SOURCE',action='Không coi bounds mặc định là bằng chứng từ tác giả.')
    if a['defaultValueLiteral'] in ('NOT_SHOWN','UNRESOLVED'):
        clipped=a['defaultValueLiteral']=='UNRESOLVED'
        add('Attribute default',key,'P1: isBroadcast : EBoolean =; giá trị sau = bị cắt.' if clipped else 'P1 không hiển thị default tường minh; P2/P3 không xác định.',('defaultValueLiteral='+lit(actual['defaultValueLiteral'])+('; effective EBoolean default=false' if clipped else '')) if actual else 'Không có EAttribute; annotation ghi unresolved.', 'UNRESOLVED_FROM_SOURCE' if clipped or actual is None else 'INFERRED_NOT_PROVEN',action='Không suy ra default của tác giả từ default nội tại/việc thiếu literal.')
add('Serialization metadata','EPackage nsURI/nsPrefix/name','P1 không cung cấp namespace; P3 Listing 1 dòng 21 có dSML4JaCaMo.Operation.','name=dSML4JaCaMo; nsURI=urn:dsml4jacamo:2024:reconstructed; nsPrefix=dSML4JaCaMo','INFERRED_NOT_PROVEN',action='Giữ metadata địa phương và provenance; không tuyên bố namespace gốc.')
add('Serialization flags','Tất cả EAttribute/EReference','P1 không thể hiện ordered, unique, derived, transient, volatile, unsettable hoặc thiết lập eOpposite nội bộ.','Không đặt các flag này; 63 reference có eOpposite=null.','INFERRED_NOT_PROVEN',action='Giữ mặc định; EXACT của reference chỉ áp dụng tên/source/target/direction/bounds/containment nhìn thấy.')
header=['Category','Element','Source evidence','Current Ecore','Status','Confidence','Action']
with Path('audit/full-audit.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f); w.writerow(header); w.writerows(rows)
Path('audit/full-audit.json').write_text(json.dumps([dict(zip(header,r)) for r in rows],ensure_ascii=False,indent=2),encoding='utf-8')
def esc(x): return str(x).replace('|','\\|').replace('\n','<br>')
table='| '+' | '.join(header)+' |\n| '+' | '.join(['---']*7)+' |\n'+'\n'.join('| '+' | '.join(esc(c) for c in r)+' |' for r in rows)
links=lambda name: '['+name+']('+name+')'
count=Counter(r[4] for r in rows)
report='''# FORENSIC / AUDIT REVIEW — DSML4JaCaMo 2024

Đối tượng: `Core/JaCaMo-Metamodel.ecore`. Ngày audit: 2026-09-13. Không sửa tệp đầu vào.

## 1. VERDICT

**B. FAITHFUL BUT PARTIALLY UNRESOLVED RECONSTRUCTION**

Không tìm thấy khác biệt ở phần abstract syntax có thể đọc được: 37 EClass (kể cả abstract/concrete), 67 thuộc tính có datatype nhìn thấy, 63 reference với source/target/tên/hướng/multiplicity/containment, 14 generalization và 13 default tường minh đều khớp. Ba thuộc tính có tên nhưng datatype bị che được lưu bằng EAnnotation, không bị gán kiểu đoán. `Message.isBroadcast` giữ EBoolean và ghi rõ default của tác giả chưa xác định.

Không chọn A: Figure 1 có scrollbar, ba datatype và một default bị cắt; attribute bounds và nhiều thiết lập serialization không xuất hiện trong nguồn. Đây là xác nhận mức độ trung thành với bằng chứng công bố, không phải chứng minh đồng nhất với Ecore gốc chưa được cung cấp.

## 2. SOURCE INVENTORY SUMMARY

| Hạng mục nguồn | Kết quả |
| --- | --- |
| EClass | 37 hộp lớp |
| Abstract | 3: AbsOperation, BodyTerm, Action; chữ nghiêng và biểu tượng abstract trong Figure 1 |
| Concrete | 34 lớp còn lại |
| Tên attribute nhìn thấy | 70; 67 có datatype đọc được, 3 chỉ đọc được tên |
| Default tường minh đọc được | 13: 11 literal false, 2 literal intra-group |
| EReference | 63 đường có role label và arrowhead |
| Generalization | 14 nhánh; đếm nhánh subclass, không đếm số tam giác dùng chung |
| Containment | 27 reference có diamond đen ở source; 36 non-containment |
| Multiplicity reference | 34 × 0..*; 13 × 1..1; 9 × 0..1; 7 × 1..* |
| Phần chưa xác định | 3 datatype, 1 default bị cắt, bounds của attribute, nội dung có thể nằm ngoài vùng scrollbar |

**Chuỗi bằng chứng và tính độc lập.** Đọc PDF (6 trang), trích văn bản và ảnh nhúng Figure 1 trang PDF 3 / trang in 639; kiểm tra toàn trang bằng Poppler và các crop từ ảnh. Ảnh nhúng `R34.jp2` và ảnh JPG cung cấp đều có kích thước 2605 × 1296; phóng ảnh không khôi phục nội dung bị scrollbar che. Lưu inventory nguồn bằng `reconstruct_source.py` trước lần đọc Ecore. Không đọc các tệp reconstruction notes, mapping JSON hoặc validator có sẵn để dựng inventory. Sau đó mới parse Ecore, kiểm tra annotations và diff.

P1: Figure 1 của chính PDF; P2: Section III trang PDF 2; P3: Section IV/Listing 1 trang PDF 2 và 4. P4 chỉ là aid: draw.io có 77 edge object (63 association + 14 inheritance), metadata ghi `agent=ChatGPT`, modified 2026-09-12 và trang “Editable vector trace”; vì vậy không coi đó là chứng cứ tác giả độc lập. Mọi cạnh trong inventory được lần trên P1. P5 là target được kiểm tra; provenance trong target không tự chứng minh độ đúng.

**Cross-validation P2/P3.** Section III xác nhận các nhóm Agent/Artifact/Organisation, action chain và các subtype AbsOperation nhưng không xác định ba datatype bị che. Listing 1 xác nhận các đường truy cập sau; không dùng vòng lặp trong Listing để suy ra bounds/containment:

| Listing 1, dòng | Feature được cross-check |
| --- | --- |
| 3, 14, 36 | MAS.agent; MAS.workspace; MAS.organisation |
| 6–9 | Agent.plan; Plan.hasContext; Plan.hasBody; Plan.hasAction; Body.firstAction |
| 15, 20 | Workspace.artifact; Artifact.operation |
| 45, 51, 68 | Organisation.structuralspecification; Organisation.functionalspecification; Organisation.normativespecification |
| 52, 54, 57, 59 | FunctionalSpecification.scheme; Scheme.SchemeOgoal; OGoal.OGoalToOPlan; OPlan.FirstOgoal |
| 69 | NormativeSpecification.norm |
| 53 | sch.id hợp lệ nhờ Scheme kế thừa Organisation.id; không thêm id khai báo trực tiếp vào Scheme |

Section III viết `FormationConstaints`, trong khi P1 ghi `FormationConstraints`: dùng P1. Văn xuôi “mission contains goals” không override Figure 1 `Mission.ogoal` không có diamond. Listing 1 là excerpt, không lấy độ hoàn chỉnh/cú pháp template làm bằng chứng thiếu feature.

## 3. FULL AUDIT TABLE

`EXACT` trên dòng EAttribute chỉ xác nhận tên, datatype và default **khi default thực sự hiển thị**. Các dòng Attribute bounds / Attribute default phía dưới ghi riêng phần không được chứng minh; không được đọc EXACT thành việc mọi thuộc tính serialization đã được khôi phục. `Confidence=HIGH` ở dòng UNRESOLVED là độ chắc chắn rằng bằng chứng đang thiếu, không phải độ chắc chắn của một kiểu/default đoán.

`UNRESOLVED_FROM_SOURCE` cho ba tên thuộc tính không có EAttribute là lựa chọn bảo toàn bằng chứng bằng annotation, không phải bỏ sót một feature có kiểu đã biết. Không dùng `MISSING_IN_ECORE` để buộc đoán datatype.

'''+table+'''

## 4. CRITICAL DIFFERENCES

**Không phát hiện MISMATCH, MISSING_IN_ECORE hoặc EXTRA_IN_ECORE được nguồn xác nhận.** Các giới hạn về ba thuộc tính chưa khai báo và default bị cắt được liệt kê ở mục 5; chúng ngăn kết luận “exact reconstruction”. Annotation bảo tồn tên/bằng chứng nhưng không tạo một EStructuralFeature để model instance gán giá trị.

Các điểm nhạy cảm đã xác minh:

- `MAS.PlatformParamters` là chữ `PlatformParamter` xuống dòng `s`; giữ đúng spelling, không đổi thành PlatformParameters.
- `ObsProperty.obsproperty -> Belief [0..*]`, containment=false: đường từ bên trái ObsProperty chạy ngang sang trái rồi đi xuống, arrowhead vào Belief. Không đảo thành Belief.obsproperty. Phân biệt với `Artifact.obsproperty -> ObsProperty`, containment=true.
- `Norm`, `Group`, `Role`, `Scheme` cùng kế thừa `Organisation`; đường xám chung kết thúc bằng hollow triangle vào Organisation. Cấu trúc khác lạ vẫn giữ nguyên.
- Bốn subtype LinkedOperation/InternalOperation/GuardOperation/Operation đều kế thừa AbsOperation.
- Action kế thừa BodyTerm; ExternalAction, InternalAction, TriggeringEvent kế thừa Action. MentalNotes kế thừa BodyTerm, Message kế thừa InternalAction. TriggeringEvent là concrete.
- Năm self-reference được yêu cầu đều non-containment: Group.hasSubGroups [0..*], Role.Extendsrole [0..1], OGoal.NextOgoal [0..1], Workspace.hasSubworkspace [0..*], Action.nextAction [0..1].
- `Scheme.Splan` và `OPlan.Splan` là hai reference khác nhau cùng tới TriggeringEvent; `Mission.Mplan` là cạnh thứ ba. Không gộp các đường giao nhau.
- `OPlan.FirstOgoal` không có diamond; `Scheme.SchemeOgoal` có diamond. `Mission.ogoal` không có diamond.

**Kiểm tra tính hợp lệ thực thi.** Parse XML độc lập và load bằng EMF Java thật (ecore 2.39.0, xmi 2.39.0, common 2.42.0; JDK 21.0.5), resolveAll và Diagnostician trên EPackage: severity=0, resource errors=0, warnings=0, unresolved proxies=0. Đếm EMF: 37 EClass, 67 EAttribute, 63 EReference, 14 supertype entries. Đây là kiểm tra Ecore/XMI, không chỉ well-formed XML. Phạm vi Diagnostician theo [EMF Validation Overview](https://help.eclipse.org/latest/topic/org.eclipse.emf.doc/references/overview/EMF.Validation.html); tài liệu EMF chỉ hỗ trợ phương pháp kiểm tra, không bổ sung baseline DSML4JaCaMo.

| Structural check | Kết quả |
| --- | --- |
| XML well-formed; EPackage root; XMI 2.0 | PASS |
| Load Ecore và EMF Diagnostician | PASS, severity 0 |
| Duplicate classifiers | 0 |
| Duplicate local structural features | 0 |
| Inherited feature-name collisions | 0 |
| Invalid/unresolved ETypes hoặc superclass targets | 0 |
| Invalid bounds / visible literal types | 0 |
| eOpposite | Không khai báo trên cả 63 reference; không có opposite proxy lỗi |
| Inheritance cycles | 0 |
| Direct declared containment type cycles | 0 |
| Effective containment type cycles, có kế thừa | 13 simple cycles; lưu đủ trong validation.json |

**Không đánh đồng hai loại cycle.** Khi xét feature thừa kế, tồn tại đường type-level như `Norm -> NormativeSpecification -> Norm`, `Group -> StructuralSpecification -> Group`, `Role -> StructuralSpecification -> Role`, `Scheme -> FunctionalSpecification -> Scheme`. Ví dụ Norm kế thừa Organisation.normativespecification, còn NormativeSpecification.norm chứa Norm. Đây là cấu trúc đệ quy ở mức kiểu được P1 quy định, không phải một EObject tự nằm trong cây containment của chính nó. Các cạnh quay lại norm/group/role/scheme đều có lowerBound=0 nên ví dụ này cũng không tự buộc cây instance vô hạn. Không có model instance được cung cấp để kiểm tra vòng containment instance. Không xóa inheritance hoặc containment để làm mất những chu trình kiểu này.

## 5. UNRESOLVED EVIDENCE

| Element | Tên đọc được? | Datatype đọc được? | Default tác giả | Xử lý hiện tại |
| --- | --- | --- | --- | --- |
| ObsProperty.initialValue | Có, initialValue | Không; phần dưới bị che | UNRESOLVED | EAnnotation trên ObsProperty; không EAttribute |
| AbsOperation.paramName | Có, paramName | Không; phần dưới bị che | UNRESOLVED | EAnnotation trên AbsOperation; không EAttribute |
| TriggeringEvent.addAndDel | Có, addAndDel | Không; phần dưới bị che | UNRESOLVED | EAnnotation trên TriggeringEvent; không EAttribute |
| Message.isBroadcast | Có | Có, EBoolean | UNRESOLVED: thấy dấu =, không thấy value | EAttribute EBoolean; defaultValueLiteral=null; annotation giải thích |

EMF xác nhận `Message.isBroadcast.getDefaultValue()` là false và `getDefaultValueLiteral()` là null. false này là giá trị nội tại của EBoolean, **không phải default tường minh của tác giả**. Không đặt `defaultValueLiteral="false"` chỉ vì runtime trả false.

Ngoài bốn trường hợp trên, Figure không in attribute multiplicities. Để bounds 0..1 trong Ecore là quyết định mặc định được provenance công khai, trạng thái INFERRED_NOT_PROVEN. Các attribute không hiện `=...` không cho phép chứng minh tác giả không đặt default; không tự điền literal. Scrollbar cũng khiến tổng số thuộc tính ẩn hoàn toàn không xác định được; 70 là số tên **nhìn thấy**, không phải tuyên bố tổng số tuyệt đối của metamodel gốc.

## 6. RELATIONSHIP AUDIT

Toàn bộ 63 reference dưới đây đã được so sánh, đều EXACT trên sáu mặt đọc được: source, role name, target, direction, multiplicity và containment. `*` tương đương upperBound=-1 trong XML. Tất cả eOpposite hiện tại đều null; không suy ra một opposite không được vẽ.

```text
'''+ '\n'.join(ref(r) for r in s['references'])+'''
```

Toàn bộ 14 generalization, mỗi dòng là một quan hệ trực tiếp:

```text
'''+ '\n'.join(c['name']+' -> '+sup for c in s['classes'] for sup in c['eSuperTypes'])+'''
```

## 7. FINAL CONFIDENCE

Coverage dưới đây dùng denominator từ **phần nguồn nhìn thấy**, không phải xác suất đúng. Độ tin cậy định tính của đối chiếu phần này: HIGH; độ hoàn chỉnh đối với metamodel tác giả chưa công bố: chưa thể xác định.

| Hạng mục | Coverage và phạm vi |
| --- | --- |
| EClass coverage | 37/37 = 100%, gồm abstract/concrete |
| Attribute coverage | 67/70 = 95.71% tên nhìn thấy đã có EAttribute; 3/70 còn lại được giữ bằng EAnnotation |
| Attribute datatype, trong phần có thể đọc | 67/67 = 100%; không dùng tỷ lệ này để che ba datatype chưa biết |
| Visible attribute-name evidence coverage | (67 + 3)/70 = 100%; annotation không tương đương EAttribute |
| Reference coverage | 63/63 = 100% |
| Multiplicity coverage | 63/63 = 100% cho reference; attribute multiplicity không đủ evidence để tính tỷ lệ khớp |
| Containment coverage | 63/63 = 100% quyết định true/false; 27/27 diamond đen được bảo toàn |
| Inheritance coverage | 14/14 = 100% |
| Explicit visible default coverage | 13/13 = 100%; riêng Message.isBroadcast vẫn unresolved |
| Toàn bộ thuộc tính, kể cả vùng scrollbar không nhìn thấy | Không tính phần trăm: denominator không xác định |

## 8. RECOMMENDED PATCH

**Không đề xuất patch.** Không có lỗi chắc chắn từ P1/P2/P3. Ba datatype thiếu và một default bị cắt đã có annotation đúng chính sách yêu cầu. Sửa spelling, đổi hướng obsproperty, bỏ inheritance Organisation, đổi self-reference sang containment, hoặc thêm kiểu/default đoán đều không được nguồn hỗ trợ.

Giữ nguyên namespace địa phương có provenance. Không thêm OCL, deontic extensions, runtime semantics hoặc khái niệm từ bài khác. Không tạo thay đổi chỉ để gắn nhãn “verified”.

## 9. VERIFIED FILE

**Không tạo `JaCaMo-Metamodel-verified.ecore`.** Tệp hiện tại đã là reconstruction tốt nhất có thể xác nhận từ evidence được cung cấp. Tệp target và các đầu vào được giữ nguyên byte.

SHA-256 của target trước/sau audit: `'''+v['hashes']['Core/JaCaMo-Metamodel.ecore']+'''`.

Bằng chứng để tái chạy / kiểm tra:

- '''+links('source-inventory.json')+''' — inventory P1/P2/P3 độc lập, không lấy từ target.
- '''+links('ecore-inventory.json')+''' — canonical extraction: abstract, eSuperTypes, attribute bounds/type/default, reference bounds/type/containment/eOpposite và annotations.
- '''+links('full-audit.csv')+''' và '''+links('full-audit.json')+''' — bảng đầy đủ có thể xử lý bằng công cụ.
- '''+links('validation.json')+''' — diff, hash và toàn bộ cycle ở mức kiểu.
- '''+links('emf-validation.txt')+''' — log EMF Diagnostician.
- '''+links('reconstruct_source.py')+''', '''+links('audit_ecore.py')+''', '''+links('ValidateEcore.java')+''' và '''+links('write_report.py')+''' — mã tái lập kết quả. Chỉ `reconstruct_source.py` chứa transcription thủ công; máy không tự đọc hay tự chứng minh notation trong ảnh.

Thống kê dòng audit (có các dòng field-level để phân biệt quan sát và inference): '''+', '.join(k+'='+str(val) for k,val in sorted(count.items()))+'''. Không có dòng MISMATCH/MISSING_IN_ECORE/EXTRA_IN_ECORE.
'''
Path('audit/DSML4JaCaMo-2024-forensic-audit.md').write_text(report,encoding='utf-8')
print('Report:',len(rows),'audit rows;',len(report),'characters;',dict(count))
assert not v['errors']
assert all(d[2]=='UNRESOLVED_FROM_SOURCE' for d in v['nonexact'])
assert hashlib.sha256(Path('Core/JaCaMo-Metamodel.ecore').read_bytes()).hexdigest()==v['hashes']['Core/JaCaMo-Metamodel.ecore']
