# Workflow Definition

Основание: исходный PRODUCT draft 0.1, разделы 9.2, 9.5–9.7, 20, 44.


## Граф

Workflow Definition задает ориентированный граф.
Модель включает Node, Edge, Node Configuration, Input Mapping, Output Mapping и Error Policy.
Каждая Node имеет стабильный `node_key`.
Опубликованное определение входит в Service Release.
Workflow Studio редактирует граф; Workflow Runtime исполняет опубликованные правила.

## Формат

Исходник допускает JSON snapshot графа или нормализованные Workflow DocType.
Окончательный формат и JSON Schema не приняты.
[ADR-003](../adr/ADR-003-workflow-definition-format.md) имеет статус Proposed.
Нельзя выдавать пример payload за утвержденный runtime protocol.

## Expressions

Исходник задает пространства имен:

```text
request.*
requester.*
service.*
release.*
context.*
node.<node_key>.output.*
actor.*
org.*
```

Expression language SHOULD быть декларативным и безопасным.
Произвольный Python/JavaScript SHOULD NOT служить основным механизмом условий.
Пример условия: `request.amount > 100000`.
ACL определяет право использования поля в expression: [permissions](permissions.md).

> DECISION REQUIRED — D-09: язык expressions.
> Не заданы grammar, типы, функции, поведение ошибок и правила доступа к namespace.
> Это влияет на валидацию формы, маршрутизацию и безопасность.
> Исходник выбирает безопасные декларативные expressions, но не конкретный язык.
> До conditions нужно утвердить контракт языка и проверяемые ошибки.

## Проверка перед публикацией

Publish запрещен, если:

- отсутствует Start или достижимый End;
- есть dangling edge;
- Node ссылается на удаленное поле;
- отсутствует assignment;
- N_OF_M некорректен;
- expression не компилируется;
- секретное поле передается в Public Message;
- integration action недоступна;
- граф содержит запрещенный цикл.

Полный checklist также требует завершения всех веток.
Эти требования дополняют проверку наличия достижимого End.
Число Start и полная семантика End при параллельности в исходнике не заданы.
До поддержки таких графов нужно конкретизировать их в ADR-003 или спецификации Node.

## Циклы

> PROPOSED
> Для первой тестируемой версии исходник рекомендует запрет произвольных циклов графа.
> Возврат на доработку предлагается реализовать контролируемым поведением Approval, Request Information или Repeat Block.

Произвольные циклы усложняют recovery, observability и защиту от бесконечного исполнения.
Repeat Block не имеет самостоятельного контракта в исходнике.
До реализации возвратов нужно решить D-03 в [каталоге Node](workflow-nodes.md).
