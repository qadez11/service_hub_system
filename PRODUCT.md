# PRODUCT — «Единое окно»

Статус: продуктовая модель на основе исходного draft 0.1.
Документ задает целевой продукт. Он не описывает готовность текущего кода.
Рабочее название — «Единое окно».
Технологическая база — Frappe Framework и Frappe UI.

## Как читать документацию

```text
PRODUCT → ARCHITECTURE → ROADMAP → MILESTONE → SLICE → EXEC PLAN → IMPLEMENTATION
```

| Читатель | Начальный маршрут |
|---|---|
| Новый участник | Этот документ → [обзор продукта](docs/product/overview.md) → [терминология](docs/product/terminology.md) |
| Владелец продукта | Этот документ → [поведение Request](docs/product/requests.md) → [ROADMAP](ROADMAP.md) |
| Архитектор | [ARCHITECTURE](ARCHITECTURE.md) → тематические документы → ADR |
| Разработчик | [README](README.md) → [AGENTS](AGENTS.md) → текущий milestone и Slice |
| Codex | [AGENTS](AGENTS.md) → источники Slice → [.agent/PLANS.md](.agent/PLANS.md) |

Детальное правило имеет одно основное место.
Master-документы дают контекст и ссылки.
PROPOSED не означает принятое решение.
DECISION REQUIRED запрещает молча выбирать продуктовую семантику при реализации.

## Что мы строим

«Единое окно» — внутренняя корпоративная платформа получения услуг.
Она объединяет service catalog, request management, workflow execution, task management, approvals и Knowledge Base.
Сотрудник выбирает нужный результат, а система организует внутреннее исполнение.

Для Requester путь выглядит так:

```text
Service → одна Request → понятный Public Status → коммуникация → результат
```

Внутри Request могут работать несколько Team, исполнителей, согласующих и интеграций.
Эта сложность не превращается в несколько независимых пользовательских обращений.

Service — центральная сущность продукта.
Она связывает вход пользователя, правила исполнения и измеримый результат.
Workflow Runtime является частью продукта услуг.

## Проблема

Корпоративные услуги распределены между почтой, чатами, таблицами, формами, ITSM, 1С и Wiki.
Сотрудник не знает, куда обращаться и кто отвечает за результат.
Одна потребность превращается в несколько несвязанных обращений.
Правила и решения остаются в переписке или памяти исполнителей.

Изменения процессов могут нарушать старые обращения.
Согласования и сроки трудно проверить.
Чувствительные данные могут попасть не тем участникам.
Историю результата трудно восстановить.

Продукт задает единый вход, явные правила, контролируемое исполнение и проверяемую историю.
Он использует существующие корпоративные данные через согласованную границу интеграции.

## Для кого

| Участник | Основной результат |
|---|---|
| Requester | Найти Service, подать Request и получить результат |
| Исполнитель | Найти Task, взять ее в работу и выполнить |
| Согласующий | Принять разрешенное решение на основе доступных данных |
| Менеджер команды | Управлять очередью, загрузкой и рисками сроков |
| Владелец услуги | Настроить Service и отвечать за ее качество |
| Process Designer | Поддерживать workflow |
| Администратор платформы | Управлять платформой и разрешенным аварийным вмешательством |

Полномочия перечислены в [ролях](docs/product/roles.md).
Process Designer не получает автоматический доступ к содержимому реальных Request.
Наличие Task также не дает полного доступа к Request.

## Потребности пользователя

Примеры из исходной модели:

- получить доступ к внутренней системе;
- подготовить рабочее место;
- заказать справку или документ;
- оформить закупку;
- согласовать договор;
- сообщить о технической проблеме;
- изменить данные;
- получить консультацию;
- пройти внутреннюю процедуру;
- запустить межфункциональный процесс.

Эти примеры описывают область продукта.
Они не требуют реализации всех Service в первом milestone.
[Пилот](docs/product/overview.md) выбирает небольшой проверяемый набор.

## Основные сущности

| Сущность | Смысл | Подробности |
|---|---|---|
| Service | Результат организации и правила его получения | [Модель Service](docs/product/service-model.md) |
| Service Draft | Редактируемая рабочая версия Service | [Service Designer](docs/product/service-designer.md) |
| Service Release | Неизменяемые опубликованные правила Service | [Service Release](docs/architecture/service-release.md) |
| Request | Одно обращение Requester | [Request](docs/product/requests.md) |
| Workflow Definition | Определение графа и правил исполнения | [Workflow Definition](docs/architecture/workflow-definition.md) |
| Workflow Execution | Техническое исполнение графа для Request | [Workflow Runtime](docs/architecture/workflow-runtime.md) |
| Node Run | Отдельный запуск Node | [Workflow Runtime](docs/architecture/workflow-runtime.md) |
| Task | Внутренняя работа, созданная Human Task или Approval | [Task assignment](docs/architecture/task-assignment.md) |
| Knowledge Article | Статья с публикацией, историей и правами | [Knowledge Base](docs/product/knowledge-base.md) |

