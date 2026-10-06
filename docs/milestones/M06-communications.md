# M06 — Communications

План разработки. Он не подтверждает готовность текущего приложения.
Бюджеты — оценки объема контекста и проверки, а не сроки.

## Goal

Добавить безопасное уточнение данных, сообщения и уведомления.

## User Result

Requester отвечает на вопрос в той же Request. Внутренние участники используют отдельные request-scoped и task-scoped internal каналы только в пределах ACL.

## Why Now

Runtime поддерживает ожидания и ветвление. Коммуникация теперь может продолжать реальный процесс.

## Dependencies

[M05](M05-parallel-workflows.md). Базовые permissions уже действуют; M07 расширяет их. Право открыть Request Information в parallel и необходимость controlling public communicator требуют D-25.

## Milestone Scope

Request Information; Public Message; request-scoped Internal Note; task-scoped Internal Note; Send Message; безопасный notification context; каналы пилота; сохранение черновика Request после решения D-04.
Три scope входят в Product Scope M06; они не расширяют M01 задним числом.

## Out of Scope for M06

Telegram/Teams/Slack по умолчанию, неутвержденные email approvals и attachments без access policy. Учет SLA pause/resume завершается в M08.

## Architecture Involved

[Communications](../architecture/communications.md), [permissions](../architecture/permissions.md).

## Slices

Предварительные Slice: M06.1 public/request-internal/task-internal каналы и ACL (M); M06.2 Request Information и ответ (M); M06.3 безопасные notifications (M); M06.4 черновик Request (M); M06.5 сквозное уточнение (S).
До начала milestone каждый Slice нужно развернуть в отдельный acceptance scenario.

## Acceptance Criteria

Requester получает только Public Message. Request-scoped internal не виден без явного Request participant right; task-scoped internal не открывается всем участникам Request. Ответ Requester продолжает нужное ожидание. Запрещенные поля отсутствуют в шаблонах и доставленных уведомлениях.

## Required Tests

Негативные тесты утечки и пересечения прав между тремя scope; повтор доставки; чужой ответ; продолжение после ответа; черновик после публикации новой версии.

## AI Budget

L. Оценка предварительная; выполнять отдельными Slice.

## Exit Criteria

Уточнение проходит сквозным путем. Каналы и шаблоны проверены на отсутствие закрытых данных.

## Known Risks

Сообщение или email может обойти safe projection. Политика черновика может нарушить привязку Service Release.

## Decision Required

[Q06/Q07](../product/overview.md): каналы доставки. [D-18](../architecture/communications.md): lifecycle сообщений. [D-25](../architecture/communications.md): controlling public communicator, Request Information при parallel и simultaneous waits. [D-04](../product/statuses.md): черновик. [D-03](../architecture/workflow-nodes.md): уточнение внутреннему участнику.

[Общий ROADMAP](../../ROADMAP.md) · [Правила ExecPlan](../../.agent/PLANS.md)
