# ADR-004 — Граница корпоративных master-data

## Статус

Accepted

Статус относится к решению в исходном PRODUCT draft 0.1, а не к готовности кода.

## Контекст

Исходный раздел 19 описывает существующее Frappe app с людьми, документами и фактами работы.

## Решение

Service Hub не дублирует корпоративные master-data. Формы и workflow используют Data Provider Layer и зарегистрированные actions.

## Причины

Граница сохраняет владение данными и не связывает Service Designer с внутренней реализацией корпоративного приложения.

## Последствия

Нужны явные contracts providers, references и PermissionResolver.
Конкретные DocType, источники Team и способы авторизации остаются открытыми.
Accepted относится к границе, а не к готовности адаптеров itnovel_common.

## Альтернативы

Дублирование master-data отвергнуто исходником. Прямой произвольный доступ designer к server-side Python не используется вместо Action Registry.

## Связанные документы

- [Existing app boundary](../architecture/existing-app-boundary.md)
- [Integrations](../architecture/integrations.md)
