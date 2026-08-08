[角色與背景]

你是一位資深 Python Web 開發工程師，同時也是擅長帶領初學者實作專案的程式設計導師。

我要建立一個適合初學者學習、可直接放到 GitHub 展示的「Python 網頁版猜數字遊戲」。

技術限制如下：

* Python
* Flask
* HTML
* CSS
* 不使用資料庫
* 不使用 React、Vue、Django 等額外框架
* 優先使用 Python 標準函式庫與 Flask 內建能力
* 程式碼應簡單、清楚、容易理解
* 專案必須可以在一般本機 Python 環境執行

---

[核心目標]

建立一個完整可執行的 Flask 網頁版猜數字遊戲。

遊戲需求：

1. 每局開始時，由電腦隨機產生一個 1 到 100 之間的整數。

2. 玩家在網頁輸入自己的猜測。

3. 如果玩家猜的數字大於答案，顯示：

   「太大」

4. 如果玩家猜的數字小於答案，顯示：

   「太小」

5. 如果玩家猜中答案，顯示：

   「恭喜猜中了！」

   並顯示：

   「你總共猜了 X 次」

6. 每一次有效猜測都必須累計猜測次數。

7. 玩家猜中後，可以重新開始一局新的遊戲。

遊戲狀態請優先使用 Flask session 管理，包括：

* 正確答案
* 猜測次數

不要使用資料庫。

---

[執行步驟]

請依照以下順序完成專案。

第一步：設計專案目錄

建立一個清楚、適合 GitHub 展示的專案，例如：

guess-number-game/

app.py

requirements.txt

.gitignore

README.md

templates/
index.html

static/
style.css

如果你認為有必要增加其他檔案，可以增加，但不要過度設計。

第二步：建立 Flask Application

在 app.py 中：

1. 初始化 Flask。
2. 設定 session。
3. 建立首頁 route。
4. 使用 random.randint(1, 100) 產生答案。
5. 使用 session 保存答案。
6. 使用 session 保存猜測次數。
7. 接收 HTML form POST。
8. 比較玩家猜測與正確答案。
9. 回傳「太大」、「太小」或「猜中」訊息。
10. 實作重新開始遊戲功能。

第三步：輸入驗證

必須處理以下情況：

* 玩家沒有輸入內容
* 玩家輸入非數字
* 玩家輸入小數
* 玩家輸入小於 1
* 玩家輸入大於 100

這些錯誤輸入：

* 不應造成 Flask 500 Error
* 不應計入猜測次數
* 應顯示清楚的中文錯誤訊息

例如：

「請輸入 1 到 100 之間的整數」

第四步：建立 HTML UI

建立 templates/index.html。

至少包含：

* 遊戲標題
* 說明文字
* 數字輸入框
* 「猜！」按鈕
* 遊戲結果提示
* 猜測次數
* 猜中後的「再玩一次」按鈕

HTML 請使用標準 semantic HTML。

第五步：建立 CSS

建立 static/style.css。

UI 要求：

* 簡潔
* 現代
* 適合 GitHub Demo
* 畫面置中
* 手機與桌面皆可正常觀看
* 不使用大型 CSS Framework
* 不使用 Bootstrap，除非有非常充分理由

不要把 UI 做得過度複雜。

第六步：建立 requirements.txt

只放實際需要的 Python 套件。

例如 Flask。

不要加入沒有使用的 dependency。

第七步：建立 .gitignore

至少排除：

* **pycache**
* .venv
* venv
* .env
* Python cache files

第八步：建立 README.md

README 至少包含：

1. 專案名稱
2. 專案介紹
3. 功能列表
4. 使用技術
5. 專案目錄
6. 安裝方式
7. 建立 virtual environment
8. 安裝 requirements
9. 啟動 Flask
10. 瀏覽器開啟網址
11. 遊戲玩法
12. GitHub 上傳方式

GitHub 上傳部分請提供：

git init

git add .

git commit -m "Initial commit"

git branch -M main

git remote add origin <YOUR_GITHUB_REPOSITORY_URL>

git push -u origin main

不要假設我的 GitHub repository URL，使用 placeholder。

第九步：提供教學說明

完成程式碼後，另外用初學者可以理解的方式說明：

1. Flask route 是什麼
2. GET 與 POST 在這個專案中的用途
3. HTML form 如何傳資料到 Flask
4. request.form 如何取得玩家輸入
5. Flask session 是什麼
6. 為什麼答案應存在 session
7. 如何累計猜測次數
8. random.randint(1, 100) 的作用
9. templates 與 static 資料夾的作用

第十步：驗證流程

請在回答最後提供人工驗證 Checklist。

至少包含：

[ ] 第一次進入網站會產生答案

[ ] 輸入比答案大的值會顯示「太大」

[ ] 輸入比答案小的值會顯示「太小」

[ ] 猜中時顯示成功訊息

[ ] 猜中時顯示總猜測次數

[ ] 猜測次數計算正確

[ ] 非數字輸入不會造成錯誤

[ ] 超出 1–100 不會計入猜測次數

[ ] 重新開始後答案重新產生

[ ] 重新開始後猜測次數歸零

---

[輸出格式]

請嚴格按照以下順序回答：

## 1. 專案架構

使用 tree 格式顯示完整目錄。

## 2. app.py

提供完整程式碼。

不可只提供片段。

## 3. templates/index.html

提供完整程式碼。

## 4. static/style.css

提供完整程式碼。

## 5. requirements.txt

提供完整內容。

## 6. .gitignore

提供完整內容。

## 7. README.md

提供可以直接存成 README.md 的完整內容。

## 8. 程式執行方式

依序提供：

* 建立 virtual environment
* 啟用 virtual environment
* pip install
* 啟動程式
* 瀏覽器測試

Windows 與 Linux/macOS 指令若不同，請分別說明。

## 9. Flask 教學說明

說明：

* route
* request
* form
* GET
* POST
* session
* random
* templates
* static

## 10. GitHub 上傳方式

提供完整 Git 指令。

## 11. 驗證 Checklist

列出可以逐項測試的功能。

每一份程式碼都必須標明檔案路徑，例如：

```python
# app.py
```

不要使用：

「其他部分省略」

「同上」

「略」

等方式省略程式碼。

---

[防護網/限制條件]

1. 不要過度工程化。
2. 不使用資料庫。
3. 不使用 Docker。
4. 不使用 JavaScript Framework。
5. 不導入 React、Vue、Django。
6. 不需要登入系統。
7. 不需要 User Account。
8. 不需要 API。
9. 不需要排行榜。
10. 不需要多人遊戲。
11. 不需要遊戲歷史資料庫。
12. 不要增加需求之外的大型功能。
13. 不要編造「我已執行成功」或「測試已通過」。
14. 如果無法實際執行程式，請明確寫成「以下為預期結果與人工驗證方式」。
15. 所有 Python 程式碼必須可以直接組成完整專案，不得缺少必要 import。
16. 所有使用到的套件必須出現在 requirements.txt。
17. 不要把正式環境 Secret Key 直接硬編碼卻不說明風險。
18. 開發示範可以提供簡單 Secret Key，但必須說明正式環境應改用環境變數。
19. 遇到不確定事項時，優先採用最簡單、最適合初學者的方案。
20. 程式碼應附適量中文註解，但不要每一行都加註解。

完成標準：

* git clone 後可依 README 建立環境。
* 可啟動 Flask 網站。
* 五項核心猜數字功能完整。
* 錯誤輸入受到控制。
* 程式碼適合初學者閱讀。
* UI 簡潔且完整。
* GitHub 專案檔案齊全。
* README 足以讓另一個使用者自行啟動專案。
