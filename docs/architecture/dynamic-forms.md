# Динамические формы

Основание: исходный PRODUCT draft 0.1, разделы 8, 20.3, 24, 45, 52.4.


## Модель

Форма состоит из schema и значений Request.
Каждое поле имеет стабильный `field_key`.
Изменение label MUST NOT менять `field_key`.
Удаление поля из новой версии MUST NOT удалять значения старых Request.
Форма фиксируется в Service Release.
[Доменная модель](domain-model.md) определяет подход к хранению без Custom Fields на каждую Service.

## Типы из исходного полного набора

| Группа | Типы |
|---|---|
| Текст | text, textarea, rich text |
| Числа | number, money |
| Время | date, datetime |
| Выбор | boolean, select, multi-select |
| Корпоративные ссылки | user, team, organization unit, employee, document reference |
| Файлы | file, image |
| Структуры | table/repeater |
| Адреса | URL, email, phone |
| Системные значения | hidden/system value |

Employee, document reference и справочники используют существующее корпоративное приложение через [providers](existing-app-boundary.md).
MVP требует основные типы, required, conditions, references и attachments.
Исходник не задает точный минимальный перечень типов для M02.

## Условия

Пример: `request.device_type == "Laptop"`.
Условие управляет видимостью, обязательностью, read-only и доступными options.
Условная видимость UI не заменяет ACL.
[Серверные permissions](permissions.md) защищают значения независимо от формы.

## Валидация

Исходник требует required, min/max, regexp, custom expression, существование reference и cross-field validation.
Backend MUST проверять правила, влияющие на допустимость данных.
Frontend может давать предварительную обратную связь.
Expression language требует решения D-09 в [Workflow Definition](workflow-definition.md).

## Предзаполнение

Источники: текущий пользователь, сотрудник, подразделение, руководитель, локация и должность.
Также используются активные факты работы и связанные документы.
Provider-backed reference не копирует корпоративные master-data в новую независимую модель.

> DECISION REQUIRED — D-14: контракт schema и базовые типы.
> Не определены точная JSON Schema, минимальные типы M02 и связь `key` из примера payload с `field_key` модели.
> Это влияет на старые данные, expressions и validation.
> Исходник дает полный список типов и упрощенный пример сериализации.
> До M02 нужно утвердить минимальный профиль, сериализацию идентификатора и правила расширения.
