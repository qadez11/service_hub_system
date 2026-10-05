# Workflow Runtime

Основание: исходный PRODUCT draft 0.1, разделы 10, 16, 20.4–20.5, 26.8, 27, 43, 51.


## Разделение исполнения

Request хранит пользовательский контекст.
Workflow Execution хранит техническое состояние графа.
Это разделение позволяет позднее добавить restart/recovery без новой пользовательской Request.
Workflow Runtime MUST исполнять Request по Service Release, выбранному при ее создании.
Он использует опубликованный Workflow Definition этого Release.
После создания Request значение `Request.service_release` MUST NOT изменяться, включая retry, recovery и ручное вмешательство.
Основной контракт находится в [Service Release](service-release.md).
Workflow Studio не участвует в механизме исполнения.

## Node Run

Каждый запуск Node фиксируется отдельно.
Атрибуты исходника:

`node_key`, `attempt`, `status`, `started_at`, `finished_at`, `input_snapshot`, `output_snapshot`, `error_code`, `error_details_internal`, `actor`, `correlation_id`.

[Справочник состояний](../product/statuses.md) определяет значения Node Run.
Input/output snapshots и диагностика подчиняются [permissions](permissions.md).
Node Run не становится автоматически частью публичной истории.

## Транзакции

Следующие переходы MUST быть транзакционными:

| Переход | Связанные изменения |
|---|---|
| Завершение Task | Сохранить output → завершить Node → запланировать следующие Node |
| Claim Task | Проверить и установить владельца; [атомарность](task-assignment.md) |
| Решение Approval | Сохранить решение и выполнить разрешенное продвижение графа |
| Publish | Зафиксировать Service Release и переключить указатель для новых Request |

> PROPOSED
> Исходник рекомендует outbox/event pattern для внешних side effects после успешного commit.

Точный способ надежной постановки следующей работы должен быть описан в ExecPlan до реализации перехода.
Сам факт использования background job не доказывает атомарность или отсутствие повторного эффекта.

## Фоновая работа

Асинхронно выполняются integration nodes, notifications, пересчет SLA, timers, retries, тяжелый export и search indexing.
Состояние исполнения хранится вне браузера.
Worker restart не должен терять ожидания и таймеры.

## Идемпотентность

Каждый автоматический side effect MUST быть идемпотентным либо защищенным idempotency key.
Исходник рекомендует ключ:

```text
<request_id>:<node_key>:<attempt>:<action_key>
```

> DECISION REQUIRED — D-10: attempt и повтор внешнего эффекта.
> Не определено, меняется ли attempt при retry доставки или только при новом логическом запуске.
> Изменение ключа после выполненного внешнего действия может повторить эффект.
> Исходник требует отсутствие дублей и предлагает ключ с attempt, но не задает эту границу.
> До реальных integration actions нужно определить identity эффекта и поведение при потере ответа.

## Ошибки

Error Policy автоматической Node предусматривает:

- retry заданное число раз;
- retry with backoff;
- fail workflow;
- переход в error branch;
- ожидание admin intervention.

После исчерпания retry integration action Node Run получает `failed`.
Requester не видит stack trace и секреты.
Внутренний пользователь с правом видит диагностический код.
Public Status определяется опубликованным mapping: [состояния](../product/statuses.md).

## Ручное вмешательство

Администратор или менеджер с правом может переназначить Task, повторить failed Node или пропустить Node.
Он может выбрать error branch, отменить ожидание, вручную завершить или отменить Request.
Он может добавить Internal Note о вмешательстве.
Каждое вмешательство MUST создавать [Audit Event](audit.md).
Исходник допускает обязательную причину для особо опасных действий.

> DECISION REQUIRED — D-11: recovery и вмешательство.
> Не определены допустимые исходные состояния, последствия skip/retry/manual completion и действия с внешними эффектами.
> Это влияет на целостность workflow и аудит.
> Исходник перечисляет действия, но не задает таблицу переходов или перечень действий с обязательной причиной.
> До каждой операции нужно утвердить права, переходы, защиту от повторов и правило причины.

## Диагностика

Internal trace view показывает граф с пройденными, активными, ожидающими и failed Node.
Он содержит timestamps, результаты expressions, retry history и безопасный preview входов/выходов.
Он связан с Request, но доступен только внутренним пользователям с правом.
[Observability](overview.md) дополняет trace метриками и stuck execution detector.

## Минимальная проверка надежности

Повторная доставка job не повторяет бизнес-эффект.
Повторное завершение Task не создает второй следующий Node Run.
Перезапуск worker сохраняет возможность продолжить Workflow Execution.
Детальный протокол восстановления остается частью решений конкретного Slice.
