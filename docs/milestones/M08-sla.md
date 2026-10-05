# M08 — SLA

План разработки. Он не подтверждает готовность текущего приложения.
Бюджеты — оценки объема контекста и проверки, а не сроки.

## Goal

Добавить учет рабочего времени и действия при риске срока.

## User Result

Requester видит обещанный срок, команда видит риски и получает эскалации.

## Why Now

Workflow, коммуникация и permissions позволяют безопасно учитывать ожидания и сообщать о сроках.

## Dependencies

[M07](M07-security.md), решения по календарям и видам SLA.

## Milestone Scope

Business Calendar; Resolution SLA; Task due time; pause/resume; warning/breach; escalation; Wait/Timer. First response и Approval SLA — по решению D-19.

## Out of Scope for M08

Сложное capacity planning и внешние supplier workflows.
Изменение SLA MUST NOT менять опубликованный Service Release или `Request.service_release`: [контракт](../architecture/service-release.md).

## Architecture Involved

[SLA](../architecture/sla.md), [runtime](../architecture/workflow-runtime.md).

## Slices

Предварительные Slice: M08.1 календарь (M); M08.2 часы и сроки (M); M08.3 pause/resume (M); M08.4 warning/breach (M); M08.5 Wait/Timer и восстановление (M); M08.6 эскалация и сквозная закупка (M).

## Acceptance Criteria

Срок учитывает календарь. Ожидание Requester приостанавливает разрешенный SLA и ответ возобновляет его. Warning/breach не дублируют действие при повторе job.

## Required Tests

Выходные, праздники, исключения, timezone; пересекающиеся паузы по принятой модели; restart timers; неизменность правил старой Request; E2E Request Information.

## AI Budget

XL. Календарь, часы и эскалации требуют отдельных Slice.

## Exit Criteria

Полный SLA-критерий Request Information проходит. Сроки и эскалации воспроизводимы.

## Known Risks

Изменение календаря может незаметно менять обещание старой Request. Повтор timer job может дублировать эскалацию.

## Decision Required

[D-19](../architecture/sla.md): точная семантика часов, календарей и обязательные виды SLA. [D-08](../architecture/service-release.md): изменяемые ссылки.

[Общий ROADMAP](../../ROADMAP.md) · [Правила ExecPlan](../../.agent/PLANS.md)
