# M04 — Approvals and Conditions

План разработки. Он не подтверждает готовность текущего приложения.
Бюджеты — оценки объема контекста и проверки, а не сроки.

## Goal

Добавить последовательное согласование и условную маршрутизацию.

## User Result

Заявитель получает результат через руководителя и условную проверку, не видя внутреннюю сложность.

## Why Now

После последовательного пути можно расширить бизнес-правила без одновременного введения Parallel.

## Dependencies

[M03](M03-workflow-studio.md), ManagerResolver и решение по expression language.

## Scope

Approval с одним согласующим; Condition; Switch; End Failure.
Разрешенные ветки approved/rejected/returned/cancelled зависят от принятой таблицы переходов.
Assignment user/role/requester manager, условия формы и выражения используют общие contracts.
Сценарий доступа добавляет Security Approval только для privileged role.

## Out of Scope

Коллективные ANY/ALL/N_OF_M переходят в M05. Произвольные циклы, email approval и делегирование по отсутствию не добавляются автоматически.

## Architecture Involved

[Node](../architecture/workflow-nodes.md), [Definition](../architecture/workflow-definition.md), [assignment](../architecture/task-assignment.md), [dynamic forms](../architecture/dynamic-forms.md).

## Slices

| Slice | Результат | Budget |
|---|---|---|
| M04.1 Expressions | Безопасное условие компилируется и вычисляется на сервере | M |
| M04.2 Condition/Switch | Request идет по разрешенной ветке с проверкой references | M |
| M04.3 Approval | Один согласующий принимает разрешенное решение; действие транзакционно | M |
| M04.4 Assignment | User/role/manager получают Task без неявного доступа к Request | M |
| M04.5 Возврат и отказ | Согласованные returned/rejected пути завершаются или продолжаются проверяемо | M |
| M04.6 Условия формы и сценарий | Видимость/required/read-only/options и доступ к системе работают сквозным путем | M |

## Acceptance Criteria

Решение принимает только уполномоченный согласующий.
Повтор решения не продвигает граф дважды.
Condition и Switch используют утвержденные expressions.
Сценарий доступа проходит без привилегированной роли и с ней.

## Required Tests

Негативные expressions; недоступные references; конкурирующие решения; все утвержденные исходы Approval; ветви Condition/Switch; regression immutable Service Release.

## AI Budget

XL. Делить по expressions, Node и assignment.

## Exit Criteria

Последовательное Approval и условная маршрутизация проверены сквозным сценарием. Неопределенные исходы не имеют скрытых defaults.

## Known Risks

Возврат на доработку может потребовать неподготовленную модель повторов. Expression может раскрыть запрещенное поле.

## Decision Required

[D-09](../architecture/workflow-definition.md): язык. [D-03](../architecture/workflow-nodes.md): контролируемый возврат. [D-15](../architecture/task-assignment.md): fallback назначения. [Q07](../product/overview.md): email approval остается отдельным решением.

[Общий ROADMAP](../../ROADMAP.md) · [Правила ExecPlan](../../.agent/PLANS.md)
