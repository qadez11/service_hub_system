# M07 — Security

План разработки. Он не подтверждает готовность текущего приложения.
Бюджеты — оценки объема контекста и проверки, а не сроки.

## Goal

Расширить базовую серверную защиту до полной field-level и participant модели.

## User Result

Пользователь получает только разрешенные поля, attachments и действия во всех каналах.

## Why Now

Основные каналы данных уже существуют. Теперь можно проверить единую policy matrix на реальных сценариях.

## Dependencies

[M06](M06-communications.md). Server-side enforcement и safe projections обязательны с M01.

## Scope

Field-level view/edit и другие права; participant permissions; attachment permissions; API/notification/export filtering; classification inheritance; permission debugging.

## Out of Scope

Неограниченный policy language и изменение immutable Service Release для исправления прав старой Request без отдельного решения.

## Architecture Involved

[Permissions](../architecture/permissions.md), [audit](../architecture/audit.md).

## Slices

Предварительные Slice: M07.1 field policies (M); M07.2 participants (M); M07.3 attachments (M); M07.4 projections всех каналов (M); M07.5 наследование чувствительности (M); M07.6 permission debugging и негативная матрица (M).
Каждый канал утечки проверяется отдельным наблюдаемым сценарием.

## Acceptance Criteria

Критерий salary/Finance проходит. API, Task, сообщения, notifications, exports, attachments, audit и search не раскрывают закрытые данные.

## Required Tests

Негативная permission matrix; бывший участник; смена Team; прямой API; скачивание Attachment; Restricted input/output; поиск и экспорт.

## AI Budget

XL. Нельзя объединять все каналы и policies в одну задачу.

## Exit Criteria

Матрица доступа утверждена и проверена. Нет защиты только на frontend. Диагностика объясняет решение policy.

## Known Risks

Конфликт policies или безопасное преобразование может открыть Restricted output. Snapshot policy не равен текущему членству Team.

## Decision Required

[D-16/D-17](../architecture/permissions.md): policy matrix и бывшие участники. [Q02/Q03/Q09](../product/overview.md): чувствительность, компании, хранение.

[Общий ROADMAP](../../ROADMAP.md) · [Правила ExecPlan](../../.agent/PLANS.md)