Полный словарь находится в [терминологии](docs/product/terminology.md).
Продуктовая сущность не означает автоматически отдельный утвержденный DocType.

## Принципы продукта

### Пользователь выбирает результат

Requester не обязан знать структуру организации.
Портал показывает Service и подготовку к получению результата.
Внутренние передачи работы между подразделениями остаются частью одной Request.

### Одна потребность сохраняет один контекст

Request имеет один номер, историю, Public Status, публичную переписку и результат.
Внутренние Task не становятся отдельными пользовательскими обращениями.
Оценка качества относится к полученной Service.

### Опубликованные правила стабильны

Published Service Release MUST быть immutable.
Новая Request MUST ссылаться на конкретный Service Release.
Редактирование Service не меняет правила уже запущенной Request.
Точный контракт находится в [Service Release](docs/architecture/service-release.md).

### Внутреннее исполнение скрыто

Public Status не равен состоянию workflow.
Requester получает понятный статус и безопасную историю.
Node Run, технические ошибки, внутренние Task и Internal Note не раскрываются автоматически.
[Состояния](docs/product/statuses.md) определяют внешний набор и открытые вопросы mapping.

### Доступ проверяет сервер

Скрытие поля во frontend не является защитой.
Закрытые данные не должны утекать через API, notifications, Task, сообщения, exports, attachments, audit и search.
[Permissions](docs/architecture/permissions.md) — основной источник этих правил.

### Редактор отделен от исполнителя

Workflow Studio редактирует Workflow Definition.
Workflow Runtime исполняет опубликованное определение независимо от браузера.
Техническая модель находится в [ARCHITECTURE](ARCHITECTURE.md).

### Работа имеет одного владельца claim

Две одновременные попытки claim не должны дать двух успешных владельцев одной Task.
[Atomic claim](docs/architecture/task-assignment.md) определяет гарантию и приемку.

### Параллельность сохраняет смысл

ALL, ANY и N_OF_M — разные режимы.
Политика оставшихся веток задается явно.
[Каталог Node](docs/architecture/workflow-nodes.md) содержит правила и нерешенные случаи.

## Модули и ожидаемый опыт

### Service Portal

Requester находит Service по своей формулировке потребности.
Карточка объясняет результат и ожидаемый срок.
Страница Service показывает подготовку, доступность, FAQ и связанные знания.
Она не раскрывает внутренний workflow.

[Service Portal](docs/product/service-portal.md) описывает страницы, поиск и обзорный clickable prototype.

### My Requests

Requester видит свои Request, статус, сообщения и результат.
Он отвечает на уточнения в том же пользовательском контексте.
Отмена зависит от политики.
Подтверждение результата требует уточнения lifecycle перед реализацией.

[Request](docs/product/requests.md) содержит действия и эталонные сценарии.

### Agent Workspace

Исполнитель работает с очередями Task.
Он видит разрешенные данные и доступные действия.
Менеджер управляет назначениями и загрузкой.
Внутренняя диагностика отделена от страницы Requester.

[Agent Workspace](docs/product/agent-workspace.md) описывает рабочее место.

### Service Designer

Владелец услуги настраивает Service Draft.
Он задает форму, аудиторию, исполнителей, SLA, доступ, коммуникации и знания.
Публикация фиксирует проверенные правила в Service Release.

[Service Designer](docs/product/service-designer.md) содержит вкладки, preview, Test Run и checklist.

### Workflow Studio

Process Designer строит граф из поддерживаемых Node.
Он проверяет маршрут и тестирует его без боевых Task.
Состав Node растет по milestone.
Первая версия редактора работает с уже существующим последовательным runtime.

[Workflow Definition](docs/architecture/workflow-definition.md) задает техническую границу графа.

### Knowledge Base

Знания помогают Requester до обращения и исполнителю во время Task.
Статьи связаны с Service, формой и Node.
Внутренние инструкции сохраняют собственные права.

[Knowledge Base](docs/product/knowledge-base.md) содержит структуру и возможности редактора.

### Operations & Analytics

Владелец оценивает качество Service, сроки и узкие места.
Менеджер оценивает очередь и загрузку.
Администратор оценивает failures, интеграционные ошибки и работу платформы.

[Метрики](docs/product/overview.md) сохраняют исходный перечень.
[Workflow Runtime](docs/architecture/workflow-runtime.md) описывает диагностику и вмешательство.

