# Audit Event

Основание: исходный PRODUCT draft 0.1, разделы 16–17, 24, 26.2, 27, 40, 51.


## Неизменяемая история

Audit Event MUST быть append-only.
Каждое privileged action и ручное вмешательство MUST создавать Audit Event.
Обычный пользователь не удаляет объекты с историей: [правила хранения](domain-model.md).
Audit payload подчиняется [permissions](permissions.md).

## События аудита

Логируются:

- создание Request и изменение доступных данных;
- переходы workflow;
- создание, назначение, claim и завершение Task;
- решения Approval;
- изменение SLA;
- сообщения;
- скачивание Restricted Attachment;
- admin intervention;
- публикация Service Release;
- изменение access policy;
- integration calls;
- retry и failure.

Основные lifecycle events нужны с появлением действия, которое они фиксируют.
M10 расширяет аудит и диагностику; он не откладывает аудит claim или публикации до конца roadmap.

## Атрибуты

Исходный перечень: timestamp, actor, action, object_type, object_id, request_id, metadata, sensitivity, correlation_id.
Исходник также допускает source_ip/session; обязательность этих данных не определена.
Точная схема и механизм append-only должны быть описаны в Slice.

Audit Event отличается от [Domain Event](integrations.md).
Domain Event служит notification, analytics и интеграциям.
Само наличие события не доказывает наличие защищенной записи аудита.

## Приемка

Проверка claim должна подтверждать ровно одно успешное событие при конкурирующих запросах.
Проверка ручного вмешательства должна подтверждать actor, действие и объект.
Негативная проверка должна исключать редактирование существующего Audit Event обычным путем.
Закрытые значения не попадают в доступный пользователю audit payload.

Сроки хранения, регуляторные требования и состав source_ip/session требуют Q09 в [обзоре продукта](../product/overview.md).
Для больших объемов отдельное хранилище допустимо позднее: [масштаб](overview.md).
