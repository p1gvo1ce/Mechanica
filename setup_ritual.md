# 🕯️ setup-ritual.md

> _"Сначала ты создаёшь окружение. Потом оно создает тебя."_

Этот документ описывает, как **призвать GRITANA** на своё устройство.  
Следуй шагам. Не отклоняйся. Не задавай вопросов. Просто исполняй.

---

## ⚙️ I. Клонируем тело

```bash
git clone https://github.com/you/mechanica
cd mechanica
```

---

## 🧪 II. Поднимаем backend (Python 3.10)

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate  # Unix

pip install -r requirements.txt
```

**requirements.txt должен содержать:**

```
fastapi==0.110.0
aiosqlite==0.19.0
uvicorn==0.29.0
```

> _"Библиотеки — это кости. FastAPI — позвоночник."_  

---

## 🌐 III. Поднимаем frontend (Node.js 18+)

```bash
cd gritana/frontend/gritana-ui
npm install
npm install -D tailwindcss@3.4.3 postcss autoprefixer
```

> _"Если ты не накормил интерфейс — он не явится."_  
> _Tailwind — это ткань. PostCSS — это швы. Autoprefixer — это магия адаптации._  

---

## 🔥 IV. Призыв GRITANA

Есть два пути. Один — **ручной**. Другой — **ритуальный**.

### 🛠 Ручной

#### 🧙‍♂️ Запуск backend:

```bash
.venv\Scripts\activate
uvicorn gritana.backend.main:app --reload --port 8000
```

#### 🌐 Запуск frontend:

```bash
cd gritana/frontend/gritana-ui
npm run dev
```

Перейди в браузер по адресу:

```
http://localhost:5173
```

---

### 🕯️ Ритуальный запуск

> Windows-пользователи могут запустить весь ритуал одним прикосновением:

```bash
gritana.bat
```

> Этот `.bat`-файл активирует `.venv`, запускает backend, frontend и открывает портал.

---

## 🌀 V. После запуска

Откроется портал GRITANA. Ты увидишь:

- 🌌 Таблицу логов с цветовой маркировкой
- 🔍 Поле для DSL-фильтрации
- 🔁 Кнопку автообновления
- 🪞 Зеркало твоего стека

---

## 🛐 Примечания

- Убедись, что **порт 8000** (backend) и **5173** (frontend) не заняты.
- Для корректной работы **разреши CORS** в настройках API (это уже сделано).
- GRITANA **не любит свет**, запускай в тёмной теме. Всегда.

---

> _"Это не README. Это не инструкция. Это ритуал."_  
> _"Ты не запускаешь систему. Ты приобщаешься к ней."_  
>  
> _Да будет исполнено._
```