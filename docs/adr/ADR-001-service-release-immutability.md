# ADR-001 — Неизменяемость Service Release

## Статус

Accepted

Статус относится к решению в исходном PRODUCT draft 0.1, а не к готовности кода.

## Контекст

Исходные разделы 7, 26.1, 31 и 51 запрещают менять исполняемые правила старой Request при редактировании Service.

## Решение

Published Service Release MUST быть immutable.
При создании Request система MUST выбрать ровно один Service Release.
Request MUST сохранить прямую ссылку на него на весь срок своей жизни.
После создания Request значение `Request.service_release` MUST NOT изменяться.
Неизменяемость Release и неизменяемость связи Request → Service Release — отдельные инварианты.
Новый Service Release MUST применяться только к новым Request.
Редактирование Service или новая публикация MUST NOT менять правила существующей Request.
Workflow Runtime MUST исполнять правила Service Release, выбранного при создании Request.
Основной технический контракт находится в [Service Release](../architecture/service-release.md).

## Причины

Система должна воспроизводить исполнение и сохранять договоренность с Requester.

## Последствия

Изменение исполняемых правил требует новой публикации. Старые Service Release остаются доступны runtime.
Integration secrets не входят в snapshot. Контракты внешних ссылок требуют отдельного решения D-08.
Migrate Execution остается будущей функцией с неутвержденной семантикой.
Она MUST NOT считаться исключением из инварианта Request → Service Release.
Изменение этого инварианта потребует отдельного явного ADR.
До принятия такого ADR `Request.service_release` MUST оставаться неизменяемой.

## Альтернативы

Чтение текущего Service Draft или current_release для старой Request отвергнуто исходником.
Автоматическое и ручное переключение существующей Request на другой Service Release запрещено.

## Связанные документы

- [Service Release](../architecture/service-release.md)
- [Service](../product/service-model.md)
