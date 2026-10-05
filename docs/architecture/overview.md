# Архитектура: компоненты и ограничения

Основание: исходный PRODUCT draft 0.1, разделы 19–20, 27, 51–52.


## Контекст

Backend использует Frappe Framework, DocType, jobs и транзакции.
Frontend использует Vue 3 и Frappe UI.
Существующее корпоративное приложение хранит людей, документы и факты работы.
Service Hub получает эти данные через [Data Provider Layer](existing-app-boundary.md).

Исходник допускает одно физическое Frappe app на старте.
Предложенное логическое разделение: catalog, forms, workflow_designer, workflow_runtime, tasks, sla, access, communications, knowledge, integrations, audit, analytics.
Это границы ответственности, а не требование создать одноименные Python-модули.

## Ответственность компонентов

| Компонент | Ответственность | Основной документ |
|---|---|---|
| Catalog и Service Designer | Service, Service Draft, публикация | [Service Release](service-release.md) |
| Forms | Схема, значения, validation | [Dynamic forms](dynamic-forms.md) |
| Workflow Studio | Редактирование и проверка графа | [Workflow Definition](workflow-definition.md) |
| Workflow Runtime | Исполнение, ожидания, ошибки и recovery | [Runtime](workflow-runtime.md) |
| Tasks | Назначение, claim, завершение | [Assignment](task-assignment.md) |
| Access | Серверные policies и projections | [Permissions](permissions.md) |
| Communications | Сообщения и разрешенный notification context | [Communications](communications.md) |
| SLA | Business Calendar, clocks, pause, escalation | [SLA](sla.md) |
| Knowledge | Статьи, revisions, permissions, поиск | [Knowledge Base](../product/knowledge-base.md) |
| Integrations | Providers, actions, API, события | [Integrations](integrations.md) |
| Audit | Append-only история действий | [Audit](audit.md) |
| Analytics | Агрегирование продуктовых метрик | [Метрики](../product/overview.md) |

## Надежность

Workflow state MUST NOT зависеть от браузера.
Повторная доставка job MUST NOT дублировать side effects.
Workflow Execution и таймеры MUST переживать restart worker.
[Runtime](workflow-runtime.md) определяет границы транзакций и восстановления.

## Производительность и масштаб

Числа ниже — исходные цели первой версии, которые требуют уточнения профиля нагрузки.
Они не являются результатами измерений текущего приложения.

| Операция | Цель |
|---|---|
| Каталог и My Requests | p95 < 500 ms без тяжелых интеграций |
| Agent Queue | p95 < 800 ms на типовом наборе |
| Submit Request | p95 < 1 s до постановки асинхронной работы |
| Поиск Knowledge Base | Интерактивный отклик; числовая цель не задана |

Целевая архитектура MUST поддерживать как минимум десятки тысяч пользователей.
В перспективе она должна поддерживать тысячи активных Service.
Исторические объемы: миллионы Request/Task и десятки миллионов Audit Event.
Отдельные хранилища Audit/Search допустимы позднее для больших объемов.
Это не требование вводить их в M00/M01.
Профиль нагрузки требует решения Q04 в [обзоре продукта](../product/overview.md).

## Observability

Предусмотрены correlation ID для Request/Workflow Execution, structured logs и job metrics.
Нужны dashboard failed Node, latency/error metrics интеграций и stuck execution detector.
[Внутренняя диагностика](workflow-runtime.md) не раскрывает закрытые payload.

## Риски и принятые направления

| Риск | Направление из исходника |
|---|---|
| Построение универсального BPMN вместо продукта | Ограниченный набор бизнес-Node и модель Service |
| Неограниченная гибкость permissions | Декларативные policies, deny-by-default, safe projections |
| Стандартный Frappe Workflow как основной engine | Собственный runtime поверх Frappe; [ADR-002](../adr/ADR-002-custom-workflow-runtime.md) |
| Custom Fields на каждую Service | Schema + JSON values + индексные projections |
| Перегруженный портал | Простые Service, Public Status, коммуникация и результат |

Главные инварианты и потоки собраны в [ARCHITECTURE](../../ARCHITECTURE.md).
