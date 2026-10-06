# ROADMAP — порядок реализации Product Scope

Это rolling-wave plan по исходному PRODUCT draft 0.1 и заданной последовательности M00–M10.
План не объявляет возможности реализованными и не задает календарные сроки.
M00/M01 детализированы; M02/M03 имеют предметные Slice; M04/M05 описаны на среднем уровне.
M06–M10 требуют уточнения перед началом зависимой работы.

## Источники и порядок планирования

```text
Product Scope → Roadmap → Milestone → Slice → ExecPlan → Implementation
```

[PRODUCT](PRODUCT.md) задает Product Scope. Этот документ — основной источник порядка реализации.
Документы Milestone задают Milestone Scope и Out of Scope for Mxx.
Исключение из конкретного Milestone MUST NOT трактоваться как удаление функции из Product Scope.

## Последовательность

```mermaid
flowchart LR
  M00[Foundation] --> M01[Request Happy Path]
  M01 --> M02[Service Designer]
  M02 --> M03[Workflow Studio]
  M03 --> M04[Approvals / Conditions]
  M04 --> M05[Parallel]
  M05 --> M06[Communications]
  M06 --> M07[Security]
  M07 --> M08[SLA]
  M08 --> M09[Knowledge Base]
  M09 --> M10[Hardening]
```

Каждый milestone зависит от предыдущего exit gate и перечисленных в его документе решений.
M01 доказывает первый работающий путь. Готовность к пилоту проверяется по общим критериям к завершению M10 ниже.
Исходные этапы 0–6 перегруппированы в M00–M10; требования сохранены по темам.
M00 описывает модель, но не реализует business workflow.
Atomic claim перенесен в первый работающий путь, поскольку Team queue уже создает риск гонки.

## AI Budget

| Budget | Значение |
|---|---|
| XS | Локальная правка с одной простой проверкой |
| S | Небольшой Slice с одним наблюдаемым результатом |
| M | Slice с несколькими связанными слоями и предметными тестами |
| L | Существенная работа; делить на конкретные проверяемые Slice |
| XL | Работу нельзя безопасно давать AI как одну задачу. Нужно разделить ее на slices |

Budget не является оценкой часов, стоимости или числа tokens.
Дальний Budget предварителен; уточнение не разрешает менять продуктовую семантику.

## Обзор milestone

| Milestone | Цель | Пользовательский результат | Milestone Scope | Out of Scope for Mxx | Зависимости | Exit criteria | AI Budget |
|---|---|---|---|---|---|---|---|
| [M00 — Foundation](docs/milestones/M00-foundation.md) | Стабильная основа | Разработчик запускает app и проверки | Dev environment, Frappe UI, tests/lint/CI, skills, documentation, provider boundary | Business workflow | Документы и доступ к dev site | Воспроизводимый запуск; проверки и граница данных подтверждены | L |
| [M01 — Request Happy Path](docs/milestones/M01-request-happy-path.md) | Один полный путь | Requester получает результат одной Task | Service Release, Request, runtime, queue, atomic claim, safe view | Studio, Approval, Parallel, advanced SLA/ACL | M00 и минимальные contracts | E2E, concurrency, permissions и повтор jobs проверены | XL |
| [M02 — Service Designer](docs/milestones/M02-service-designer.md) | Управляемая публикация | Владелец выпускает новую форму | Service Draft, typed form, field_key, publish/versioning | Visual graph editor, миграция Request | M01 | R1 остается на v1; R2 работает на v2 | XL |
| [M03 — Workflow Studio](docs/milestones/M03-workflow-studio.md) | Визуальное проектирование | Designer собирает поддерживаемый граф | Start, Human Task, End Success, Validate, Test Run | Новые runtime Node и сложные ветки | M02; ADR-003 Accepted | Граф исполняется независимо от editor; Test Run изолирован | XL |
| [M04 — Approvals and Conditions](docs/milestones/M04-approvals-and-conditions.md) | Согласования и условия | Request идет по нужной ветке | Approval, Condition, Switch, End Failure, expressions | Parallel и коллективное Approval | M03; expression/return contracts | Сценарий доступа и разрешенные исходы проверены | XL |
| [M05 — Parallel Workflows](docs/milestones/M05-parallel-workflows.md) | Параллельное исполнение | Team выполняют одну Request совместно | Split, ALL/ANY/N_OF_M, cancel/continue, collective Approval | Loops, compensation, child requests | M04; Join/Approval decisions; D-23/D-24 | Все Join проверены; continuation однократен; Public Status один и безопасен | XL |
| [M06 — Communications](docs/milestones/M06-communications.md) | Безопасная коммуникация | Requester отвечает в своей Request | Request Information; public, request-scoped internal и task-scoped internal; notifications; draft | Мессенджеры и учет SLA времени | M05; D-25; каналы и draft binding | Ответ продолжает процесс; закрытые данные не раскрыты | L |
| [M07 — Security](docs/milestones/M07-security.md) | Расширенная защита | Доступ к полям и файлам соблюдает policy | Field ACL, participants, attachments, API/notification/export filtering | Произвольный policy language | M06; policy matrix | Негативная матрица всех каналов проходит | XL |
| [M08 — SLA](docs/milestones/M08-sla.md) | Учет сроков | Команда видит риски SLA | Calendar, Request Resolution SLA, Task due/SLA, independent pause/resume, Wait/Timer, escalation | Capacity planning | M07; D-19; D-23 для escalation recipients | Сроки и паузы воспроизводимы; internal waiting не скрывается за неявной pause; timers переживают restart | XL |
| [M09 — Knowledge Base](docs/milestones/M09-knowledge-base.md) | Контекстные знания | Пользователь находит разрешенную помощь | Collections, editor, revisions, publish, search, links | AI search, неутвержденная Wiki migration | M08; Wiki/search decisions | Статьи доступны по policy в контексте Service/Node | L |
| [M10 — Hardening](docs/milestones/M10-hardening.md) | Готовность пилота | Четыре Service проходят полную приемку | Audit, observability, recovery, actions, performance, analytics, CSAT | Будущие платформенные расширения вне M00–M10 | M09; нагрузка и pilot contracts | Общие критерии пилота подтверждены | XL |

