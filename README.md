# 維基關鍵字配對
使用維基百科資料進行相似詞搜尋

# 配置
[下載wiki預處理檔案](https://github.com/p208p2002/key-match-with-wiki/releases/tag/0.0.2)，放置在splitdata資料夾底下

# 進行相似詞搜尋
```
$ python main.py -k=陳水扁 -sr=25
```
```
-k --key 搜尋關鍵字
-sr --serach_range 搜尋範圍/深度(default:25)
-t --thread 執行緒啟用上限(default:4)
```

# 範例輸出
```
Key: 
陳水扁

Output:
陳水扁
馬英九
蔡英文
李登輝
蘇貞昌
謝長廷
遊錫堃
副總統
國民黨
蔣經國
```



