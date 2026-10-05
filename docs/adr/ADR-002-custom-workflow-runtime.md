# ADR-002 — Собственный Workflow Runtime поверх Frappe

## Статус

Accepted

Статус относится к решению в исходном PRODUCT draft 0.1, а не к готовности кода.

## Контекст

Исходные разделы 10, 20 и 52.3 требуют параллельных веток, Task, Join и длительного исполнения.
Исходник считает стандартный Frappe Workflow недостаточным для этой модели.

## Решение

Использовать собственный Workflow Runtime поверх Frappe DocType, background jobs и транзакций.
Workflow Studio остается редактором. Runtime исполняет опубликованный Workflow Definition.

## Причины

Нужно независимо хранить Request, Workflow Execution и Node Run.
Нужны ожидания, параллельность, recovery и безопасные side effects.

## Последствия

Проект отвечает за семантику исполнения, concurrency, retries и observability.
Реализация развивается от последовательного happy path к ограниченному набору бизнес-Node.
Это решение не вводит универсальный BPMN и не выбирает другую платформу.

## Альтернативы

Стандартный Frappe Workflow как основной engine отвергнут исходником.
Конкретный внешний engine в исходнике не выбран и этим ADR не добавляется.

## Связанные документы

- [Workflow Runtime](../architecture/workflow-runtime.md)
- [Workflow Definition](../architecture/workflow-definition.md)
- [Типы Node](../architecture/workflow-nodes.md)
