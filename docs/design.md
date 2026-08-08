# 設計文件：Python 網頁版猜數字遊戲

> 本文件依據 [`docs/prompt.md`](./prompt.md) 的需求整理而成，作為實作前的架構設計依據，尚未包含實際程式碼。

---

## 1. 專案目標與範圍

一個適合初學者學習、可直接放到 GitHub 展示的 Flask 網頁版猜數字遊戲。

**必須有：**
- Flask + 標準函式庫，無資料庫、無前端框架
- 電腦隨機出題（1–100）、玩家猜測、太大/太小/猜中提示
- 累計猜測次數、可重新開始
- 遊戲狀態存於 Flask `session`
- 完整的輸入驗證，錯誤輸入不當機、不計次

**明確不做（防護網）：**
- 資料庫、Docker、JS 框架（React/Vue）、Django
- 登入系統、使用者帳號、API、排行榜、多人遊戲、歷史紀錄
- 任何需求外的大型功能

這些邊界直接對應 prompt.md 的「防護網/限制條件」章節，設計時每一步都要能回答「這是不是需求要求的最小功能」。

---

## 2. 專案目錄結構

```
guess-number-game/
├── app.py                 # Flask 應用程式與遊戲邏輯
├── requirements.txt        # 相依套件（僅 Flask）
├── .gitignore              # 排除虛擬環境、快取檔
├── README.md                # 安裝、執行、玩法、上傳教學
├── templates/
│   └── index.html          # 遊戲主頁面（Jinja2 模板）
└── static/
    └── style.css            # 頁面樣式
```

不額外增加設定檔、藍圖（blueprint）、套件包裝結構——單一 `app.py` 已足以承載此規模的邏輯，符合「不要過度工程化」的限制。

---

## 3. 執行流程設計

### 3.1 狀態機

遊戲的核心狀態只有兩種：**進行中（playing）** 與 **已猜中（won）**。用 session 裡是否存在 `answer` 搭配一個 `guess_count` 即可表達，不需要額外的 `status` 欄位：

```
[首次進入 /]
     │
     ▼
 產生 answer, guess_count = 0  ──► 顯示輸入表單
     │
     │  POST /guess (有效輸入)
     ▼
 guess_count += 1
     │
     ├─ guess < answer  → 顯示「太小」，回到輸入表單
     ├─ guess > answer  → 顯示「太大」，回到輸入表單
     └─ guess == answer → 顯示「恭喜猜中了！你總共猜了 X 次」＋「再玩一次」按鈕
```

「再玩一次」觸發 `/reset`（或同一 route 以 POST 標記重置），效果等同於重新產生 `answer` 並將 `guess_count` 歸零。

### 3.2 Route 設計

| Route | Method | 用途 |
|---|---|---|
| `/` | GET | 顯示遊戲首頁。若 session 中無 `answer`（第一次造訪），產生新答案並初始化次數。 |
| `/guess` | POST | 接收表單猜測值，驗證輸入，比較答案，更新 session，回傳同一頁面並帶提示訊息。 |
| `/reset` | POST | 清除/重新產生 `answer`，`guess_count` 歸零，重導回 `/`。 |

為了讓初學者容易理解，統一用「渲染同一個 `index.html`」的方式回應，透過傳入的變數（`message`、`message_type`、`guess_count`、`is_won`）控制畫面顯示，而不是拆成多個模板。這比拆分多頁更貼近需求「簡單、清楚、容易理解」。

### 3.3 Session 資料結構

```python
session['answer']       # int, 1-100，正確答案
session['guess_count']  # int, 已累計的「有效」猜測次數
```

- 不使用資料庫，所有狀態靠 Flask session（預設以簽章過的 cookie 儲存）。
- `app.secret_key` 在開發環境給一個簡單固定值即可，並在 README / 註解中說明正式環境應改用環境變數（例如 `os environ.get("SECRET_KEY")`），避免誤導讀者把範例當成正式作法。
- 猜中後不清除 `answer`，直到玩家按下「再玩一次」才重置，這樣可以在猜中畫面上仍然正確顯示本局的 `guess_count`。

---

## 4. 輸入驗證設計

驗證需在計入次數與比較答案「之前」完成，任何驗證失敗都：
1. 不遞增 `guess_count`
2. 不呼叫 `int()`/比較邏輯造成例外
3. 回傳清楚的中文錯誤訊息，HTTP 200（不是 500）

驗證規則（依序檢查，命中即停止並回錯誤訊息）：

| 情況 | 檢查方式 | 錯誤訊息 |
|---|---|---|
| 沒有輸入 | 字串為空或去除空白後為空 | 「請輸入 1 到 100 之間的整數」 |
| 非數字 / 小數 | 用 `str.isdigit()` 或 `try/except ValueError` 包住 `int()` 轉換（拒絕含 `.` 的輸入） | 「請輸入 1 到 100 之間的整數」 |
| 小於 1 或大於 100 | 轉換成功後檢查範圍 | 「請輸入 1 到 100 之間的整數」 |

