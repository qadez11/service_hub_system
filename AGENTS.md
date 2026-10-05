# Инструкция для Codex

## Проект и стек

«Единое окно» — внутренние Service, Request, workflow, Task, Approval и Knowledge Base.
Стек: Frappe Framework, Vue 3 / Frappe UI и существующее корпоративное Frappe app.
Требования описывают целевой продукт; сначала проверь фактическое состояние кода.

## Что читать

1. [PRODUCT](PRODUCT.md) — смысл и границы продукта.
2. [ARCHITECTURE](ARCHITECTURE.md) — компоненты и инварианты.
3. [ROADMAP](ROADMAP.md) и текущий milestone — scope и Slice.
4. Только связанные docs/product, docs/architecture и ADR.
5. [.agent/PLANS.md](.agent/PLANS.md) — ExecPlan одной сложной задачи.

Используй [терминологию](docs/product/terminology.md). Не загружай всю документацию для каждого Slice.
Изучи README, существующие изменения и применимые frappe-skills перед работой с кодом.

## Архитектура и workflow

- Published Service Release immutable; Request привязан к конкретному Service Release.
- Runtime не читает исполняемые правила из Service Draft или current_release старой Request.
- Workflow Studio — редактор; Workflow Runtime — независимый серверный исполнитель.
- Request, Workflow Execution и Node Run имеют разные роли.
- Claim Task атомарен. Продвижение графа и автоматические side effects защищены от дублей.
- ALL, ANY и N_OF_M сохраняют отдельные правила; не выводи семантику Approval из Join без решения.
- Не создавай Frappe Custom Fields под каждую Service.
- Не дублируй корпоративные master-data; используй provider/action boundary.
- Audit append-only; привилегированные действия фиксируются.

## Security

Backend проверяет доступ с deny-by-default.
Public API возвращает safe projection, а не полную Request с frontend masking.
Проверяй API, Task, messages, notifications, exports, attachments, audit, search и производные outputs.
Integration secrets не входят в Service Release.
M07 не разрешает откладывать базовую защиту более ранних Slice.

## Scope, решения и тесты

Делай small vertical changes: один наблюдаемый результат за Slice.
Для сложной работы сначала составь ExecPlan; Budget XL сначала раздели.
Не принимай silent product decisions. PROPOSED и DECISION REQUIRED не являются утвержденным контрактом.
Изменяй правило в основном документе; не создавай конкурирующий источник истины.
Не перезаписывай чужие изменения и не расширяй scope ради соседней функции.

Проверяй acceptance scenario и значимые негативные случаи.
Для permissions нужны серверные негативные тесты; для claim и Join — concurrency tests.
Для версий нужен тест старой Request после новой публикации; для jobs — проверка повторной доставки.
Запусти проверки затронутого поведения. Сообщи ограничения среды и непроверенные условия.
Для документации проверь относительные ссылки, термины и покрытие требований.

## STOP

Останови зависимую реализацию и сообщи причину, если:

1. Нужно изменить продуктовую семантику, которой нет в PRODUCT и связанных источниках.
2. Требование противоречит существующему ADR.
3. Изменение нарушает immutable Service Release.
4. Security реализуется только во frontend.
5. Slice неожиданно требует переписать большую часть системы.
6. Scope существенно превышает milestone.
7. После нескольких попыток исправления архитектура обрастает workaround.
8. Нельзя сформулировать проверяемый acceptance criterion.

Формат сообщения:

```text
STOP

Причина:
...

Что нужно решить:
...
```

Открытый вопрос в будущем milestone не блокирует независимую документационную работу.
Не начинай зависимую реализацию до явного решения.
