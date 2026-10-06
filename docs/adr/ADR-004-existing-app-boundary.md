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
Принятый для M01 минимальный D-21 contract находится в
[Existing app boundary](../architecture/existing-app-boundary.md#d-21--corporate-provider-contract-decision):
corporate employee identity приходит только через адаптер, routing Team и ее
membership принадлежат Service Hub, а effective access является пересечением
corporate и Service Hub contextual permissions. Внутренние Common DocType и
API остаются разрешенными только внутри adapter implementation.

Это не утверждает готовность адаптеров `itnovel_common` и не проектирует
будущие providers. Manager, organization, document и расширенный employment
контракты отложены в основном документе решения.

## Альтернативы

Дублирование master-data отвергнуто исходником. Прямой произвольный доступ designer к server-side Python не используется вместо Action Registry.

## Связанные документы

- [Existing app boundary](../architecture/existing-app-boundary.md)
- [Integrations](../architecture/integrations.md)
