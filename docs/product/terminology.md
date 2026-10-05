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
| Request | Одно обращение пользователя за результатом Service |
| Requester | Заявитель, который создает Request и получает результат |
| Workflow Definition | Определение графа и правил workflow; опубликованное определение входит в Service Release |
| Workflow Execution | Техническое исполнение Workflow Definition для Request |
| Node | Узел Workflow Definition со стабильным `node_key` |
| Node Run | Отдельный запуск Node с состоянием, входом, выходом и попыткой |
| Task | Внутренняя задача, которую создают Human Task или Approval |
| Human Task | Тип Node, который создает Task для исполнителя или очереди |
| Approval | Тип Node для согласования с решением согласующего |
| Team | Команда, членство в которой участвует в назначении и проверке доступа |
| Assignee | Исполнитель, которому назначена Task |
| Public Status | Внешний статус Request, доступный Requester |
| Internal Status | Внутреннее состояние Request; не заменяет состояния Node Run и Task |
| SLA | Политика сроков обслуживания и учет ее исполнения |
| Business Calendar | Часовой пояс, рабочие дни, интервалы, праздники и исключения для учета рабочего времени |
| Public Message | Сообщение, доступное Requester |
| Internal Note | Внутренняя заметка, доступная только внутренним участникам с правом |
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

## Нормализация исходных названий

- `Execution` в исходном тексте означает Workflow Execution.
- `Release` в исходном тексте означает Service Release.
- `Draft` в контексте редактирования Service означает Service Draft.
- `Service Request` и `Service Task` — предложенные имена DocType для Request и Task.
- `Article` в исходном разделе Knowledge Base означает Knowledge Article.
- `public_status` и `internal_status` — имена полей, а не дополнительные сущности.
- `Public` и `Internal` — типы сообщений; Internal Note относится к внутреннему каналу.
- `Process Studio` в навигации исходника обозначает Workflow Studio.

Статусы и допустимые результаты перечислены в [едином справочнике состояний](statuses.md).
Он сохраняет регистр исходных списков. `Failed` из примера нормализован в `failed` для Node Run.
Новые состояния и новые роли этой редакцией не вводятся.
