# Task: назначение и atomic claim

Основание: исходный PRODUCT draft 0.1, разделы 11, 26.2, 36–38.


## Task

Human Task и Approval создают Task.
Исходные атрибуты: request, node_run, title, team, assignee, candidate users, candidate roles, priority, due_at, SLA state, status, form/input schema, result schema, claimed_at, completed_at.
[Состояния](../product/statuses.md) содержат отдельный enum Task.
[Agent Workspace](../product/agent-workspace.md) определяет представления очередей.

## Assignment rules

| Способ | Milestone Scope по ROADMAP |
|---|---|
| Конкретный user | M04 |
| Team queue | M01 |
| Role | M04 |
| Manager of requester | M04 |
| Owner of referenced object | Полная модель; срок не задан |
| User из expression | Полная модель; срок не задан |
| Round-robin | Полная модель; срок не задан |
| Least-loaded | Позднее |

M01 использует Team queue. Остальные способы вводятся отдельными Slice.
ManagerResolver относится к [границе корпоративного приложения](existing-app-boundary.md).
Права выбора кандидатов относятся к [permissions](permissions.md).

## Atomic claim

Одна Task MUST NOT иметь два успешных конкурентных claim.
Claim MUST выполняться транзакционно на сервере.
Исходник допускает условный update или row lock. Конкретный прием пока не выбран.
Проигравший claim возвращает conflict и актуального Assignee без потери данных.

Приемка:

1. Создать неназначенную Task в общей очереди.
2. Выполнить claim одновременно от двух исполнителей с правом.
3. Проверить ровно одного Assignee и один успешный claim.
4. Проверить conflict/current assignee у второго исполнителя.
5. Проверить ровно один успешный claim Audit Event.

## Приоритет

Server-side правило может учитывать срочность Requester, тип Service, VIP flag, масштаб влияния, SLA и workflow.
Пользовательское «Срочно» MUST NOT напрямую становиться Critical без серверного правила.
Исходник не задает полный enum приоритетов или веса факторов.

## Отсутствие и делегирование

Исходник допускает ручное переназначение менеджером.
[ROADMAP](../../ROADMAP.md) относит уточнение операций команды к M10.
Будущая модель включает out-of-office, acting manager, delegation period и substitute approver.
Ролевое описание согласующего допускает делегирование только по разрешенной политике.

> DECISION REQUIRED — D-15: fallback и полномочия назначения.
> Не заданы действия при отсутствии руководителя, пустой очереди кандидатов и изменении членства Team.
> Это влияет на доступность исполнения и сохранение прав.
> Исходник перечисляет assignment rules и ручное переназначение, но не выбирает fallback.
> До внедрения каждого правила нужно определить обработку отсутствующего адресата и допустимые переназначения.
