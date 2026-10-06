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

Параметры конкретного dev site и проверенные команды запуска фиксируются в [M00](docs/milestones/M00-foundation.md).
Это не инструкция для production deployment.

## Backend development smoke

The local development site is `development.localhost`. Run these commands inside
the existing Frappe development container, where the Bench path is
`/workspace/development/frappe-bench`:

```bash
cd /workspace/development/frappe-bench
bench --site development.localhost list-apps
# Run once only when the list does not contain service_hub_system.
bench --site development.localhost install-app service_hub_system
bench serve --port 8000
```

With `bench serve` running, use a second container shell for the backend smoke:

```bash
cd /workspace/development/frappe-bench
curl -fsS -H 'Host: development.localhost' http://127.0.0.1:8000/api/method/frappe.ping
bench --site development.localhost execute frappe.get_attr --args '["service_hub_system.__version__"]'
```

Expected output is `{"message":"pong"}` followed by `0.0.1`. The `Host` header
is required because Bench routes requests to the selected site by hostname. This
is a backend-only smoke check; frontend startup is covered by M00.3.

## Frontend development smoke

The Vue/Frappe UI frontend runs in the same development container. Its npm
dependencies are installed in `apps/service_hub_system/frontend`; the container
uses a supported Node runtime. Keep `bench serve --port 8000` running as shown
above, then start Vite in a second container shell:

```bash
cd /workspace/development/frappe-bench/apps/service_hub_system/frontend
npm run type-check
npm run dev
```

Vite serves the frontend on port `8080` at `/service-hub/`. The Frappe UI Vite
plugin proxies `/api` requests to Bench port `8000`, preserving the hostname so
that `development.localhost` remains the selected Frappe site. From a third
container shell, verify the complete development path:

```bash
curl -fsS -H 'Host: development.localhost:8080' \
  http://localhost:8080/service-hub/
curl -fsS -H 'Host: development.localhost:8080' \
  http://localhost:8080/api/v2/method/frappe.ping
```

The second command must return `{"data":"pong"}`. The existing Home page
shows the same `frappe.ping` result as **Backend smoke: Working**; it does not
read Service Hub product data. Build the production assets in the container:

```bash
cd /workspace/development/frappe-bench/apps/service_hub_system/frontend
npm run build
```

The Frappe UI plugin writes the ignored generated assets to
`service_hub_system/public/frontend/` and route entry to
`service_hub_system/www/service-hub.html`. This Docker environment does not
publish the Vite port to the host; use a forwarded port when the devcontainer
provides one, or run the container-local curl smoke above.

## Test foundation

Do not run Frappe tests against `development.localhost`: the Frappe runner
loads test records into the selected site's database. This environment uses the
separate `service-hub-tests.localhost` site and its own database. It has only
`frappe` and `service_hub_system` installed and must never use development data
as fixtures.

Create the test site once from an interactive shell in the existing Frappe
development container. The command requests the protected local MariaDB
credential; do not add that credential to source control or shell scripts.

```bash
cd /workspace/development/frappe-bench
bench new-site service-hub-tests.localhost --install-app service_hub_system
bench --site service-hub-tests.localhost set-config allow_tests true
bench --site service-hub-tests.localhost list-apps
```

The final command must list only `frappe` and `service_hub_system`. Then run
the backend smoke suite only on that named site:

```bash
cd /workspace/development/frappe-bench
bench --site service-hub-tests.localhost run-tests --app service_hub_system
```

The frontend uses Vitest with jsdom. From the same container, run:

```bash
cd /workspace/development/frappe-bench/apps/service_hub_system/frontend
npm run test
npm run type-check
```

The frontend command reports the existing router fallback smoke test. It makes
no backend request and uses no product or development data.

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
