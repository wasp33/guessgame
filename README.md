# 猜數字遊戲（Guess Number Game）

一個使用 Python + Flask 打造的網頁版猜數字遊戲。適合 Flask / Python 網頁開發初學者練習與展示。

## 專案介紹

電腦會隨機產生一個 1 到 100 之間的整數，玩家在網頁上輸入猜測，系統會提示「太大」或「太小」，直到猜中為止，並顯示總共猜測的次數。遊戲狀態（答案、猜測次數）保存在 Flask session 中，不使用資料庫。

## 功能列表

- 每局開始隨機產生 1–100 的答案
- 網頁表單輸入猜測數字
- 猜測後即時顯示「太大」／「太小」／「恭喜猜中了！」
- 累計並顯示已猜測次數
- 猜中後可按「再玩一次」重新開始新的一局
- 完整的輸入驗證（空白、非數字、小數、超出範圍），錯誤輸入不會造成錯誤，也不計入次數

## 使用技術

- Python 3
- Flask（含內建 session）
- HTML5（semantic HTML）
- CSS3（不使用任何 CSS 框架）
- 不使用資料庫、不使用 JavaScript 框架

## 專案目錄

```
guessgame/
├── app.py               # Flask 應用程式與遊戲邏輯
├── requirements.txt      # 相依套件
├── .gitignore             # Git 排除清單
├── README.md               # 本文件
├── templates/
│   └── index.html         # 遊戲頁面
└── static/
    └── style.css           # 樣式
```

## 安裝與啟動方式

### 1. 建立 virtual environment

**Linux / macOS**

```bash
python3 -m venv .venv
```

**Windows**

```bat
python -m venv .venv
```

### 2. 啟用 virtual environment

**Linux / macOS**

```bash
source .venv/bin/activate
```

**Windows (Command Prompt)**

```bat
.venv\Scripts\activate
```

**Windows (PowerShell)**

```powershell
.venv\Scripts\Activate.ps1
```

### 3. 安裝套件

```bash
pip install -r requirements.txt
```

### 4. 啟動 Flask

```bash
python app.py
```

### 5. 瀏覽器開啟網址

啟動後於瀏覽器開啟：

```
http://127.0.0.1:5000
```

## 遊戲玩法

1. 開啟網頁後，電腦會自動產生一個 1–100 之間的答案（玩家看不到）。
2. 在輸入框輸入你猜的數字，按下「猜！」。
3. 系統會提示：
   - 「太大」：代表答案比你猜的小
   - 「太小」：代表答案比你猜的大
   - 「恭喜猜中了！你總共猜了 X 次」：代表你猜中了
4. 每一次有效的猜測都會累計次數；輸入錯誤（空白、非數字、小數、超出 1–100）不會計入次數。
5. 猜中後可以按「再玩一次」重新開始新的一局，答案會重新產生，次數歸零。

## 開發注意事項（Secret Key）

`app.py` 目前使用寫死的簡易 `secret_key` 方便本機開發與展示：

```python
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-please-change")
```

若要部署到正式環境，請務必設定環境變數 `SECRET_KEY` 為隨機且保密的字串，不要使用程式碼中的預設值，以避免 session 被偽造的風險。

## 上傳到 GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <YOUR_GITHUB_REPOSITORY_URL>
git push -u origin main
```

請將 `<YOUR_GITHUB_REPOSITORY_URL>` 換成你自己的 GitHub repository 網址。
