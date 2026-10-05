# API, actions, события и поиск

Основание: исходный PRODUCT draft 0.1, разделы 19, 20.4, 21, 41, 53.


## Серверная граница API

Исходник задает REST/RPC surface без конкретных URL и signature:

| Область | Операции |
|---|---|
| Catalog | List services; get service |
| Request | Create draft request; submit request; get request |
| Communications | Add public message; answer information request |
| Tasks | List my tasks; claim task; complete task; decide approval |
| Operations | Admin retry node |
| Knowledge | Search knowledge |

Все операции подчиняются серверным [permissions](permissions.md).
Get Request для Requester возвращает PublicRequestView.
Транзакционные действия соблюдают [runtime boundaries](workflow-runtime.md).
Публичные API для внешних систем относятся к будущему roadmap.
Текущий список REST/RPC не означает анонимного доступа.

## Action Registry

Автоматические Node используют зарегистрированные actions.
Designer не получает произвольный доступ к server-side Python.
Пример исходного контракта:

```yaml
key: employee.create_equipment_assignment
name: Закрепить оборудование
input_schema: ...
output_schema: ...
permissions: ...
idempotent: true
```

Это иллюстрация, а не готовая action schema.
Секреты не включаются в Service Release.
Контракт ссылки и idempotency требуют D-08 и D-10 в [Service Release](service-release.md) и [runtime](workflow-runtime.md).
Точный набор actions первого пилота требует Q14 в [обзоре продукта](../product/overview.md).

## Domain Events

```text
request.created
request.status_changed
request.completed
request.cancelled
node.started
node.completed
node.failed
task.created
task.claimed
task.completed
approval.requested
approval.decided
message.created
sla.warning
sla.breached
service.released
```

События используются для notifications, analytics и интеграций.
Исходник не задает delivery guarantees, payload schema и версионирование событий.
До внешних подписчиков эти контракты должны быть определены в ExecPlan.
Рекомендация outbox после commit находится в [runtime](workflow-runtime.md).

## Поиск

Первая версия допускает Frappe/MariaDB full-text либо уже существующий отдельный индекс.
Индексируются Service, безопасные описания Service и опубликованные Knowledge Article.
Публикация статьи не отменяет проверку ее permissions.
Поиск Request для исполнителя строится отдельно с учетом ACL.
Система MUST NOT получать глобальные sensitive results и фильтровать их только на клиенте.
Фоновая индексация подчиняется тем же правилам раскрытия данных.

> DECISION REQUIRED — D-20: backend поиска.
> Не выбран Frappe/MariaDB full-text или существующий отдельный индекс.
> Это влияет на обновление индекса и проверку доступа.
> Оба варианта разрешены исходником.
> До поиска нужно подтвердить доступную инфраструктуру и серверную фильтрацию.

[Data Provider Layer](existing-app-boundary.md) описывает границу с корпоративными данными.
