# Доменная модель и хранение

Основание: исходный PRODUCT draft 0.1, разделы 7, 10–11, 17, 20, 40.


## Уровни модели

Service задает логическую идентичность.
Service Release задает идентичность исполняемых правил.
Request хранит пользовательское обращение.
Workflow Execution и Node Run хранят техническое исполнение.
Human Task и Approval создают Task.

```text
Service → Service Release ← Request → Workflow Execution → Node Run → Task
```

Схема показывает связи понятий. Она не задает все cardinality или внешние ключи.
Прямую привязку Request к Service Release определяет [Service Release](service-release.md).
Будущий restart/recovery не должен требовать новую пользовательскую Request.

## Предложенный каталог DocType

> PROPOSED
> Исходник рекомендует эти DocType. Это не утвержденные схемы и не перечень уже реализованных объектов.

| Область | Предложенные DocType |
|---|---|
| Catalog | Service; Service Category; Service Release; Service Audience Policy |
| Forms | Form Schema; Form Field Definition |
| Workflow | Workflow Definition; Workflow Revision; Workflow Node Definition; Workflow Edge Definition |
| Runtime | Service Request; Workflow Execution; Node Run; Workflow Variable / Execution Context, если отдельное хранение потребуется |
| Tasks | Service Task; Task Queue View; Approval Decision |
| SLA | SLA Policy; SLA Instance; Business Calendar; Business Calendar Exception |
| Communications | Request Message; Notification Event |
| Security | Field Access Policy; Attachment Policy |
| Knowledge | Knowledge Collection; Knowledge Article; Knowledge Revision |
| Audit | Audit Event |

Service Draft есть в продуктовой модели, но исходник не задает отдельный DocType с таким именем.
Термины Request и Task не заменяются именами предложенных DocType в продуктовом тексте.

## Атрибуты из исходной модели

Перечни ниже сохраняют исходные атрибуты. Они не определяют типы БД, индексы или обязательность каждого поля.

| Объект | Атрибуты |
|---|---|
| Service | `name`, `service_code`, `title`, `short_description`, `full_description`, `category`, `icon`, `service_owner`, `business_owner`, `support_teams`, `audience_policy`, `status`, `current_release`, `knowledge_collection`, `tags` |
| Request | `request_id`, `service`, `service_release`, `requester`, `created_at`, `public_status`, `internal_status`, `form_data`, `result_data`, `current_execution`, `closed_at`, `cancelled_at`, `source` |

Другие атрибуты имеют одно основное место:

- [Service Release](service-release.md): metadata и payload.
- [Workflow Runtime](workflow-runtime.md): Node Run.
- [Task assignment](task-assignment.md): Task.
- [Audit](audit.md): Audit Event.

[Состояния](../product/statuses.md) задают известные enum и открытые вопросы.

## JSON и нормализованное хранение

Исходник рекомендует хранить критичные фильтруемые атрибуты колонками.
Snapshots формы, workflow и Service Release допускают JSON.
Ответы формы хранятся как JSON; индексируемые значения могут выделяться для поиска и отчетов.
Система MUST NOT создавать Frappe Custom Fields под каждую Service.
Это предотвращает коллизии, рост metadata и проблемы версионирования старых Request.
Формат Workflow Definition остается открытым: [ADR-003](../adr/ADR-003-workflow-definition-format.md).

> DECISION REQUIRED — D-07: физическая модель.
> Не определены точные поля DocType, типы, связи, индексы и хранение Service Draft.
> Это влияет на целостность и миграции.
> Исходник допускает нормализованные DocType и JSON snapshots.
> До каждой модели в Slice нужно утвердить минимальную схему без выдумывания новых продуктовых сущностей.

## Хранение истории и удаление

Обычный пользователь MUST NOT физически удалять production-объекты с историей.
Исходник предлагает операции Archive, Disable и Deprecate.
Это операции жизненного цикла, а не новые значения enum для каждого объекта.

Правило особенно относится к Service Release, Request, Task, Audit Event и Knowledge Revision.
[Архивация Service](../product/service-model.md) не останавливает старые Request.
Сроки хранения и регуляторные исключения требуют решения Q09 в [обзоре продукта](../product/overview.md).
