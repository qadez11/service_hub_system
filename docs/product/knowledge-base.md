# Knowledge Base

Основание: исходный PRODUCT draft 0.1, разделы 18, 24, 41, 54.


## Назначение

Knowledge Base входит в сервисный слой.
Она поддерживает самообслуживание, инструкции исполнителям, FAQ, регламенты, внутренние процедуры и помощь в формах.
UX-ориентир — Outline: быстрый редактор, collections, дерево, поиск и читаемая типографика.

## Структура

Модель включает Workspace / Collection, Knowledge Article, иерархию, теги, Revision и permissions.
[Состояния Knowledge Article](statuses.md) отделены от состояний Service.
[Доменная модель](../architecture/domain-model.md) содержит предложенные DocType.

## Редактор первой версии

Редактор поддерживает заголовки, абзацы, списки, таблицы и callout.
Он поддерживает блоки кода, изображения, вложения, обычные и внутренние ссылки, service embeds.

## Связь с Service

Service может показывать статьи для Requester, внутренние инструкции исполнителя, FAQ и inline help поля.
Agent Workspace подбирает Knowledge Article по Service и Node.
Публикация статьи не дает всем пользователям право на ее чтение.
Поиск учитывает доступ на сервере: [контракт поиска](../architecture/integrations.md).

Milestone Scope M09 включает collections, редактор, публикацию, permissions, поиск и связь статьи с Service/Node.
Knowledge Base входит в Product Scope и остается Out of Scope for M01.
Связь с существующей Wiki остается вопросом Q13 в [обзоре продукта](overview.md).
Реализация запланирована в [M09](../milestones/M09-knowledge-base.md).