Полные Goal, User Result, Why Now, Milestone Scope, tests, risks, decisions и Slice находятся в документах milestone.
Перед каждым сложным Slice нужен [.agent/PLANS.md](.agent/PLANS.md).

## Сквозные гарантии с первого применимого Slice

- Published Service Release MUST быть immutable. После создания Request ее связь с выбранным Service Release MUST NOT изменяться. Оба инварианта действуют с M01; M02 добавляет полноценный редактор и publish.
- Server-side permissions и safe projection действуют с M01; M07 расширяет модель.
- Atomic claim входит в M01 вместе с очередью.
- Request и Task сохраняют разные роли: Agent Workspace ориентирован на Task, Request сохраняет общий кейс.
- Coordinating responsibility входит в Product Scope, но не требует от M01 отдельных Request Owner и Coordinating Team: в одном статическом пути та же fixed Team может нести минимальную координацию. D-23 блокирует зависимую parallel-модель до M05, а не M01.
- Lifecycle audit появляется вместе с действиями; M10 расширяет эксплуатационную полноту.
- Защита повторного продвижения появляется вместе с runtime; M10 проверяет сложные failure modes и внешние actions.
- Notifications получают только безопасный контекст с M06.
- Test Run использует stub/sandbox actions; полноценные sandbox environments остаются будущей возможностью.

Полный publish checklist и ранний ограниченный профиль требуют [D-05](docs/product/service-designer.md).
Открытый вопрос блокирует зависимый Slice, а не разрешает временно нарушить инвариант.

## Покрытие Product Scope в M00–M10

| Исходная область | Где достигается |
|---|---|
| Catalog: категории, карточки, поиск, страница | Простой вход M01; категории и поиск M02 после D-20 |
| Service Designer: описание, аудитория, форма, владельцы, publish | M02 |
| Dynamic Form: основные типы, required, conditions, references, attachments | M02; expressions M04; защищенные attachments M07 |
| Workflow Studio: Start/Human Task/End | M03 поверх runtime M01 |
| Approval/Condition/End Failure | M04 |
| Parallel Split и Join ALL/ANY/N_OF_M | M05 |
| Request Information/Send Message | M06 |
| Wait и SLA | M08 |
| Action, включая ограниченные Create/Update Record и Integration Action | Набор Q14 уточняется для пилота; надежность и завершение M10 |
| Runtime: release binding, state, retries, waiting | M01 и расширения M04–M10 |
| Agent Workspace: Task queues, claim, assignee, completion, internal channels | M01; request/task-scoped internal M06; SLA представления M08 |
| Portal: submit, My Requests, status, messages, answer, result | M01 и M06 |
| Request/field/message/attachment access | База M01; каналы M06; полный профиль M07 |
| Request Resolution SLA, Task due/SLA, calendar, независимые pause, warning/breach | M08 |
| Knowledge: collections, editor, publish, permissions, search, Service/Node links | M09 |
| Audit lifecycle и admin intervention | Lifecycle с M01; полное recovery/intervention M10 |

## Сохраненные возможности вне минимального раннего пути

Эти требования не удалены и не считаются автоматически выполненными общим названием milestone.

