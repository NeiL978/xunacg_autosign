# XunACG自動簽到

XunACG論壇的自動簽到程式。  
運用了Requests及BeautifulSoup的技術。

## 功能
* 自動登入XunACG論壇
* 每日簽到
* 多帳號簽到
* 每日嫖下載卷（免費取得次數，每日不一樣）

## 待加入的功能
* ~~多帳號簽到~~
* 推播到通訊軟體中

## 使用方式
### 1. 安裝Requests及BeautifulSoup庫

```shell
pip install -r requirements.txt
              or
pip3 install -r requirements.txt
```
### 2. 填入資料
將`config-template.py`更名為`config.py`中，將帳號密碼填入。


| Name     | Value  | 說明       |
|----------|--------|----------|
| EMAIL    | test03 | 帳號/Email |
| PASSWORD | xxxxx  | 密碼       |
| UID      | 12345  | 到個人中心查看  |
