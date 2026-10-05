# M03 — Workflow Studio

План разработки. Он не подтверждает готовность текущего приложения.
Бюджеты — оценки объема контекста и проверки, а не сроки.

## Goal

Добавить визуальный редактор существующего последовательного runtime.

## User Result

Process Designer собирает Start → Human Task → End Success, проверяет граф и публикует Service Release.

## Why Now

Runtime и публикация уже доказаны. Теперь editor может использовать устойчивый контракт.

## Dependencies

[M02](M02-service-designer.md), принятый [ADR-003](../adr/ADR-003-workflow-definition-format.md).

## Scope

Canvas, палитра, Edge и панель настроек для Start, Human Task и End Success.
Validate, Test Run, preview и публикация через существующий Service Designer.
Mini-map, zoom, execution preview и история изменений входят в целевой UX; их порядок уточняется внутри milestone.
Термин End в кратком плане означает здесь End Success. End Failure появится в M04.

## Out of Scope

Approval, Condition, Switch, Parallel, Subflow, произвольные циклы и новые правила исполнения.

## Architecture Involved

[Workflow Definition](../architecture/workflow-definition.md), [runtime](../architecture/workflow-runtime.md), [Service Designer](../product/service-designer.md).

## Slices

| Slice | Результат | Приемка | Budget |
|---|---|---|---|
| M03.1 Round-trip | Граф загружается и сохраняется без потери node_key/configuration | Семантика до и после сохранения совпадает | M |
| M03.2 Canvas | Designer соединяет три поддерживаемых типа Node | Сохраненный граф исполняется существующим runtime | M |
| M03.3 Настройки Human Task | Designer задает инструкции, вход, результат и поддерживаемое назначение | Backend проверяет ссылки и права | M |
| M03.4 Validate | Ошибки графа показаны в контексте Node/Edge | Публикация ошибочного графа запрещена | M |
| M03.5 Test Run | Тестовый путь виден без боевых Task | Использованы тестовые данные и stub actions | M |
| M03.6 Preview и публикация | Designer проверяет роль и публикует граф | Request исполняет опубликованный граф после закрытия редактора | M |
| M03.7 Навигация и revisions | Большой canvas читаем; изменения доступны в истории | Zoom/mini-map/preview не меняют семантику графа | S |

Каждый Slice использует единый утвержденный формат определения.
M03.7 не подразумевает Git-like diff Service Release из будущего roadmap.

## Acceptance Criteria

Editor сохраняет node_key и конфигурацию.
Validate запрещает dangling edge, отсутствие достижимого End и неподдерживаемые Node.
Test Run не создает боевые Task и внешние side effects.
Опубликованный граф исполняется после закрытия редактора.
Предыдущие Request сохраняют прежний Service Release.

## Required Tests

Round-trip graph; backend validation; Test Run isolation; E2E публикации и исполнения; regression M01/M02.
Проверка UI должна охватить соединение Node и исправление ошибки validation.

## AI Budget

XL. Canvas, validation и Test Run требуют отдельных Slice.

## Exit Criteria

Designer строит поддерживаемый граф без кода; runtime не зависит от состояния editor. Test Run изолирован.

## Known Risks

Editor может случайно стать источником runtime state. Test Run может запустить реальные actions.

## Decision Required

[D-22](../adr/ADR-003-workflow-definition-format.md): формат должен быть принят.
[D-03](../architecture/workflow-nodes.md): политика циклов и неподдерживаемых Node.
Точный механизм Test Run isolation и хранения revisions отсутствует в исходнике; его нужно описать до M03.5/M03.7.

[Общий ROADMAP](../../ROADMAP.md) · [Правила ExecPlan](../../.agent/PLANS.md)