| Возможность | Основной документ | Следующая точка уточнения |
|---|---|---|
| Черновик Request | [Состояния](docs/product/statuses.md) | D-04 перед M06 |
| Подтверждение результата и отмена | [Request](docs/product/requests.md) | D-06 до действий пилота, не позднее gate M10 |
| Shared queue views и массовое переназначение | [Agent Workspace](docs/product/agent-workspace.md), [роли](docs/product/roles.md) | M10 при уточнении операций команды |
| Полный список типов/validations формы | [Dynamic forms](docs/architecture/dynamic-forms.md) | Базовый профиль M02; остальные типы — отдельные будущие Slice |
| First response и Approval SLA | [SLA](docs/architecture/sla.md) | D-19 в M08 |
| Coordinating responsibility Request | [Request](docs/product/requests.md) | D-23 до M05; escalation recipients до M08 |
| Controlling public communicator | [Communications](docs/architecture/communications.md) | PROPOSED; D-25 до M05/M06 |
| Owner-of-reference, expression, round-robin assignment | [Assignment](docs/architecture/task-assignment.md) | Отдельные Slice после минимальных назначений; сроки не утверждены |
| Least-loaded, absence и delegation | [Assignment](docs/architecture/task-assignment.md) | Вне Milestone Scope M00–M10; ручное переназначение доступно раньше |
| Subflow и Repeat Block | [Node](docs/architecture/workflow-nodes.md) | D-03 до включения; ранний scope их не предполагает |
| Permission debugging | [Permissions](docs/architecture/permissions.md) | M07 |
| Search по Service, знаниям и отдельно Request | [Integrations](docs/architecture/integrations.md) | D-20 до реализации каждого поискового представления |
| Архивация Service и защита исторических объектов | [Service](docs/product/service-model.md), [данные](docs/architecture/domain-model.md) | Применять с появлением объекта; операционный UX до пилота |
| 15 экранов clickable prototype | [Portal](docs/product/service-portal.md) | Отдельная UX-задача; не prerequisite backend M01 |

## За пределами Milestone Scope M00–M10

Исходные исключения из ближайшего плана сохранены. Они не удаляют будущие возможности из Product Scope:

- полноценный BPMN и произвольный code node;
- сложные циклы и compensation transactions;
- process mining и AI auto-routing;
- CMDB и external customer portal;
- полноценный marketplace интеграций;
- mobile app;
- визуальный report builder;
- сложное capacity planning;
- цифровая подпись как встроенная функция.

Запрос anonymous/external requests остается [Q08](docs/product/overview.md), а не принятым расширением внутреннего продукта.

## Будущие возможности Product Scope

| Направление | Сохраненные возможности исходника |
|---|---|
| Повторное использование процессов | Визуальные reusable Subflow, child services/child request, service dependencies |
| Внешнее исполнение | External supplier tasks, webhook wait, inbound event, event-driven waits, public APIs внешних систем |
| Автоматизация | Document generation/templates, e-signature, script/code node, foreach, loop, AI action, compensation/rollback, escalation subflow |
| AI | Search по Service и Knowledge Base, form assistant, classification/routing |
| Оптимизация | Process mining, bottleneck recommendations, workload balancing |
| Платформа | Sandbox environments, Git-like diff Service Release, import/export workflow packages, marketplace Action nodes |
| Каналы | Mobile/PWA, Telegram/Teams/Slack |
| Управление портфелем | Service cost accounting, service portfolio management |
| Масштаб | Отдельные хранилища Audit/Search при обоснованной нагрузке |
| Работа с активными процессами | [Migrate Execution](docs/architecture/service-release.md) — будущая функция с неутвержденной семантикой. Она MUST NOT разрешать изменение `Request.service_release`; изменение инварианта потребует отдельного явного ADR |

Пункты не имеют календарных дат или обещанного состава выпуска.
Очередность Subflow остается открытой: [D-03](docs/architecture/workflow-nodes.md).
Эта таблица не решает противоречие вместо владельца продукта.

## Общие критерии пилота к завершению M10

Готовность к пилоту требует выполнения всех условий:

1. Владелец собирает новую поддерживаемую Service без кода.
2. Публикация создает immutable Service Release.
3. При создании Request система выбирает ровно один Service Release. Ссылка остается неизменной на всем сроке жизни Request.
4. Работают последовательные и параллельные workflow.
5. Работают Approval и Request Information.
6. Task назначаются через Team queue; claim атомарен.
7. Requester получает только безопасный public view.
8. Field-level ACL проверяется server-side.
9. SLA учитывает Business Calendar и pause.
10. Есть audit lifecycle и ручных вмешательств.
11. Есть recovery failed Node.
12. Работает Knowledge Base.
13. Четыре [эталонные Service](docs/product/requests.md) проходят end-to-end tests.

[Пилот](docs/product/overview.md) требует подтвержденных владельцев, данных, каналов и интеграционных действий.
M01 имеет собственный Milestone Scope. Общие критерии пилота не расширяют его границы.
