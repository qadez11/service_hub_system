# M10 — Hardening

План разработки. Он не подтверждает готовность текущего приложения.
Бюджеты — оценки объема контекста и проверки, а не сроки.

## Goal

Подготовить результаты M01–M10 к пилоту и проверить надежность всех реализованных механизмов.

## User Result

Четыре эталонные Service проходят сквозную приемку; команда умеет диагностировать и восстанавливать исполнение.

## Why Now

После появления основных функций можно проверить их взаимодействие и измерить эксплуатационные характеристики.

## Dependencies

[M09](M09-knowledge-base.md), все предшествующие exit criteria и утвержденный профиль пилота.

## Milestone Scope

Расширение audit и observability; retries; idempotency hardening; workflow debugging; manual intervention; performance; analytics; CSAT. Ограниченные actions пилота завершаются по Q14.

## Out of Scope for M10

Универсальный BPMN, marketplace, AI automation, process mining, child services и прочие будущие возможности вне Milestone Scope M00–M10.

## Architecture Involved

[Runtime](../architecture/workflow-runtime.md), [audit](../architecture/audit.md), [качество](../architecture/overview.md), [метрики](../product/overview.md), [CSAT](../product/requests.md).

## Slices

Предварительные малые Slice задают способ декомпозиции. Они не исчерпывают Scope milestone.

| Slice | Один наблюдаемый результат | Budget |
|---|---|---|
| M10.1 Trace | Внутренний пользователь находит failed Node и видит безопасную диагностику | M |
| M10.2 Retry | Одно выбранное действие переживает потерю ответа без повторного эффекта | M |
| M10.3 Вмешательство | Одна утвержденная операция recovery проходит с проверкой права и Audit Event | M |
| M10.4 Action | Одно зарегистрированное действие пилота выполняется по контракту | M |
| M10.5 Performance | Один измеренный bottleneck устранен и повторно измерен | M |
| M10.6 Метрика | Одна продуктовая метрика вычисляется на проверяемых данных | S |
| M10.7 CSAT | Requester оценивает успешно завершенную Service; владелец видит агрегат | M |
| M10.8 Пилотная Service | Одна эталонная Service проходит полный E2E | M |

До начала M10 нужно добавить отдельные Slice для остальных операций, actions, метрик и трех других Service.
Нельзя объявлять весь milestone завершенным после одного представителя каждой группы.

## Acceptance Criteria

Выполнены общие критерии пилота из [ROADMAP](../../ROADMAP.md). Повтор job не дублирует эффект. Recovery сохраняет Request и audit. Метрики измерены на согласованном профиле.

## Required Tests

Failure injection; worker restart; потеря ответа интеграции; безопасный retry; privileged actions; нагрузка; утечки в logs/audit/trace; четыре эталонных E2E.

## AI Budget

XL. Перед ExecPlan нужно уточнить и дополнить малые Slice по фактическому составу пилота.

## Exit Criteria

Все общие критерии пилота из [ROADMAP](../../ROADMAP.md) подтверждены доказательствами. Риски пилота явны. Нерешенные вопросы не скрыты под завершенным milestone.

## Known Risks

Hardening не должен превращаться в место первого появления базовых гарантий. Реальные actions могут потребовать неописанные внешние contracts.

## Decision Required

[D-10/D-11](../architecture/workflow-runtime.md): retry/recovery. [D-01](../product/overview.md): reopen metric. [Q04/Q09/Q10/Q14](../product/overview.md): нагрузка, хранение, пилот и actions. [D-06](../product/requests.md): подтверждение/отмена до включения действий в пилот.

[Общий ROADMAP](../../ROADMAP.md) · [Правила ExecPlan](../../.agent/PLANS.md)
