## *The document of [translate_api](https://github.com/shinalone/translate_api/blob/master/README.md)*

### *1. Feactures:*
- *Google. - translate_api is a python3 library that uses the translation functionality of the Google interface.*
- *Switch the server. - The default server is Google-China server, the user can switch to (google.com) server.*
- *All languages can be translated.*

### *2. Usage:*
```python
>>>from translate_api.translate_api import api
>>>print(api())
''
## Default function api(): api(text=r'',from_language='en',to_language='zh-CN',host='https://translate.google.cn')

>>>api('Hello,World!')
'你好，世界！'

>>>api('你好，世界！','zh-CN','ko')
'안녕, 세상!'

>>>print(api(text=r'こんにちは世界！',from_language='ja',to_language='en',host='https://translate.google.cn'))
'Hello World!'

## Finally, you can try switching the `host` to use. 
```

