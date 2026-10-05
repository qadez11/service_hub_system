# Граница существующего корпоративного приложения

Основание: исходный PRODUCT draft 0.1, разделы 19, 54.


## Владение данными

Существующее приложение хранит людей, документы и факты работы.
Service Hub MUST NOT создавать независимые дубликаты этих master-data.
Workflow и формы обращаются к зарегистрированным providers/actions, а не к внутренней реализации корпоративного приложения.
[ADR-004](../adr/ADR-004-existing-app-boundary.md) фиксирует эту границу.

## Data Provider Layer

Примеры контрактов исходника:

| Provider | Область |
|---|---|
| PeopleProvider | Люди |
| OrganizationProvider | Организационная структура |
| EmploymentProvider | Факты работы |
| DocumentProvider | Документы |
| ManagerResolver | Руководитель Requester |
| PermissionResolver | Проверка доступа к корпоративному объекту |

Это имена границ ответственности, а не утвержденные interfaces с готовыми методами.
Dynamic Form использует reference на существующие DocType или provider-backed entities.
Prefill использует только разрешенные данные.
Изменяющие действия проходят через [Action Registry](integrations.md).

## Что известно из репозитория

На момент анализа 2026-10-05 рядом находится app `itnovel_common`.
Его README описывает общие организационные сущности и оболочку Vue 3 / Frappe UI.
В локальном `apps.txt` перечислены frappe, service_hub_system и itnovel_common.
Это подтверждает наличие app в Bench, но не утверждает конкретный источник Team или методы providers.
Исследование текущей задачи не проверяло готовность production-интеграции.

> DECISION REQUIRED — D-21: конкретные контракты существующего app.
> Не определены source of truth пользователей/Team/оргструктуры, чувствительные объекты и точные DocType/methods.
> Это влияет на identity, references и права.
> Исходник выбирает provider boundary, но не конкретное сопоставление с itnovel_common.
> В M00 нужно изучить корпоративные контракты и записать mapping. Не объявлять совпадение имен готовой интеграцией.

Q01, Q02, Q03, Q05 и Q11 находятся в [обзоре продукта](../product/overview.md).
Версионирование внешних ссылок требует D-08 в [Service Release](service-release.md).
