# Терминология

Основание: исходный PRODUCT draft 0.1, разделы 4, 7–18, 20, 30–35.


## Правила употребления

В документации используется одно название для одного понятия.
Имена полей и событий остаются такими, как в исходной модели.
MUST означает обязательное требование; MUST NOT — запрет.
SHOULD означает рекомендацию; MAY — разрешенную возможность.
PROPOSED означает предложение, которое нельзя считать принятым решением.
DECISION REQUIRED обозначает вопрос, который нужно решить до зависимой реализации.

| Термин | Определение |
|---|---|
| Service | Услуга организации с определенным результатом и правилами его получения |
| Service Draft | Редактируемая рабочая версия Service |
| Service Release | Неизменяемая опубликованная версия исполняемых правил Service |
| Request | Одно обращение пользователя за результатом Service. При создании система MUST выбрать ровно один Service Release. Ссылка MUST NOT изменяться на всем сроке жизни Request; [контракт](../architecture/service-release.md) |
| Requester | Заявитель, который создает Request и получает результат. Для M01 это ровно одна active corporate employee identity, разрешенная из authenticated Frappe User с fail-closed поведением; сохраняется только [CorporateRef](../architecture/existing-app-boundary.md#stable-reference) |
| Workflow Definition | Определение графа и правил workflow; опубликованное определение входит в Service Release |
| Expression Language | Язык выражений. MUST быть декларативным и безопасным. MUST NOT предоставлять исполнение произвольного server-side Python или другого произвольного кода; [контракт и D-09](../architecture/workflow-definition.md#expression-language) |
| Workflow Execution | Техническое исполнение Workflow Definition для Request |
| Node | Узел Workflow Definition со стабильным `node_key` |
| Node Run | Отдельный запуск Node с состоянием, входом, выходом и попыткой |
| Task | Внутренняя рабочая единица, которую создают Human Task или Approval; primary object Agent Workspace |
| Human Task | Тип Node, который создает Task для исполнителя или очереди |
| Approval | Тип Node для согласования с решением согласующего |
| Team | Команда, членство в которой участвует в назначении и проверке доступа |
| Assignee | Исполнитель, которому назначена Task |
| Coordinating responsibility | Единая ответственность за доведение Request как кейса до результата; не равна Service Owner или Task Assignee; точная модель — [D-23](requests.md#coordinating-responsibility-request) |
| Request Owner | Возможное user-представление coordinating responsibility; не обязательно одновременно с Coordinating Team |
| Coordinating Team | Возможное Team-представление coordinating responsibility; не обязательно одновременно с Request Owner |
| Public Status | Внешний статус Request, доступный Requester |
| Internal Status | Внутреннее состояние Request; не заменяет состояния Node Run и Task |
| SLA | Политика сроков обслуживания и учет ее исполнения |
| Business Calendar | Часовой пояс, рабочие дни, интервалы, праздники и исключения для учета рабочего времени |
| Public Message | Сообщение, доступное Requester |
| Request-scoped Internal Note | Внутренняя заметка в контексте Request, доступная только участникам Request с явным правом |
| Task-scoped Internal Note | Внутренняя заметка в контексте Task, доступная только участникам Task с явным правом |
| Knowledge Article | Статья Knowledge Base с публикацией, историей и правами |
| Knowledge Base | База знаний, связанная с Service, формами и Task |
| Workflow Studio | Визуальный редактор Workflow Definition |
| Workflow Runtime | Серверный исполнитель опубликованного Workflow Definition |
| Service Designer | Интерфейс настройки Service Draft и публикации Service Release |
| Agent Workspace | Интерфейс очередей и выполнения Task |
| Result Schema | Схема результата Service |
| PublicRequestView | Безопасное представление Request для API и UI Requester |
| ACL | Правила доступа к объектам, полям и каналам раскрытия данных |
| Audit Event | Неизменяемая запись события аудита |
| Action Registry | Реестр разрешенных автоматических действий |
| Data Provider Layer | Граница получения корпоративных данных через зарегистрированные providers |
| Test Run | Проверка workflow на тестовых данных без боевых Task |
| CSAT | Оценка качества Service после успешного завершения |

## Термины планирования

Product Scope → Roadmap → Milestone → Slice → ExecPlan → Implementation.

- Product Scope — границы целевого продукта в [PRODUCT](../../PRODUCT.md).
- Roadmap — порядок реализации в [ROADMAP](../../ROADMAP.md).
- Milestone Scope — состав конкретного Milestone.
- Out of Scope for Mxx — возможности вне указанного Milestone; это не исключение из Product Scope.
- Slice — малая вертикальная задача с одним проверяемым результатом.
- ExecPlan — план выполнения одного Slice.
- Implementation — реализация по ExecPlan.

## Нормализация исходных названий

- `Execution` в исходном тексте означает Workflow Execution.
- `Release` в исходном тексте означает Service Release.
- `Draft` в контексте редактирования Service означает Service Draft.
- `Service Request` и `Service Task` — предложенные имена DocType для Request и Task.
- `Article` в исходном разделе Knowledge Base означает Knowledge Article.
- `public_status` и `internal_status` — имена полей, а не дополнительные сущности.
- Public Message относится к Request; Internal Note всегда имеет request-scoped или task-scoped контекст.
- `Process Studio` в навигации исходника обозначает Workflow Studio.

Статусы и допустимые результаты перечислены в [едином справочнике состояний](statuses.md).
Он сохраняет регистр исходных списков. `Failed` из примера нормализован в `failed` для Node Run.
Новые состояния и новые роли этой редакцией не вводятся.
