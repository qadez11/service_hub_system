# Service Designer и Workflow Studio

Основание: исходный PRODUCT draft 0.1, разделы 7–9, 22–23, 44.


## Service Designer

Владелец услуги редактирует Service Draft через вкладки:

1. Основное.
2. Форма.
3. Процесс.
4. Исполнители.
5. Доступ.
6. SLA.
7. Коммуникации.
8. База знаний.
9. Проверка.
10. Публикация.

Навигация владельца включает каталог Service, Service Draft, Service Release, Workflow Studio, SLA, Knowledge Base и аналитику.
Публикация фиксирует правила; техническая операция описана в [Service Release](../architecture/service-release.md).

## Форма

Конструктор задает типы полей, условия, валидацию и предзаполнение.
Изменение подписи не меняет идентичность поля.
Удаление поля из новой формы не удаляет значения старых Request.
Полный контракт формы находится в [динамических формах](../architecture/dynamic-forms.md).

## Workflow Studio

Workflow Studio — редактор графа.
Экран содержит canvas, палитру Node, связи и правую панель настройки выбранной Node.
Toolbar содержит Validate, Test и Publish.
Также предусмотрены mini-map, zoom, execution preview и история изменений.

Состав доступных Node зависит от milestone.
M03 начинает со Start, Human Task и End Success.
[Каталог Node](../architecture/workflow-nodes.md) сохраняет полный исходный набор и вопросы его очередности.
Workflow Runtime работает независимо от открытого редактора.

## Preview и Test Run

Preview показывает Service в режимах Requester, исполнителя и согласующего.
Test Run использует тестовые данные и не создает боевые Task.
Интеграционные действия работают через sandbox или stub.
Test Run показывает пройденные Edge, значения expressions и ошибки.
Режим Test Run не означает наличие полноценных sandbox environments из будущего roadmap.

## Checklist публикации

Полная целевая проверка включает:

- валидную форму;
- валидный workflow и assignment каждой Task;
- завершение всех веток;
- заданный SLA;
- определенный mapping Public Status;
- заданную audience policy;
- валидную access policy;
- безопасные Notification Template;
- доступные integration actions;
- успешный Test Run.

Publish требует release note.
Технические причины отказа в публикации перечислены в [Workflow Definition](../architecture/workflow-definition.md).

> DECISION REQUIRED — D-05: публикация в ранних milestone.
> Полный checklist требует SLA, notifications и Test Run до появления этих возможностей в roadmap.
> Без решения M01/M02 нельзя считать выпуском полного Service Designer.
> В исходнике одновременно есть ранний статический happy path и полный целевой checklist публикации.
> До ранней публикации нужно утвердить ограниченный профиль поддерживаемых правил и его валидатор. Неподдерживаемые правила нельзя молча пропускать.