統一使用同一句錯誤訊息即可涵蓋 prompt.md 列出的所有錯誤情境，避免訊息過多造成初學者困惑，也符合「不要過度工程化」原則。

實作上建議寫成一個小函式 `parse_guess(raw: str) -> tuple[int | None, str | None]`，回傳 `(數值, 錯誤訊息)`，讓 route 內邏輯保持乾淨。

---

## 5. 前端（HTML）設計

`templates/index.html` 使用 Jinja2 渲染，單一頁面涵蓋所有畫面狀態：

- **結構（semantic HTML）**：`<header>` 放標題與說明，`<main>` 放遊戲表單與結果，`<footer>` 可放簡短資訊（可省略）。
- **表單**：`<form method="post" action="/guess">`，內含 `<input type="number" name="guess" min="1" max="100">` 與送出按鈕「猜！」。`min`/`max` 屬性只是前端提示，後端仍須完整驗證。
- **結果區塊**：依 `message_type`（`too_high` / `too_low` / `error` / `success`）顯示對應文字與樣式 class，方便 CSS 上色。
- **次數顯示**：顯示 `guess_count`（目前已猜次數）。
- **猜中後**：隱藏或停用猜測表單，顯示「恭喜猜中了！你總共猜了 X 次」與「再玩一次」按鈕（`<form method="post" action="/reset">`）。

不引入任何 JS 框架；如果需要小互動（例如自動 focus 輸入框），可用少量原生 `<script>`，但非必要則不加，避免超出「不使用 JavaScript Framework」以外還額外堆功能。

---

## 6. 樣式（CSS）設計

`static/style.css` 目標：簡潔、現代、RWD、無框架。

- 使用 flexbox 將卡片置中（`min-height: 100vh` + `display:flex; align-items:center; justify-content:center;`）。
- 單一「卡片」容器（`max-width: 420px` 左右），圓角、輕陰影，符合現代 GitHub Demo 風格。
- 用 CSS class 區分訊息狀態顏色：
  - `.message--error` → 警示色（如紅／橘）
  - `.message--hint`（太大/太小）→ 中性提示色
  - `.message--success` → 成功色（如綠）
- 響應式：容器寬度用 `%`/`max-width` 而非固定 px，並加 `padding` 讓手機上不貼邊；不需要 media query 太多層，一個基本斷點即可。
- 不使用 Bootstrap 或其他大型框架，全部手寫少量 CSS variables 方便維護配色。

---

## 7. requirements.txt / .gitignore

- `requirements.txt`：僅 `Flask`（可加版本號，例如 `Flask>=3.0`），不加未使用套件。
- `.gitignore` 至少包含：`__pycache__/`、`.venv`、`venv`、`.env`、`*.pyc` 等 Python 快取/環境檔。

---

## 8. README 內容規劃

依 prompt.md 要求，README.md 需包含：專案名稱、介紹、功能列表、使用技術、目錄結構、安裝方式（建立 venv、安裝需求、啟動 Flask）、瀏覽器開啟網址、遊戲玩法、GitHub 上傳步驟（含 placeholder repo URL）。這部分待正式撰寫 README 時再展開，此設計文件僅先確認要涵蓋哪些章節，避免遺漏。

---

## 9. 錯誤處理與邊界情況

| 情境 | 處理方式 |
|---|---|
| 使用者尚未有 session（第一次造訪 `/guess` 或 `/reset`，例如直接 POST） | 視為尚未開局，重新導向 `/` 讓其自然初始化，避免 `KeyError` |
| Session 被清除或過期 | `/` 的邏輯本身會偵測 `answer` 不存在並重新產生，具備自我修復能力 |
| 表單缺少 `guess` 欄位 | 用 `request.form.get('guess', '')` 取得，交由既有驗證流程處理成「沒有輸入」 |

---

## 10. 驗證 Checklist（對應設計目標）

- [ ] 第一次進入網站會產生答案
- [ ] 輸入比答案大的值會顯示「太大」
- [ ] 輸入比答案小的值會顯示「太小」
- [ ] 猜中時顯示成功訊息與總猜測次數
- [ ] 猜測次數計算正確（僅有效猜測才累計）
- [ ] 非數字 / 小數 / 空白輸入不會造成 500 錯誤，且不計次
- [ ] 超出 1–100 範圍不會計入猜測次數
- [ ] 重新開始後答案重新產生、猜測次數歸零

---

## 11. 後續實作提醒

- 程式碼需附適量中文註解（非逐行），優先說明「為什麼」而非「做什麼」。
- 開發用 `secret_key` 可寫死，但需在程式碼註解與 README 中明確提醒正式環境應改用環境變數。
- 所有實際「已測試通過」的說法都必須基於真的執行過；若只是設計/推導，需標註為「預期結果，待人工驗證」。
