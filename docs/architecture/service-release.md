# Service Release: публикация и неизменяемость

Основание: исходный PRODUCT draft 0.1, разделы 7, 26.1, 30–32, 45, 51.


## Инвариант

Published Service Release MUST быть immutable.
Request MUST хранить прямую ссылку ровно на один Service Release.
Workflow Runtime MUST читать правила этого Service Release.
Он MUST NOT вычислять правила старой Request через `service.current_release` или Service Draft.

Изменение формы, workflow, SLA или access policy требует нового Service Release.
Service Draft не меняет уже опубликованные правила.
[ADR-001](../adr/ADR-001-service-release-immutability.md) фиксирует это решение.

## Состав снимка

Service Release фиксирует:

- форму и workflow graph;
- expression rules и assignment rules;
- SLA policies и access policies;
- Notification Template;
- mapping Public Status;
- ссылки на конфигурацию интеграций;
- Result Schema;
- metadata публикации.

Integration secrets MUST NOT попадать в snapshot.
Ссылки на конфигурацию не разрешают незаметно менять смысл опубликованного действия.
Граница ссылок требует решения D-08 ниже.

Атрибуты исходника: `service`, `version`, `published_at`, `published_by`, `content_hash`, `release_payload`, `previous_release`, `release_notes`.

## Публикация

Система выполняет проверки Service Draft, прав и ролей, графа, ссылок на поля и End-веток.
Она проверяет SLA, затем создает snapshot, вычисляет hash и присваивает номер версии.
Она переключает `current_release` для новых Request.
Критический переход публикации MUST быть транзакционным.
Полный пользовательский [checklist](../product/service-designer.md) включает Test Run и release note.
Проверки графа определены в [Workflow Definition](workflow-definition.md).

> DECISION REQUIRED — D-08: воспроизводимость ссылок.
> Не определены версии provider/action contracts и изменяемой integration configuration за ссылками snapshot.
> Это влияет на повторение старых правил при обновлении корпоративного приложения и секретов.
> Исходник фиксирует исполняемые правила, но сохраняет ссылки на интеграции без секретов.
> До реальных actions нужно определить, какие данные фиксируются и какие разрешено получать по ссылке.

## Пример payload

Упрощенный пример из исходника не является валидным публикуемым Service Release.
Пустой граф здесь показывает только форму данных.
Он не задает окончательную JSON Schema.

```json
{
  "service": {"code": "ACCESS_CRM", "title": "Получить доступ в CRM"},
  "form": {
    "fields": [
      {"key": "role", "type": "select", "required": true},
      {"key": "reason", "type": "textarea", "required": true}
    ]
  },
  "workflow": {"nodes": [], "edges": []},
  "sla": {},
  "access": {},
  "notifications": {},
  "public_status_mapping": {}
}
```

Реальный payload может храниться в нескольких таблицах.
Runtime MUST восстанавливать точные правила без чтения редактируемого Service Draft.
Различие `key` в примере и `field_key` модели требует решения в [dynamic forms](dynamic-forms.md).

## Версионирование и миграция

Новые Request используют новый Service Release после переключения `current_release`.
Старые Request продолжают исполнение по прежним правилам.
Service Release остается доступен runtime после архивации Service.
Момент фиксации Service Release для черновика Request требует решения D-04 в [состояниях](../product/statuses.md).

Миграция уже запущенных процессов по умолчанию не поддерживается.
Исходник допускает будущую операцию Migrate Execution только для администратора.
Она требует явного target release, compatibility check, mapping node state, audit и dry-run.
MVP MUST NOT автоматически переключать старую Request на новую версию.
Будущее исключение потребует отдельного решения; текущий ADR его не разрешает.

## Приемка неизменяемости

1. Опубликовать Service Release v1 и создать Request R1.
2. Опубликовать v2 с измененными формой, workflow и SLA.
3. Проверить, что R1 использует все три набора правил v1.
4. Создать R2 и проверить применение v2.
5. Проверить, что опубликованный Service Release нельзя изменить через серверный путь записи.

M01 проверяет привязку. M02 проверяет публикацию и неизменяемость поддерживаемых формы и workflow.
После M08 тот же сценарий MUST дополнительно проверить фактический расчет SLA по v1 и v2.
Ранняя проверка snapshot не означает проверку еще не реализованных SLA clocks.