### Administration

Администратор управляет командами, справочниками, policies и интеграциями.
Привилегированные действия требуют полномочий и аудита.
Доступ к платформенным настройкам не заменяет явный контракт доступа к данным.

[Permissions](docs/architecture/permissions.md) и [Audit](docs/architecture/audit.md) определяют технические правила.

## Результат и качество

Каждая Service определяет Result Schema.
Requester получает понятную карточку результата.
Примеры: предоставленный доступ, готовый документ, созданная закупка.
[Модель Service](docs/product/service-model.md) сохраняет исходные примеры данных.

Service может запросить CSAT после успешного завершения.
Оценка не меняет SLA конкретного исполнителя напрямую без отдельной модели.
[Request](docs/product/requests.md) определяет формат обратной связи.

Сроки зависят от SLA и Business Calendar.
Ожидание Requester может приостанавливать SLA по политике.
Полный контракт и открытые вопросы находятся в [SLA](docs/architecture/sla.md).

## Существующее корпоративное приложение

Платформа использует существующее Frappe app с людьми, документами и фактами работы.
Service Hub не создает независимые копии этих master-data.
Формы и workflow обращаются к providers и зарегистрированным actions.

Точное сопоставление с текущими объектами требует исследования в M00.
Наличие рядом itnovel_common само по себе не доказывает готовность интеграционного контракта.
[Граница app](docs/architecture/existing-app-boundary.md) и [ADR-004](docs/adr/ADR-004-existing-app-boundary.md) фиксируют ответственность.

## Границы первого результата и MVP

M01 доказывает один путь:

```text
Service → Service Release → Request → Workflow Execution → Human Task → результат
```

Для него не нужен visual Workflow Studio.
Одна небольшая Service должна пройти путь целиком.
M01 не включает Parallel, advanced SLA, полный ACL designer или Knowledge Base.

Полный MVP шире M01.
Он включает Service Designer, последовательные и параллельные workflow, Approval, коммуникацию, server-side ACL, SLA, аудит, recovery и Knowledge Base.
Его приемка требует четырех эталонных Service.
[ROADMAP](ROADMAP.md) — основной источник состава, исключений и Definition of Done MVP.

Будущие возможности не удаляются из модели только потому, что не входят в MVP.
Subflow, child services, AI, внешние каналы и платформенные расширения сохраняются в roadmap с явной очередностью или открытым решением.

## Нефункциональные ожидания

Процесс не зависит от открытого браузера.
Повторная доставка работы не должна дублировать бизнес-эффект.
Worker restart не должен терять ожидание или таймер.

Performance и scale оцениваются на согласованном профиле организации.
Исходные числовые ориентиры сохранены в [архитектурном обзоре](docs/architecture/overview.md).
Они пока не являются измеренными характеристиками приложения.

## Открытые решения

[Обзор продукта](docs/product/overview.md) хранит все 15 исходных вопросов Q01–Q15.
Они охватывают identity, чувствительность, компании, нагрузку, SSO, каналы, пилот, хранение, локализацию, Wiki и публикацию.

Тематические DECISION REQUIRED находятся рядом с правилом, которое они блокируют.
Основные группы:

| Группа | Источник |
|---|---|
| Статусы, черновик Request, подтверждение и отмена | [Состояния](docs/product/statuses.md), [Request](docs/product/requests.md) |
| Формат графа и expressions | [ADR-003](docs/adr/ADR-003-workflow-definition-format.md), [Definition](docs/architecture/workflow-definition.md) |
| Join, коллективное Approval, циклы и Subflow | [Node](docs/architecture/workflow-nodes.md) |
| Ранний профиль публикации и ссылки snapshot | [Designer](docs/product/service-designer.md), [Service Release](docs/architecture/service-release.md) |
| Retry, recovery, ACL и SLA | [Runtime](docs/architecture/workflow-runtime.md), [permissions](docs/architecture/permissions.md), [SLA](docs/architecture/sla.md) |

Нерешенный вопрос не разрешает агенту придумывать default, роль, статус или новый scope.
[AGENTS](AGENTS.md) задает формат STOP.

## Правила развития документации

Продуктовое поведение описывается в docs/product.
Техническая модель описывается в docs/architecture.
Важное принятое или предлагаемое решение оформляется ADR.
ROADMAP определяет порядок и границы работ.
Milestone определяет проверяемый результат и slices.
ExecPlan определяет одну конкретную работу и способ проверки.

Изменение подробного правила выполняется в его основном документе.
Ссылки и краткое изложение в master-документах обновляются вместе с ним.
Изменение продукта требует явного решения; редактура не должна скрыто менять семантику.
