# M05 — Parallel Workflows

План разработки. Он не подтверждает готовность текущего приложения.
Бюджеты — оценки объема контекста и проверки, а не сроки.

## Goal

Добавить Parallel Split и независимые семантики Join ALL, ANY и N_OF_M.

## User Result

Несколько Team выполняют части одной Request; Requester получает единый результат.

## Why Now

Последовательные переходы и Approval уже работают. Теперь можно проверять concurrency нескольких веток.

## Dependencies

[M04](M04-approvals-and-conditions.md), решения по Join, коллективному Approval и mapping Public Status.

## Milestone Scope

Parallel Split; Join ALL/ANY/N_OF_M; политики cancel/continue; коллективное Approval; однократное продвижение Join; безопасный публичный результат.

## Out of Scope for M05

Произвольные loops, compensation, child requests и полноценный Subflow.

## Architecture Involved

[Node и критерии Join](../architecture/workflow-nodes.md), [runtime](../architecture/workflow-runtime.md), [статусы](../product/statuses.md).

## Slices

| Slice | Результат | Budget |
|---|---|---|
| M05.1 Split | Одна Request запускает несколько сохраняемых веток | M |
| M05.2 ALL | Продолжение только после всех требуемых веток, ровно один раз | M |
| M05.3 ANY | Первая успешная ветка запускает продолжение с cancel remaining | M |
| M05.4 N_OF_M | Порог N из M проверяется при конкурирующих завершениях | M |
| M05.5 Continue | Поздние ветки следуют утвержденной policy и не ломают итог | M |
| M05.6 Коллективное Approval | Режимы решений следуют отдельной утвержденной матрице | M |
| M05.7 Onboarding | Разные Team выполняют один сквозной сценарий | M |

## Acceptance Criteria

Все критерии ALL/ANY/N_OF_M из каталога Node выполнены. Join продолжается один раз. Оставшиеся ветки соблюдают policy. Статус Requester не зависит от гонки обновлений.

## Required Tests

Одновременное завершение веток; повторная job; поздний output после cancel; failure/cancel исходы; restart worker; коллективные решения; onboarding E2E.

## AI Budget

XL. Каждый режим Join и коллективное Approval — отдельная работа.

## Exit Criteria

Три режима имеют отдельные тесты и согласованную семантику ошибок. Сквозной onboarding завершает одну Request.

## Known Risks

Поздний side effect может прийти после публичного результата. Join и Approval имеют разные правила успеха.

## Decision Required

[D-12/D-13](../architecture/workflow-nodes.md): исходы Join и Approval. [D-02](../product/statuses.md): Public Status при параллельности. Третья policy «wait but do not block public result» требует отдельного решения о сроке реализации.

[Общий ROADMAP](../../ROADMAP.md) · [Правила ExecPlan](../../.agent/PLANS.md)
