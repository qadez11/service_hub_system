# M09 — Knowledge Base

План разработки. Он не подтверждает готовность текущего приложения.
Бюджеты — оценки объема контекста и проверки, а не сроки.

## Goal

Встроить базу знаний в каталог, формы и Agent Workspace.

## User Result

Requester находит помощь, исполнитель видит инструкции для своей Service и Node.

## Why Now

Граница permissions и поиск уже имеют контракты. Статьи можно безопасно связать с рабочими сценариями.

## Dependencies

[M08](M08-sla.md), решения о Wiki и backend поиска.

## Scope

Collections, иерархия, Knowledge Article, редактор, revisions, публикация, permissions, поиск, связи Service/Node, FAQ и inline help.

## Out of Scope

AI search, AI assistant и неутвержденная миграция всей корпоративной Wiki.

## Architecture Involved

[Knowledge Base](../product/knowledge-base.md), [поиск](../architecture/integrations.md), [permissions](../architecture/permissions.md).

## Slices

Предварительные Slice: M09.1 collections и статьи (M); M09.2 редактор (M); M09.3 publication/revisions/permissions (M); M09.4 поиск (M); M09.5 контекст Service/Node/формы (M).

## Acceptance Criteria

Опубликованная доступная статья находится поиском. Внутренняя инструкция не раскрывается Requester. Редактор поддерживает исходный набор блоков.

## Required Tests

Права на draft/published/archived статьи; дерево и revisions; индексация; безопасные attachments; contextual links.

## AI Budget

L. Уточнить после выбора редактора и связи с Wiki.

## Exit Criteria

Knowledge Base работает в реальном сценарии Service. Поиск соблюдает permissions.

## Known Risks

Публикация статьи может ошибочно считаться публичным доступом. Миграция Wiki может существенно увеличить scope.

## Decision Required

[Q13](../product/overview.md): существующая Wiki. [D-20](../architecture/integrations.md): поиск. Точный editor и revision contract исходником не выбраны.

[Общий ROADMAP](../../ROADMAP.md) · [Правила ExecPlan](../../.agent/PLANS.md)
