# Коммуникации и уведомления

Основание: исходный PRODUCT draft 0.1, разделы 9, 13, 21, 26.7;
контролируемо принятое разделение communication scopes из коллегиального draft 0.4.


## Каналы сообщений

**ACCEPT_FOR_PRODUCT_SCOPE.** Коммуникации разделены на три scope:

- `public` на Request — виден Requester и внутренним участникам с правом;
- `request-internal` — внутренний кросс-командный контекст Request только для participants с явным правом;
- `task-internal` — внутренняя работа конкретной Task для ее разрешенных участников.

Участие в Task не дает автоматически право на `request-internal`, а участие в Request не открывает все `task-internal` каналы.
Поле и Attachment ACL применяются к содержимому независимо от scope.
UI MUST требовать явное действие для изменения типа сообщения.
Серверная policy проверяется независимо от выбора в UI.
Все три scope входят в Product Scope, но не обязаны появиться в M01; их основной Milestone Scope — M06.

## Контроль public communication

> PROPOSED — controlling public communicator.
> Для parallel Request может быть полезно в каждый момент определять одного actor или Task, уполномоченных вести public communication.
> Это не является принятым глобальным инвариантом и не ограничивает права до решения D-25.

> DECISION REQUIRED — D-25: кто управляет public communication и Request Information.
> Нужно сравнить единого communicator, нескольких уполномоченных actors с координацией и правило Service Release.
> Решение должно определить fallback, право открыть Request Information, одновременные waits, audit и поведение при reassignment.
> Required before: M05/M06.

## Уведомления

Начальные каналы исходника: in-app и email.
Telegram, Teams и Slack предусмотрены позднее.
Обязательный набор пилота требует Q06 в [обзоре продукта](../product/overview.md).

Триггеры:

- создана Request;
- назначена Task;
- приближается срок SLA;
- запрошено уточнение;
- получен ответ;
- требуется Approval;
- завершена Request.

Notification Template MUST получать только разрешенный projection context.
Он не получает автоматический доступ ко всем полям Request.
Пример:

```text
notification.public.request_title
notification.public.status
notification.public.safe_fields
```

Знание ключа секретного поля автором шаблона не дает права включить значение в email.
Шаблоны фиксируются в [Service Release](service-release.md).
Фоновая доставка и повторы подчиняются [runtime](workflow-runtime.md).

## Request Information

Node может задать вопрос, открыть дополнительные поля или запросить Attachment.
Она переводит Public Status в «Ожидаем вас».
Ожидание может приостановить SLA по опубликованной политике.

Полный критерий приемки:

1. Исполнитель активной Task запрашивает уточнение.
2. Request получает «Ожидаем вас»; Requester получает уведомление.
3. Resolution SLA ставится на паузу, если политика это разрешает.
4. Requester отвечает.
5. Приостановленный SLA возобновляется; workflow продолжает исполнение.

M06 проверяет коммуникацию и продолжение workflow.
M08 добавляет проверку учета рабочего времени, паузы и возобновления.
[Permissions](permissions.md) определяют допустимые поля и attachments.
При parallel право открыть Request Information и поведение нескольких одновременных waits требуют D-25; до решения нельзя молча связывать это право с proposed communicator.

> DECISION REQUIRED — D-18: изменяемость сообщений.
> Не определены правила редактирования, удаления и смены типа уже опубликованного сообщения.
> Это влияет на ранее отправленные уведомления и историю раскрытия данных.
> Исходник требует явного действия в UI, но не задает полный lifecycle сообщения.
> До таких операций нужно определить серверные разрешения и аудит; не предполагать их наличие по одному UI-переключателю.
