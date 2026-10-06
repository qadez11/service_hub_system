# Граница существующего корпоративного приложения

Основание: исходный PRODUCT draft 0.1, разделы 19, 54; [ADR-004](../adr/ADR-004-existing-app-boundary.md).

## Владение данными

Существующее корпоративное приложение владеет person и employment identity,
документами и фактами работы. Service Hub MUST NOT создавать независимые
дубликаты этих master-data. Workflow и формы обращаются к зарегистрированным
providers/actions, а не к внутренней реализации корпоративного приложения.

Service Hub владеет своими routing Team и их membership для назначения и
очередей. Team не является Department: department из corporate employment
может быть входом для будущего правила, но MUST NOT неявно становиться Team
или ее membership.

## D-21 — Corporate Provider Contract Decision

Решение ограничено M01. Это не общий provider framework и не контракт для
всех будущих корпоративных данных.

| Concern | Candidate source | Required now? | Decision | Reason |
| --- | --- | --- | --- | --- |
| Requester identity | Corporate identity через `itnovel_common` adapter | Yes | Один authenticated Frappe User разрешается ровно в одну active corporate employee identity; Service Hub сохраняет ее `CorporateRef` | Requester должен быть корпоративным сотрудником, но domain code не должен знать Common DocType |
| Team | Service Hub routing Team и Service Hub membership | Yes | Team и membership принадлежат Service Hub; M01 использует явно сконфигурированную fixed Team | В Common нет подтвержденной Team-модели; Department не равен Team |
| Corporate permission | Corporate adapter | Yes | Adapter подтверждает, что identity допустима для Service Hub; Service Hub добавляет контекстную policy | Ни один слой сам по себе не дает доступ к Request или Task |
| Person/employment details | Corporate adapter | Yes, identity only | В M01 допустима только `RequesterIdentityProjection` | Поля Common содержат чувствительные данные, не нужные happy path |
| Manager, org hierarchy, documents | Corporate providers | No | DEFERRED — Required before: M04 для ManagerResolver; перед первым использованием для остальных | Не нужны статическому Team queue M01 |

### Stable reference

`CorporateRef` — единственный корпоративный идентификатор, который может
сохранить или передать Service Hub domain:

```text
corpref:v1:<kind>:<opaque-id>
```

`kind` для M01 равен `employee`. `opaque-id` назначает provider; это
непустой URL-safe token без значения для Service Hub. Он MAY быть отображен
adapter-ом на внутренний primary key, но MUST NOT включать имя DocType,
поле, Frappe name либо персональные данные в публичном domain contract.
Service Hub сравнивает reference только на точное равенство и не разбирает
`opaque-id`. `v1` — версия формата reference, а не версия implementation.

### Minimal M01 contract

Service Hub domain вызывает только текущий зарегистрированный
`CorporateIdentityProvider` с явным actor и purpose. Его операции:

```text
resolve_requester(actor_user, purpose="request.submit")
  -> RequesterIdentityProjection | IdentityResolutionDenied

check_identity_access(actor_user, corporate_ref, purpose)
  -> CorporateAccessGranted | CorporateAccessDenied
```

`RequesterIdentityProjection` содержит ровно:

```text
corporate_ref: CorporateRef
display_name: str
```

`display_name` предназначен только для internal M01 Task/Request context и
MUST NOT сам по себе попадать в requester-facing API, notification, export,
audit payload или search. Contract не возвращает Frappe `Document`, DocType
name, `User`, person/employee ids, department, position, contact, document,
employment history либо произвольные поля.

Для текущей реализации adapter допускается читать `itnovel_common` только
внутри своего implementation boundary. Репозиторий подтверждает candidate
`resolve_employee_for_user`: он отвергает Guest и ambiguity. Adapter обязан
дополнительно убедиться, что связанные person и employee active/valid по
корпоративному правилу; status или внутренняя схема Common не являются
частью этого контракта.

`IdentityResolutionDenied` и `CorporateAccessDenied` имеют только machine
reason из закрытого enum (`anonymous`, `not_found`, `ambiguous`, `inactive`,
`invalid`, `not_authorized`, `provider_unavailable`). Они MUST NOT возвращать
CorporateRef или корпоративные поля. Обе операции fail closed: Guest,
no-match, ambiguity, inactive/invalid identity, corporate deny, missing
provider, incompatible contract version и provider failure запрещают submit,
view или claim соответственно. Нет fallback к `User`, Department, direct
DocType read или cached/stale positive result.

### Team and Task eligibility

M01 Team имеет stable Service Hub identifier, не `CorporateRef`; ее
membership хранит Service Hub как пары `(team_id, corporate_ref)`. При
создании Team membership M01 обязан разрешить active identity через provider;
при claim он обязан заново получить active actor identity.

Actor может увидеть/claim Task из Team queue, только если одновременно:

```text
corporate permission for actor/identity
AND resolved active actor CorporateRef
AND active Service Hub Team membership
AND Service Hub contextual Task policy
AND atomic Task state permits claim
```

Это определяет effective access. Любой deny, absence или error любого
conjunct дает deny; успешная проверка membership не заменяет corporate
permission, а успешная corporate check не заменяет Service Hub context.
Task visibility и claim проверяются server-side. Запрещено выводить Team из
Department или только скрывать Task во frontend.

### Adapter boundary and registration

Граница вызова строго следующая:

```text
Service Hub domain -> CorporateIdentityProvider contract
  -> itnovel_common adapter -> itnovel_common internal DocType/API
```

Внутренние Common DocType/API разрешены только правому звену. Service Hub
domain, Request, Task, Service Release и frontend MUST NOT импортировать,
сериализовать или называть их.

M01 использует один mandatory registration key
`service_hub_corporate_identity_provider`. App configuration registers exactly
one factory for contract id `corporate-identity/v1`; Service Hub resolves it
at startup/application boundary and rejects zero or multiple factories. The
factory returns a provider declaring the same contract id. This is local
app-hook registration, not a plugin marketplace. A future incompatible
contract получает новый id (например, `corporate-identity/v2`) и явную
migration/selection decision; domain code не зависит от adapter path.

### Deferred corporate contracts

| Contract / decision | Status | Required before |
| --- | --- | --- |
| ManagerResolver | DEFERRED | M04, before manager-of-requester assignment |
| Organization hierarchy and department-based routing | DEFERRED | Before first rule that uses it |
| EmploymentProvider beyond active requester eligibility | DEFERRED | Before first employment-based Service policy |
| DocumentProvider | DEFERRED | Before first document reference/action |
| Advanced search, cache and bulk reads | DEFERRED | Before the respective feature |

## Data Provider Layer beyond M01

PeopleProvider, OrganizationProvider, EmploymentProvider, DocumentProvider,
ManagerResolver and PermissionResolver remain names of responsibility
boundaries, not approved future interfaces. Dynamic Form uses a reference to
an existing object only through a later approved provider-backed entity.
Prefill uses only permitted data. Changing operations continue through the
[Action Registry](integrations.md).

## Verification obligations for the implementation slice

The later M00.6 implementation MUST prove with an isolated fake provider:

1. exactly one active identity yields only the two projection fields;
2. anonymous, absent, ambiguous, inactive and provider-failure resolution
   deny without a CorporateRef or corporate field;
3. a corporate grant without Service Hub Team membership cannot view or claim;
4. a member with corporate deny cannot view or claim.

No real Common fixture or development-site corporate data is needed for this
contract test.
