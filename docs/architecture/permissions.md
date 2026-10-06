# Permissions и защита данных

Основание: исходный PRODUCT draft 0.1, разделы 3.5, 13–14, 26.6, 27.5, 34–35, 41–42, 51–52.


## Граница безопасности

Security MUST проверяться server-side с deny-by-default.
Frontend не является security boundary.
Backend MUST NOT передавать полный Request для последующего client-side masking.
Закрытые данные MUST NOT утекать через API, notifications, Task, messages, exports, attachments, audit или search.
Результаты Node и переменные workflow также подчиняются политике.

## PublicRequestView

API/UI Requester работают с отдельной safe projection.
Исходный пример состава:

```text
PublicRequestView
  id
  service
  status
  created_at
  safe_form_fields
  safe_result_fields
  public_messages
  public_timeline
  allowed_actions
```

Это пример контракта, а не окончательная response schema.
Internal Note, технические ошибки и закрытые значения не включаются автоматически.
[Коммуникации](communications.md) используют отдельный разрешенный контекст.

## Field-level policy

Каждое поле имеет classification/access policy.
Исходные права: `view`, `edit`, `use_in_expression`, `expose_to_notification`, `export`, `include_in_audit_payload`.
Примеры адресатов: requester, participants, assigned_team, specific_roles, manager, service_owner, admin.
Это адресаты policy, а не новые продуктовые роли.

> PROPOSED
> Исходник предлагает классификации Public Within Company, Internal, Confidential и Restricted.
> Он не утверждает окончательную policy matrix.

## Наследование чувствительности

Результат, построенный на Restricted input, по умолчанию имеет классификацию не ниже Restricted.
Нельзя прочитать секрет, скопировать его в output и тем самым открыть публичную передачу.
Исходник предлагает консервативное наследование Restricted до явного безопасного преобразования.
Уточнение модели входит в Milestone Scope M07.

> DECISION REQUIRED — D-16: политики и безопасное преобразование.
> Не определены окончательная матрица классификаций, конфликты policies и перечень безопасных преобразований.
> Это влияет на право чтения и снятие чувствительности.
> Исходник задает deny-by-default, отдельные права и консервативное наследование Restricted.
> До M07 нужно определить вычисление итогового доступа. До утверждения преобразования нельзя считать output безопасным.

## Участники и вложения

Просмотр Task не дает полный доступ к Request.
Доступ формируется из service policy, active task assignment, team membership, field-level policy и explicit participant role.
Назначение Request Owner или Coordinating Team, если один из этих вариантов будет принят по [D-23](../product/requests.md#coordinating-responsibility-request), не дает автоматически полный доступ к Request.
Права на public, request-scoped internal и task-scoped internal коммуникации проверяются отдельно.
После завершения Task доступ сохраняется или отзывается по политике.

Attachment имеет собственные access policy и classification.
Связь с Request не делает Attachment безопасным.
Скачивание Restricted Attachment создает [Audit Event](audit.md).

> DECISION REQUIRED — D-17: доступ после завершения Task.
> Не выбран срок сохранения прав бывшего участника.
> Это влияет на историю Request, сообщения, attachments и экспорт.
> Исходник явно допускает сохранение либо отзыв по политике.
> До participant permissions нужно определить правила конкретной Service и их проверку.

## Диагностика доступа

Для администратора предусмотрено объяснение видимости поля.
Оно показывает matched audience rule, participant role, field policy, team membership и explicit deny.
Этот режим не отменяет ограничения на чтение самого значения.

## Приемка чувствительного поля

Поле `salary` доступно только Finance.
Когда Request открывает Requester, поле отсутствует в API response и UI.
Его значение отсутствует в notification context и экспорте Requester.
Другие каналы раскрытия проверяются отдельными негативными тестами.

## Поэтапное внедрение

M01 обязан проверять доступ к Request, очереди и действиям на сервере.
M01 использует разрешенную safe projection с минимальным набором данных.
Для corporate identity и Team queue M01 effective access — это corporate
grant AND Service Hub contextual permission; любой deny/error, отсутствующий
provider или membership дает deny. Точный D-21 contract и safe identity
projection находятся в [границе существующего приложения](existing-app-boundary.md#d-21--corporate-provider-contract-decision).
M06 обязан защищать сообщения и notification context с момента их появления.
M07 расширяет field-level, participant, attachment и export policies.
M07 не является разрешением откладывать защиту уже доступных данных.
