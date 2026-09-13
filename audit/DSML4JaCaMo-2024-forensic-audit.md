# FORENSIC / AUDIT REVIEW — DSML4JaCaMo 2024

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

| Category | Element | Source evidence | Current Ecore | Status | Confidence | Action |
| --- | --- | --- | --- | --- | --- | --- |
| EClass | MAS | P1: hộp MAS; abstract=false; eSuperTypes=[] | abstract=false; eSuperTypes=[] | EXACT | HIGH | Giữ nguyên. |
| EClass | Agent | P1: hộp Agent; abstract=false; eSuperTypes=[] | abstract=false; eSuperTypes=[] | EXACT | HIGH | Giữ nguyên. |
| EClass | Workspace | P1: hộp Workspace; abstract=false; eSuperTypes=[] | abstract=false; eSuperTypes=[] | EXACT | HIGH | Giữ nguyên. |
| EClass | Artifact | P1: hộp Artifact; abstract=false; eSuperTypes=[] | abstract=false; eSuperTypes=[] | EXACT | HIGH | Giữ nguyên. |
| EClass | Port | P1: hộp Port; abstract=false; eSuperTypes=[] | abstract=false; eSuperTypes=[] | EXACT | HIGH | Giữ nguyên. |
| EClass | ObsProperty | P1: hộp ObsProperty; abstract=false; eSuperTypes=[] | abstract=false; eSuperTypes=[] | EXACT | HIGH | Giữ nguyên. |
| EClass | AbsOperation | P1: hộp AbsOperation; abstract=true; eSuperTypes=[] | abstract=true; eSuperTypes=[] | EXACT | HIGH | Giữ nguyên. |
| EClass | LinkedOperation | P1: hộp LinkedOperation; abstract=false; eSuperTypes=AbsOperation | abstract=false; eSuperTypes=AbsOperation | EXACT | HIGH | Giữ nguyên. |
| EClass | InternalOperation | P1: hộp InternalOperation; abstract=false; eSuperTypes=AbsOperation | abstract=false; eSuperTypes=AbsOperation | EXACT | HIGH | Giữ nguyên. |
| EClass | GuardOperation | P1: hộp GuardOperation; abstract=false; eSuperTypes=AbsOperation | abstract=false; eSuperTypes=AbsOperation | EXACT | HIGH | Giữ nguyên. |
| EClass | Operation | P1: hộp Operation; abstract=false; eSuperTypes=AbsOperation | abstract=false; eSuperTypes=AbsOperation | EXACT | HIGH | Giữ nguyên. |
| EClass | Organisation | P1: hộp Organisation; abstract=false; eSuperTypes=[] | abstract=false; eSuperTypes=[] | EXACT | HIGH | Giữ nguyên. |
| EClass | NormativeSpecification | P1: hộp NormativeSpecification; abstract=false; eSuperTypes=[] | abstract=false; eSuperTypes=[] | EXACT | HIGH | Giữ nguyên. |
| EClass | StructuralSpecification | P1: hộp StructuralSpecification; abstract=false; eSuperTypes=[] | abstract=false; eSuperTypes=[] | EXACT | HIGH | Giữ nguyên. |
| EClass | FunctionalSpecification | P1: hộp FunctionalSpecification; abstract=false; eSuperTypes=[] | abstract=false; eSuperTypes=[] | EXACT | HIGH | Giữ nguyên. |
| EClass | Norm | P1: hộp Norm; abstract=false; eSuperTypes=Organisation | abstract=false; eSuperTypes=Organisation | EXACT | HIGH | Giữ nguyên. |
| EClass | Group | P1: hộp Group; abstract=false; eSuperTypes=Organisation | abstract=false; eSuperTypes=Organisation | EXACT | HIGH | Giữ nguyên. |
| EClass | Role | P1: hộp Role; abstract=false; eSuperTypes=Organisation | abstract=false; eSuperTypes=Organisation | EXACT | HIGH | Giữ nguyên. |
| EClass | Scheme | P1: hộp Scheme; abstract=false; eSuperTypes=Organisation | abstract=false; eSuperTypes=Organisation | EXACT | HIGH | Giữ nguyên. |
| EClass | FormationConstraints | P1: hộp FormationConstraints; abstract=false; eSuperTypes=[] | abstract=false; eSuperTypes=[] | EXACT | HIGH | Giữ nguyên. |
| EClass | Link | P1: hộp Link; abstract=false; eSuperTypes=[] | abstract=false; eSuperTypes=[] | EXACT | HIGH | Giữ nguyên. |
| EClass | Mission | P1: hộp Mission; abstract=false; eSuperTypes=[] | abstract=false; eSuperTypes=[] | EXACT | HIGH | Giữ nguyên. |
| EClass | OPlan | P1: hộp OPlan; abstract=false; eSuperTypes=[] | abstract=false; eSuperTypes=[] | EXACT | HIGH | Giữ nguyên. |
| EClass | OGoal | P1: hộp OGoal; abstract=false; eSuperTypes=[] | abstract=false; eSuperTypes=[] | EXACT | HIGH | Giữ nguyên. |
| EClass | Belief | P1: hộp Belief; abstract=false; eSuperTypes=[] | abstract=false; eSuperTypes=[] | EXACT | HIGH | Giữ nguyên. |
| EClass | Rule | P1: hộp Rule; abstract=false; eSuperTypes=[] | abstract=false; eSuperTypes=[] | EXACT | HIGH | Giữ nguyên. |
| EClass | Goal | P1: hộp Goal; abstract=false; eSuperTypes=[] | abstract=false; eSuperTypes=[] | EXACT | HIGH | Giữ nguyên. |
| EClass | Plan | P1: hộp Plan; abstract=false; eSuperTypes=[] | abstract=false; eSuperTypes=[] | EXACT | HIGH | Giữ nguyên. |
| EClass | Body | P1: hộp Body; abstract=false; eSuperTypes=[] | abstract=false; eSuperTypes=[] | EXACT | HIGH | Giữ nguyên. |
| EClass | Context | P1: hộp Context; abstract=false; eSuperTypes=[] | abstract=false; eSuperTypes=[] | EXACT | HIGH | Giữ nguyên. |
| EClass | BodyTerm | P1: hộp BodyTerm; abstract=true; eSuperTypes=[] | abstract=true; eSuperTypes=[] | EXACT | HIGH | Giữ nguyên. |
| EClass | Action | P1: hộp Action; abstract=true; eSuperTypes=BodyTerm | abstract=true; eSuperTypes=BodyTerm | EXACT | HIGH | Giữ nguyên. |
| EClass | ExternalAction | P1: hộp ExternalAction; abstract=false; eSuperTypes=Action | abstract=false; eSuperTypes=Action | EXACT | HIGH | Giữ nguyên. |
| EClass | InternalAction | P1: hộp InternalAction; abstract=false; eSuperTypes=Action | abstract=false; eSuperTypes=Action | EXACT | HIGH | Giữ nguyên. |
| EClass | TriggeringEvent | P1: hộp TriggeringEvent; abstract=false; eSuperTypes=Action | abstract=false; eSuperTypes=Action | EXACT | HIGH | Giữ nguyên. |
| EClass | MentalNotes | P1: hộp MentalNotes; abstract=false; eSuperTypes=BodyTerm | abstract=false; eSuperTypes=BodyTerm | EXACT | HIGH | Giữ nguyên. |
| EClass | Message | P1: hộp Message; abstract=false; eSuperTypes=InternalAction | abstract=false; eSuperTypes=InternalAction | EXACT | HIGH | Giữ nguyên. |
| EAttribute | MAS.Name | P1: MAS.Name : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | MAS.PlatformParamters | P1: MAS.PlatformParamters : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Agent.Name | P1: Agent.Name : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Workspace.Name | P1: Workspace.Name : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Workspace.Path | P1: Workspace.Path : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Workspace.Host | P1: Workspace.Host : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Artifact.artifactName | P1: Artifact.artifactName : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Artifact.className | P1: Artifact.className : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Artifact.Parameter | P1: Artifact.Parameter : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Artifact.IDVar | P1: Artifact.IDVar : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Artifact.isInitial | P1: Artifact.isInitial : EBoolean = false | EBoolean [0..1]; defaultValueLiteral='false' | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Port.Name | P1: Port.Name : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | ObsProperty.ParamName | P1: ObsProperty.ParamName : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | ObsProperty.Name | P1: ObsProperty.Name : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | ObsProperty.initialValue | P1: ObsProperty.initialValue : UNRESOLVED (bị che) | Không có EAttribute; có EAnnotation urn:reconstruction:unresolved, visibleAttribute=initialValue | UNRESOLVED_FROM_SOURCE | HIGH | Giữ annotation; không gán EType/default; chỉ bổ sung khi có bằng chứng nguồn. |
| EAttribute | AbsOperation.className | P1: AbsOperation.className : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | AbsOperation.signalExpression | P1: AbsOperation.signalExpression : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | AbsOperation.awaitExpression | P1: AbsOperation.awaitExpression : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | AbsOperation.await_timeExpression | P1: AbsOperation.await_timeExpression : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | AbsOperation.paramName | P1: AbsOperation.paramName : UNRESOLVED (bị che) | Không có EAttribute; có EAnnotation urn:reconstruction:unresolved, visibleAttribute=paramName | UNRESOLVED_FROM_SOURCE | HIGH | Giữ annotation; không gán EType/default; chỉ bổ sung khi có bằng chứng nguồn. |
| EAttribute | Organisation.id | P1: Organisation.id : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Norm.type | P1: Norm.type : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Norm.timeConstraint | P1: Norm.timeConstraint : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Group.Name | P1: Group.Name : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Group.min | P1: Group.min : EInt | EInt [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Group.max | P1: Group.max : EInt | EInt [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Role.Name | P1: Role.Name : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Role.min | P1: Role.min : EInt | EInt [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Role.max | P1: Role.max : EInt | EInt [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Scheme.PlanOperator | P1: Scheme.PlanOperator : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | FormationConstraints.Name | P1: FormationConstraints.Name : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | FormationConstraints.biDir | P1: FormationConstraints.biDir : EBoolean = false | EBoolean [0..1]; defaultValueLiteral='false' | EXACT | HIGH | Giữ nguyên. |
| EAttribute | FormationConstraints.scope | P1: FormationConstraints.scope : EString = intra-group | EString [0..1]; defaultValueLiteral='intra-group' | EXACT | HIGH | Giữ nguyên. |
| EAttribute | FormationConstraints.type | P1: FormationConstraints.type : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | FormationConstraints.to | P1: FormationConstraints.to : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | FormationConstraints.from | P1: FormationConstraints.from : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Link.type | P1: Link.type : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Link.biDir | P1: Link.biDir : EBoolean = false | EBoolean [0..1]; defaultValueLiteral='false' | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Link.scope | P1: Link.scope : EString = intra-group | EString [0..1]; defaultValueLiteral='intra-group' | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Link.from | P1: Link.from : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Link.to | P1: Link.to : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Mission.max | P1: Mission.max : EInt | EInt [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Mission.min | P1: Mission.min : EInt | EInt [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | OPlan.Sequence | P1: OPlan.Sequence : EBoolean = false | EBoolean [0..1]; defaultValueLiteral='false' | EXACT | HIGH | Giữ nguyên. |
| EAttribute | OPlan.Parallel | P1: OPlan.Parallel : EBoolean = false | EBoolean [0..1]; defaultValueLiteral='false' | EXACT | HIGH | Giữ nguyên. |
| EAttribute | OGoal.Name | P1: OGoal.Name : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | OGoal.isRootGoal | P1: OGoal.isRootGoal : EBoolean = false | EBoolean [0..1]; defaultValueLiteral='false' | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Belief.Name | P1: Belief.Name : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Belief.isInitial | P1: Belief.isInitial : EBoolean = false | EBoolean [0..1]; defaultValueLiteral='false' | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Rule.Expression | P1: Rule.Expression : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Goal.Name | P1: Goal.Name : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Plan.Name | P1: Plan.Name : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Plan.asBeliefAddition | P1: Plan.asBeliefAddition : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Plan.asQuery | P1: Plan.asQuery : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Plan.isAtomic | P1: Plan.isAtomic : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Plan.atomicLabel | P1: Plan.atomicLabel : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Plan.argID | P1: Plan.argID : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Plan.isInitial | P1: Plan.isInitial : EBoolean = false | EBoolean [0..1]; defaultValueLiteral='false' | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Body.Name | P1: Body.Name : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Context.Expression | P1: Context.Expression : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Action.Name | P1: Action.Name : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Action.Expression | P1: Action.Expression : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | TriggeringEvent.isSeparateIntention | P1: TriggeringEvent.isSeparateIntention : EBoolean = false | EBoolean [0..1]; defaultValueLiteral='false' | EXACT | HIGH | Giữ nguyên. |
| EAttribute | TriggeringEvent.isInitial | P1: TriggeringEvent.isInitial : EBoolean = false | EBoolean [0..1]; defaultValueLiteral='false' | EXACT | HIGH | Giữ nguyên. |
| EAttribute | TriggeringEvent.ttf | P1: TriggeringEvent.ttf : EInt | EInt [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | TriggeringEvent.ds | P1: TriggeringEvent.ds : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | TriggeringEvent.deletion | P1: TriggeringEvent.deletion : EBoolean = false | EBoolean [0..1]; defaultValueLiteral='false' | EXACT | HIGH | Giữ nguyên. |
| EAttribute | TriggeringEvent.addAndDel | P1: TriggeringEvent.addAndDel : UNRESOLVED (bị che) | Không có EAttribute; có EAnnotation urn:reconstruction:unresolved, visibleAttribute=addAndDel | UNRESOLVED_FROM_SOURCE | HIGH | Giữ annotation; không gán EType/default; chỉ bổ sung khi có bằng chứng nguồn. |
| EAttribute | Message.content | P1: Message.content : EString | EString [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EAttribute | Message.isBroadcast | P1: Message.isBroadcast : EBoolean | EBoolean [0..1]; defaultValueLiteral=null (không có literal tường minh) | EXACT | HIGH | Giữ nguyên. |
| EReference | MAS.agent | P1: MAS.agent -> Agent [1..*]; containment=true; diamond đen tại source | MAS.agent -> Agent [1..*]; containment=true; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | MAS.workspace | P1: MAS.workspace -> Workspace [0..*]; containment=true; diamond đen tại source | MAS.workspace -> Workspace [0..*]; containment=true; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | MAS.organisation | P1: MAS.organisation -> Organisation [0..*]; containment=true; diamond đen tại source | MAS.organisation -> Organisation [0..*]; containment=true; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Agent.belief | P1: Agent.belief -> Belief [0..*]; containment=true; diamond đen tại source | Agent.belief -> Belief [0..*]; containment=true; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Agent.rule | P1: Agent.rule -> Rule [0..*]; containment=true; diamond đen tại source | Agent.rule -> Rule [0..*]; containment=true; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Agent.hasGoal | P1: Agent.hasGoal -> Goal [0..*]; containment=true; diamond đen tại source | Agent.hasGoal -> Goal [0..*]; containment=true; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Agent.plan | P1: Agent.plan -> Plan [0..*]; containment=true; diamond đen tại source | Agent.plan -> Plan [0..*]; containment=true; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Agent.joinWorkspace | P1: Agent.joinWorkspace -> Workspace [0..*]; containment=false; không có diamond tại source | Agent.joinWorkspace -> Workspace [0..*]; containment=false; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Agent.artifact | P1: Agent.artifact -> Artifact [0..*]; containment=false; không có diamond tại source | Agent.artifact -> Artifact [0..*]; containment=false; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Organisation.normativespecification | P1: Organisation.normativespecification -> NormativeSpecification [1..1]; containment=true; diamond đen tại source | Organisation.normativespecification -> NormativeSpecification [1..1]; containment=true; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Organisation.structuralspecification | P1: Organisation.structuralspecification -> StructuralSpecification [1..1]; containment=true; diamond đen tại source | Organisation.structuralspecification -> StructuralSpecification [1..1]; containment=true; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Organisation.functionalspecification | P1: Organisation.functionalspecification -> FunctionalSpecification [1..1]; containment=true; diamond đen tại source | Organisation.functionalspecification -> FunctionalSpecification [1..1]; containment=true; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Organisation.deploysAgent | P1: Organisation.deploysAgent -> Agent [1..*]; containment=false; không có diamond tại source | Organisation.deploysAgent -> Agent [1..*]; containment=false; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | NormativeSpecification.norm | P1: NormativeSpecification.norm -> Norm [0..*]; containment=true; diamond đen tại source | NormativeSpecification.norm -> Norm [0..*]; containment=true; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | StructuralSpecification.group | P1: StructuralSpecification.group -> Group [0..*]; containment=true; diamond đen tại source | StructuralSpecification.group -> Group [0..*]; containment=true; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | StructuralSpecification.role | P1: StructuralSpecification.role -> Role [0..*]; containment=true; diamond đen tại source | StructuralSpecification.role -> Role [0..*]; containment=true; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | FunctionalSpecification.scheme | P1: FunctionalSpecification.scheme -> Scheme [0..*]; containment=true; diamond đen tại source | FunctionalSpecification.scheme -> Scheme [0..*]; containment=true; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Norm.Nrole | P1: Norm.Nrole -> Role [1..1]; containment=false; không có diamond tại source | Norm.Nrole -> Role [1..1]; containment=false; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Norm.NMission | P1: Norm.NMission -> Mission [1..1]; containment=false; không có diamond tại source | Norm.NMission -> Mission [1..1]; containment=false; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Group.hasSubGroups | P1: Group.hasSubGroups -> Group [0..*]; containment=false; không có diamond tại source | Group.hasSubGroups -> Group [0..*]; containment=false; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Group.RefRole | P1: Group.RefRole -> Role [1..*]; containment=false; không có diamond tại source | Group.RefRole -> Role [1..*]; containment=false; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Group.formationconstraints | P1: Group.formationconstraints -> FormationConstraints [0..*]; containment=true; diamond đen tại source | Group.formationconstraints -> FormationConstraints [0..*]; containment=true; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Group.link | P1: Group.link -> Link [0..*]; containment=true; diamond đen tại source | Group.link -> Link [0..*]; containment=true; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Role.Extendsrole | P1: Role.Extendsrole -> Role [0..1]; containment=false; không có diamond tại source | Role.Extendsrole -> Role [0..1]; containment=false; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Role.players | P1: Role.players -> Agent [0..*]; containment=false; không có diamond tại source | Role.players -> Agent [0..*]; containment=false; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Scheme.SchemeOPlan | P1: Scheme.SchemeOPlan -> OPlan [0..*]; containment=true; diamond đen tại source | Scheme.SchemeOPlan -> OPlan [0..*]; containment=true; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Scheme.SchemeOgoal | P1: Scheme.SchemeOgoal -> OGoal [1..*]; containment=true; diamond đen tại source | Scheme.SchemeOgoal -> OGoal [1..*]; containment=true; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Scheme.mission | P1: Scheme.mission -> Mission [1..*]; containment=true; diamond đen tại source | Scheme.mission -> Mission [1..*]; containment=true; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Scheme.Splan | P1: Scheme.Splan -> TriggeringEvent [0..*]; containment=false; không có diamond tại source | Scheme.Splan -> TriggeringEvent [0..*]; containment=false; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Mission.ogoal | P1: Mission.ogoal -> OGoal [1..*]; containment=false; không có diamond tại source | Mission.ogoal -> OGoal [1..*]; containment=false; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Mission.Mplan | P1: Mission.Mplan -> TriggeringEvent [0..*]; containment=false; không có diamond tại source | Mission.Mplan -> TriggeringEvent [0..*]; containment=false; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | OPlan.FirstOgoal | P1: OPlan.FirstOgoal -> OGoal [1..1]; containment=false; không có diamond tại source | OPlan.FirstOgoal -> OGoal [1..1]; containment=false; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | OPlan.Splan | P1: OPlan.Splan -> TriggeringEvent [0..*]; containment=false; không có diamond tại source | OPlan.Splan -> TriggeringEvent [0..*]; containment=false; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | OGoal.NextOgoal | P1: OGoal.NextOgoal -> OGoal [0..1]; containment=false; không có diamond tại source | OGoal.NextOgoal -> OGoal [0..1]; containment=false; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | OGoal.OGoalToOPlan | P1: OGoal.OGoalToOPlan -> OPlan [0..1]; containment=false; không có diamond tại source | OGoal.OGoalToOPlan -> OPlan [0..1]; containment=false; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | OGoal.OGoalToGoal | P1: OGoal.OGoalToGoal -> Goal [0..1]; containment=false; không có diamond tại source | OGoal.OGoalToGoal -> Goal [0..1]; containment=false; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | TriggeringEvent.planoperator | P1: TriggeringEvent.planoperator -> OPlan [0..1]; containment=false; không có diamond tại source | TriggeringEvent.planoperator -> OPlan [0..1]; containment=false; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | TriggeringEvent.triggersPlan | P1: TriggeringEvent.triggersPlan -> Plan [1..1]; containment=false; không có diamond tại source | TriggeringEvent.triggersPlan -> Plan [1..1]; containment=false; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Belief.triggeredBy | P1: Belief.triggeredBy -> TriggeringEvent [1..1]; containment=false; không có diamond tại source | Belief.triggeredBy -> TriggeringEvent [1..1]; containment=false; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Goal.triggeredBy | P1: Goal.triggeredBy -> TriggeringEvent [1..*]; containment=false; không có diamond tại source | Goal.triggeredBy -> TriggeringEvent [1..*]; containment=false; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Workspace.artifact | P1: Workspace.artifact -> Artifact [0..*]; containment=true; diamond đen tại source | Workspace.artifact -> Artifact [0..*]; containment=true; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Workspace.hasSubworkspace | P1: Workspace.hasSubworkspace -> Workspace [0..*]; containment=false; không có diamond tại source | Workspace.hasSubworkspace -> Workspace [0..*]; containment=false; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Artifact.port | P1: Artifact.port -> Port [0..*]; containment=true; diamond đen tại source | Artifact.port -> Port [0..*]; containment=true; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Artifact.obsproperty | P1: Artifact.obsproperty -> ObsProperty [0..*]; containment=true; diamond đen tại source | Artifact.obsproperty -> ObsProperty [0..*]; containment=true; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Artifact.operation | P1: Artifact.operation -> AbsOperation [0..*]; containment=true; diamond đen tại source | Artifact.operation -> AbsOperation [0..*]; containment=true; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Port.linkArtifacts | P1: Port.linkArtifacts -> Artifact [0..*]; containment=false; không có diamond tại source | Port.linkArtifacts -> Artifact [0..*]; containment=false; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | ObsProperty.obsproperty | P1: ObsProperty.obsproperty -> Belief [0..*]; containment=false; không có diamond tại source | ObsProperty.obsproperty -> Belief [0..*]; containment=false; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | AbsOperation.RefObsproperty | P1: AbsOperation.RefObsproperty -> ObsProperty [0..*]; containment=false; không có diamond tại source | AbsOperation.RefObsproperty -> ObsProperty [0..*]; containment=false; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Operation.guardedBy | P1: Operation.guardedBy -> GuardOperation [0..1]; containment=false; không có diamond tại source | Operation.guardedBy -> GuardOperation [0..1]; containment=false; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Operation.callsInternal | P1: Operation.callsInternal -> InternalOperation [0..1]; containment=false; không có diamond tại source | Operation.callsInternal -> InternalOperation [0..1]; containment=false; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | ExternalAction.operation | P1: ExternalAction.operation -> AbsOperation [0..1]; containment=false; không có diamond tại source | ExternalAction.operation -> AbsOperation [0..1]; containment=false; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Plan.RefArtifact | P1: Plan.RefArtifact -> Artifact [0..*]; containment=false; không có diamond tại source | Plan.RefArtifact -> Artifact [0..*]; containment=false; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Plan.hasContext | P1: Plan.hasContext -> Context [1..1]; containment=true; diamond đen tại source | Plan.hasContext -> Context [1..1]; containment=true; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Plan.hasBody | P1: Plan.hasBody -> Body [1..1]; containment=true; diamond đen tại source | Plan.hasBody -> Body [1..1]; containment=true; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Plan.hasAction | P1: Plan.hasAction -> Action [0..*]; containment=true; diamond đen tại source | Plan.hasAction -> Action [0..*]; containment=true; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Body.bodyterm | P1: Body.bodyterm -> BodyTerm [0..*]; containment=true; diamond đen tại source | Body.bodyterm -> BodyTerm [0..*]; containment=true; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Body.firstAction | P1: Body.firstAction -> Action [1..1]; containment=false; không có diamond tại source | Body.firstAction -> Action [1..1]; containment=false; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Action.nextAction | P1: Action.nextAction -> Action [0..1]; containment=false; không có diamond tại source | Action.nextAction -> Action [0..1]; containment=false; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Context.contextRule | P1: Context.contextRule -> Rule [0..*]; containment=false; không có diamond tại source | Context.contextRule -> Rule [0..*]; containment=false; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Context.contextBelief | P1: Context.contextBelief -> Belief [0..*]; containment=false; không có diamond tại source | Context.contextBelief -> Belief [0..*]; containment=false; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | MentalNotes.impliesG | P1: MentalNotes.impliesG -> Goal [1..1]; containment=false; không có diamond tại source | MentalNotes.impliesG -> Goal [1..1]; containment=false; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | MentalNotes.impliesB | P1: MentalNotes.impliesB -> Belief [1..1]; containment=false; không có diamond tại source | MentalNotes.impliesB -> Belief [1..1]; containment=false; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| EReference | Message.messageToagent | P1: Message.messageToagent -> Agent [0..*]; containment=false; không có diamond tại source | Message.messageToagent -> Agent [0..*]; containment=false; eOpposite=null | EXACT | HIGH | Giữ nguyên. |
| Generalization | LinkedOperation -> AbsOperation | P1: đường xám, hollow triangle trỏ vào AbsOperation | eSuperTypes chứa #//AbsOperation | EXACT | HIGH | Giữ nguyên. |
| Generalization | InternalOperation -> AbsOperation | P1: đường xám, hollow triangle trỏ vào AbsOperation | eSuperTypes chứa #//AbsOperation | EXACT | HIGH | Giữ nguyên. |
| Generalization | GuardOperation -> AbsOperation | P1: đường xám, hollow triangle trỏ vào AbsOperation | eSuperTypes chứa #//AbsOperation | EXACT | HIGH | Giữ nguyên. |
| Generalization | Operation -> AbsOperation | P1: đường xám, hollow triangle trỏ vào AbsOperation | eSuperTypes chứa #//AbsOperation | EXACT | HIGH | Giữ nguyên. |
| Generalization | Norm -> Organisation | P1: đường xám, hollow triangle trỏ vào Organisation | eSuperTypes chứa #//Organisation | EXACT | HIGH | Giữ nguyên. |
| Generalization | Group -> Organisation | P1: đường xám, hollow triangle trỏ vào Organisation | eSuperTypes chứa #//Organisation | EXACT | HIGH | Giữ nguyên. |
| Generalization | Role -> Organisation | P1: đường xám, hollow triangle trỏ vào Organisation | eSuperTypes chứa #//Organisation | EXACT | HIGH | Giữ nguyên. |
| Generalization | Scheme -> Organisation | P1: đường xám, hollow triangle trỏ vào Organisation | eSuperTypes chứa #//Organisation | EXACT | HIGH | Giữ nguyên. |
| Generalization | Action -> BodyTerm | P1: đường xám, hollow triangle trỏ vào BodyTerm | eSuperTypes chứa #//BodyTerm | EXACT | HIGH | Giữ nguyên. |
| Generalization | ExternalAction -> Action | P1: đường xám, hollow triangle trỏ vào Action | eSuperTypes chứa #//Action | EXACT | HIGH | Giữ nguyên. |
| Generalization | InternalAction -> Action | P1: đường xám, hollow triangle trỏ vào Action | eSuperTypes chứa #//Action | EXACT | HIGH | Giữ nguyên. |
| Generalization | TriggeringEvent -> Action | P1: đường xám, hollow triangle trỏ vào Action | eSuperTypes chứa #//Action | EXACT | HIGH | Giữ nguyên. |
| Generalization | MentalNotes -> BodyTerm | P1: đường xám, hollow triangle trỏ vào BodyTerm | eSuperTypes chứa #//BodyTerm | EXACT | HIGH | Giữ nguyên. |
| Generalization | Message -> InternalAction | P1: đường xám, hollow triangle trỏ vào InternalAction | eSuperTypes chứa #//InternalAction | EXACT | HIGH | Giữ nguyên. |
| Attribute bounds | MAS.Name | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | MAS.Name | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | MAS.PlatformParamters | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | MAS.PlatformParamters | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Agent.Name | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Agent.Name | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Workspace.Name | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Workspace.Name | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Workspace.Path | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Workspace.Path | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Workspace.Host | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Workspace.Host | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Artifact.artifactName | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Artifact.artifactName | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Artifact.className | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Artifact.className | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Artifact.Parameter | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Artifact.Parameter | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Artifact.IDVar | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Artifact.IDVar | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Artifact.isInitial | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute bounds | Port.Name | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Port.Name | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | ObsProperty.ParamName | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | ObsProperty.ParamName | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | ObsProperty.Name | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | ObsProperty.Name | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | ObsProperty.initialValue | P1 không in lowerBound/upperBound; P2/P3 không xác định. | Không áp dụng: chưa khai báo EAttribute | UNRESOLVED_FROM_SOURCE | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | ObsProperty.initialValue | P1 không hiển thị default tường minh; P2/P3 không xác định. | Không có EAttribute; annotation ghi unresolved. | UNRESOLVED_FROM_SOURCE | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | AbsOperation.className | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | AbsOperation.className | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | AbsOperation.signalExpression | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | AbsOperation.signalExpression | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | AbsOperation.awaitExpression | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | AbsOperation.awaitExpression | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | AbsOperation.await_timeExpression | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | AbsOperation.await_timeExpression | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | AbsOperation.paramName | P1 không in lowerBound/upperBound; P2/P3 không xác định. | Không áp dụng: chưa khai báo EAttribute | UNRESOLVED_FROM_SOURCE | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | AbsOperation.paramName | P1 không hiển thị default tường minh; P2/P3 không xác định. | Không có EAttribute; annotation ghi unresolved. | UNRESOLVED_FROM_SOURCE | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Organisation.id | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Organisation.id | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Norm.type | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Norm.type | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Norm.timeConstraint | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Norm.timeConstraint | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Group.Name | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Group.Name | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Group.min | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Group.min | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Group.max | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Group.max | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Role.Name | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Role.Name | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Role.min | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Role.min | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Role.max | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Role.max | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Scheme.PlanOperator | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Scheme.PlanOperator | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | FormationConstraints.Name | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | FormationConstraints.Name | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | FormationConstraints.biDir | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute bounds | FormationConstraints.scope | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute bounds | FormationConstraints.type | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | FormationConstraints.type | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | FormationConstraints.to | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | FormationConstraints.to | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | FormationConstraints.from | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | FormationConstraints.from | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Link.type | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Link.type | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Link.biDir | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute bounds | Link.scope | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute bounds | Link.from | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Link.from | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Link.to | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Link.to | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Mission.max | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Mission.max | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Mission.min | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Mission.min | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | OPlan.Sequence | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute bounds | OPlan.Parallel | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute bounds | OGoal.Name | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | OGoal.Name | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | OGoal.isRootGoal | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute bounds | Belief.Name | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Belief.Name | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Belief.isInitial | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute bounds | Rule.Expression | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Rule.Expression | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Goal.Name | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Goal.Name | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Plan.Name | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Plan.Name | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Plan.asBeliefAddition | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Plan.asBeliefAddition | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Plan.asQuery | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Plan.asQuery | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Plan.isAtomic | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Plan.isAtomic | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Plan.atomicLabel | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Plan.atomicLabel | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Plan.argID | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Plan.argID | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Plan.isInitial | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute bounds | Body.Name | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Body.Name | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Context.Expression | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Context.Expression | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Action.Name | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Action.Name | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Action.Expression | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Action.Expression | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | TriggeringEvent.isSeparateIntention | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute bounds | TriggeringEvent.isInitial | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute bounds | TriggeringEvent.ttf | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | TriggeringEvent.ttf | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | TriggeringEvent.ds | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | TriggeringEvent.ds | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | TriggeringEvent.deletion | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute bounds | TriggeringEvent.addAndDel | P1 không in lowerBound/upperBound; P2/P3 không xác định. | Không áp dụng: chưa khai báo EAttribute | UNRESOLVED_FROM_SOURCE | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | TriggeringEvent.addAndDel | P1 không hiển thị default tường minh; P2/P3 không xác định. | Không có EAttribute; annotation ghi unresolved. | UNRESOLVED_FROM_SOURCE | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Message.content | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Message.content | P1 không hiển thị default tường minh; P2/P3 không xác định. | defaultValueLiteral=null (không có literal tường minh) | INFERRED_NOT_PROVEN | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Attribute bounds | Message.isBroadcast | P1 không in lowerBound/upperBound; P2/P3 không xác định. | 0..1 theo mặc định Ecore | INFERRED_NOT_PROVEN | HIGH | Không coi bounds mặc định là bằng chứng từ tác giả. |
| Attribute default | Message.isBroadcast | P1: isBroadcast : EBoolean =; giá trị sau = bị cắt. | defaultValueLiteral=null (không có literal tường minh); effective EBoolean default=false | UNRESOLVED_FROM_SOURCE | HIGH | Không suy ra default của tác giả từ default nội tại/việc thiếu literal. |
| Serialization metadata | EPackage nsURI/nsPrefix/name | P1 không cung cấp namespace; P3 Listing 1 dòng 21 có dSML4JaCaMo.Operation. | name=dSML4JaCaMo; nsURI=urn:dsml4jacamo:2024:reconstructed; nsPrefix=dSML4JaCaMo | INFERRED_NOT_PROVEN | HIGH | Giữ metadata địa phương và provenance; không tuyên bố namespace gốc. |
| Serialization flags | Tất cả EAttribute/EReference | P1 không thể hiện ordered, unique, derived, transient, volatile, unsettable hoặc thiết lập eOpposite nội bộ. | Không đặt các flag này; 63 reference có eOpposite=null. | INFERRED_NOT_PROVEN | HIGH | Giữ mặc định; EXACT của reference chỉ áp dụng tên/source/target/direction/bounds/containment nhìn thấy. |

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
MAS.agent -> Agent [1..*]; containment=true
MAS.workspace -> Workspace [0..*]; containment=true
MAS.organisation -> Organisation [0..*]; containment=true
Agent.belief -> Belief [0..*]; containment=true
Agent.rule -> Rule [0..*]; containment=true
Agent.hasGoal -> Goal [0..*]; containment=true
Agent.plan -> Plan [0..*]; containment=true
Agent.joinWorkspace -> Workspace [0..*]; containment=false
Agent.artifact -> Artifact [0..*]; containment=false
Organisation.normativespecification -> NormativeSpecification [1..1]; containment=true
Organisation.structuralspecification -> StructuralSpecification [1..1]; containment=true
Organisation.functionalspecification -> FunctionalSpecification [1..1]; containment=true
Organisation.deploysAgent -> Agent [1..*]; containment=false
NormativeSpecification.norm -> Norm [0..*]; containment=true
StructuralSpecification.group -> Group [0..*]; containment=true
StructuralSpecification.role -> Role [0..*]; containment=true
FunctionalSpecification.scheme -> Scheme [0..*]; containment=true
Norm.Nrole -> Role [1..1]; containment=false
Norm.NMission -> Mission [1..1]; containment=false
Group.hasSubGroups -> Group [0..*]; containment=false
Group.RefRole -> Role [1..*]; containment=false
Group.formationconstraints -> FormationConstraints [0..*]; containment=true
Group.link -> Link [0..*]; containment=true
Role.Extendsrole -> Role [0..1]; containment=false
Role.players -> Agent [0..*]; containment=false
Scheme.SchemeOPlan -> OPlan [0..*]; containment=true
Scheme.SchemeOgoal -> OGoal [1..*]; containment=true
Scheme.mission -> Mission [1..*]; containment=true
Scheme.Splan -> TriggeringEvent [0..*]; containment=false
Mission.ogoal -> OGoal [1..*]; containment=false
Mission.Mplan -> TriggeringEvent [0..*]; containment=false
OPlan.FirstOgoal -> OGoal [1..1]; containment=false
OPlan.Splan -> TriggeringEvent [0..*]; containment=false
OGoal.NextOgoal -> OGoal [0..1]; containment=false
OGoal.OGoalToOPlan -> OPlan [0..1]; containment=false
OGoal.OGoalToGoal -> Goal [0..1]; containment=false
TriggeringEvent.planoperator -> OPlan [0..1]; containment=false
TriggeringEvent.triggersPlan -> Plan [1..1]; containment=false
Belief.triggeredBy -> TriggeringEvent [1..1]; containment=false
Goal.triggeredBy -> TriggeringEvent [1..*]; containment=false
Workspace.artifact -> Artifact [0..*]; containment=true
Workspace.hasSubworkspace -> Workspace [0..*]; containment=false
Artifact.port -> Port [0..*]; containment=true
Artifact.obsproperty -> ObsProperty [0..*]; containment=true
Artifact.operation -> AbsOperation [0..*]; containment=true
Port.linkArtifacts -> Artifact [0..*]; containment=false
ObsProperty.obsproperty -> Belief [0..*]; containment=false
AbsOperation.RefObsproperty -> ObsProperty [0..*]; containment=false
Operation.guardedBy -> GuardOperation [0..1]; containment=false
Operation.callsInternal -> InternalOperation [0..1]; containment=false
ExternalAction.operation -> AbsOperation [0..1]; containment=false
Plan.RefArtifact -> Artifact [0..*]; containment=false
Plan.hasContext -> Context [1..1]; containment=true
Plan.hasBody -> Body [1..1]; containment=true
Plan.hasAction -> Action [0..*]; containment=true
Body.bodyterm -> BodyTerm [0..*]; containment=true
Body.firstAction -> Action [1..1]; containment=false
Action.nextAction -> Action [0..1]; containment=false
Context.contextRule -> Rule [0..*]; containment=false
Context.contextBelief -> Belief [0..*]; containment=false
MentalNotes.impliesG -> Goal [1..1]; containment=false
MentalNotes.impliesB -> Belief [1..1]; containment=false
Message.messageToagent -> Agent [0..*]; containment=false
```

Toàn bộ 14 generalization, mỗi dòng là một quan hệ trực tiếp:

```text
LinkedOperation -> AbsOperation
InternalOperation -> AbsOperation
GuardOperation -> AbsOperation
Operation -> AbsOperation
Norm -> Organisation
Group -> Organisation
Role -> Organisation
Scheme -> Organisation
Action -> BodyTerm
ExternalAction -> Action
InternalAction -> Action
TriggeringEvent -> Action
MentalNotes -> BodyTerm
Message -> InternalAction
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

SHA-256 của target trước/sau audit: `c0aafab786c5ff3fcb468aeaf1b18b62865292e6590ffca2b9b2e962a9067fe7`.

Bằng chứng để tái chạy / kiểm tra:

- [source-inventory.json](source-inventory.json) — inventory P1/P2/P3 độc lập, không lấy từ target.
- [ecore-inventory.json](ecore-inventory.json) — canonical extraction: abstract, eSuperTypes, attribute bounds/type/default, reference bounds/type/containment/eOpposite và annotations.
- [full-audit.csv](full-audit.csv) và [full-audit.json](full-audit.json) — bảng đầy đủ có thể xử lý bằng công cụ.
- [validation.json](validation.json) — diff, hash và toàn bộ cycle ở mức kiểu.
- [emf-validation.txt](emf-validation.txt) — log EMF Diagnostician.
- [reconstruct_source.py](reconstruct_source.py), [audit_ecore.py](audit_ecore.py), [ValidateEcore.java](ValidateEcore.java) và [write_report.py](write_report.py) — mã tái lập kết quả. Chỉ `reconstruct_source.py` chứa transcription thủ công; máy không tự đọc hay tự chứng minh notation trong ảnh.

Thống kê dòng audit (có các dòng field-level để phân biệt quan sát và inference): EXACT=181, INFERRED_NOT_PROVEN=122, UNRESOLVED_FROM_SOURCE=10. Không có dòng MISMATCH/MISSING_IN_ECORE/EXTRA_IN_ECORE.
