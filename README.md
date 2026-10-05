# Service Hub System

«Единое окно» — внутренняя платформа услуг на Frappe Framework и Frappe UI.
Целевая продуктовая модель и порядок разработки описаны отдельно от текущего scaffold приложения.

## Документация

- [PRODUCT](PRODUCT.md): что строим и для кого.
- [ARCHITECTURE](ARCHITECTURE.md): компоненты и архитектурные границы.
- [ROADMAP](ROADMAP.md): порядок M00–M10 и общие критерии пилота.
- [AGENTS](AGENTS.md): инструкция для Codex.
- [ExecPlan](.agent/PLANS.md): подготовка одного Slice.

## Установка

Исходная инструкция использует [bench CLI](https://github.com/frappe/bench):

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch main
bench install-app service_hub_system
```

Параметры конкретного dev site и проверенные команды запуска нужно уточнить в [M00](docs/milestones/M00-foundation.md).
Эта документационная редакция не выполняла установку или миграции.

## Участие в разработке

Репозиторий использует pre-commit для форматирования и lint.
Для подключения hooks установи [pre-commit](https://pre-commit.com/#installation) и выполни:

```bash
cd apps/service_hub_system
pre-commit install
```

Конфигурация включает ruff, eslint и prettier.
Порядок проверки тестов и CI входит в M00.

## Лицензия

Apache-2.0. См. [license.txt](license.txt).
