# ADR-003 — Формат Workflow Definition

## Статус

Proposed

Статус относится к решению в исходном PRODUCT draft 0.1, а не к готовности кода.

## Контекст

Исходные разделы 9.2, 20.2–20.3 и 45 допускают JSON graph и нормализованные Workflow DocType.
Пример payload не содержит полной схемы Node и Edge.

## Решение

> DECISION REQUIRED — D-22: формат определения.
> Не выбран формат хранения и сериализации Workflow Definition.
> Это влияет на editor, validation, публикацию и runtime.
> Исходные варианты: нормализованные Workflow DocType или JSON snapshot графа внутри Service Release.
> До M01 нужно выбрать минимальный исполняемый формат; до M03 — подтвердить round-trip редактора.

Независимо от выбора сохраняются node_key, mappings, Error Policy и независимость опубликованного определения от Service Draft.

## Причины

Нельзя превратить допустимый вариант исходника в молча принятое архитектурное решение.

## Последствия

Точную JSON Schema и набор полей нельзя считать утвержденными.
Решение должно объяснить валидацию, идентичность Node, совместимость и восстановление опубликованных правил.

## Альтернативы

- Нормализованные Workflow Definition, Workflow Revision, Workflow Node Definition и Workflow Edge Definition.
- JSON snapshot всего графа при редактировании вне стандартной Frappe Form.

Смешанная модель потребует отдельного явного обоснования; исходник не задает ее контракт.

## Связанные документы

- [Workflow Definition](../architecture/workflow-definition.md)
- [Доменная модель](../architecture/domain-model.md)
- [Service Release](../architecture/service-release.md)
