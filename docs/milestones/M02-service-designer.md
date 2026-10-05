# M02 — Service Designer

План разработки. Он не подтверждает готовность текущего приложения.
Бюджеты — оценки объема контекста и проверки, а не сроки.

## Goal

Дать владельцу услуги редактируемый Service Draft, typed form и управляемую публикацию.

## User Result

Владелец меняет форму и публикует новый Service Release. Старые Request продолжают работать по прежним правилам.

## Why Now

После доказанного runtime нужно управлять продуктом без ручной подготовки каждого Service Release.

## Dependencies

[M01](M01-request-happy-path.md). Формат графа и минимальная модель уже определены.

## Scope

Service Draft; описание, аудитория и владельцы; категории и поиск каталога; базовая typed form; stable field_key; publish; версии и release notes.
Workflow пока задается существующим ограниченным способом.
Preview формы и проверка поддерживаемого профиля публикации входят в этот milestone.
Полный набор типов, expressions и Test Run развивается по зависимым milestone.

## Out of Scope

Визуальный редактор графа, новые типы runtime Node, полная ACL matrix, сложный SLA и миграция активных Request.

## Architecture Involved

[Service Release](../architecture/service-release.md), [dynamic forms](../architecture/dynamic-forms.md), [Service Designer](../product/service-designer.md).

## Slices

| Slice | Результат | Приемка | Budget |
|---|---|---|---|
| M02.1 Service Draft | Владелец сохраняет описание, аудиторию и владельцев | Изменение не меняет опубликованный Service Release | M |
| M02.2 Typed form | Владелец создает форму согласованного минимального профиля | Типы/required проверяются frontend и backend | M |
| M02.3 Идентичность полей | Смена label сохраняет field_key | Старые значения читаются после изменения новой формы | S |
| M02.4 Reference и prefill | Форма получает разрешенные корпоративные данные | Запрещенная reference не выбирается и не принимается API | M |
| M02.5 Validate/preview | Владелец видит ошибки до публикации | Неизвестные и неподдерживаемые правила блокируют publish | M |
| M02.6 Publish/version | Создается immutable Service Release с metadata и hash | current_release переключается атомарно | M |
| M02.7 Две версии | R1 использует v1, R2 использует v2 | Проходит часть критерия неизменяемости для уже поддерживаемых правил | M |
| M02.8 Каталог | Requester находит доступную Service по категории и поиску | Сервер исключает недоступные Service из результатов | M |

Условные поля зависят от решения о expressions и могут быть отдельным Slice M04.
Attachments требуют полноценной policy M07; ранняя форма не должна предлагать незащищенную загрузку.

## Acceptance Criteria

Владелец создает и меняет Service Draft.
Backend отвергает некорректные данные и неподдерживаемую конфигурацию.
Publish фиксирует поддерживаемые правила и release note.
Изменение label не ломает старые Request; удаление поля из новой версии не удаляет историю.
Нельзя изменить опубликованный Service Release через API.

## Required Tests

- Валидация типов и references на сервере.
- Неизменность field_key при смене label.
- Неизменность v1 после публикации v2.
- Конкурирующая публикация без частичного snapshot или некорректного current_release.
- Запрет публикации без права и при ошибках поддерживаемого профиля.
- E2E: Service Draft → publish → Request на новой форме.

## AI Budget

XL. Делить по форме, reference и публикации; не выполнять одной задачей.

## Exit Criteria

Владелец публикует поддерживаемую Service без правки кода. Две версии подтверждены тестами. Границы поддерживаемого профиля явны.

## Known Risks

Неопределенная schema может связать UI с неустойчивым форматом. Неявное пропускание правил нарушает смысл публикации.

## Decision Required

[D-14](../architecture/dynamic-forms.md): минимальные типы и schema.
[D-05](../product/service-designer.md): ранний checklist.
[Q15](../product/overview.md): полномочия публикации.
[D-04](../product/statuses.md): черновик Request, если он включается в этот выпуск.
[D-08](../architecture/service-release.md): версии provider references.
[D-20](../architecture/integrations.md): backend поиска Service.

[Общий ROADMAP](../../ROADMAP.md) · [Правила ExecPlan](../../.agent/PLANS.md)
