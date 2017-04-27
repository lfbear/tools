# small tools

+ [Baidu Voice API](/baidu_tools.py) (百度语音服务rest api调用封装)

A single python script (depend on python libs: requests, base64, json, os)

  - Voice to Text (语音识别服务)
  
```
    api = baiduYuyin(API_KEY,API_SECRET) # you can get key and secret at http://yuyin.baidu.com/, it's free
    words = api.sound2text('./test.wav') # words is a list, failed if words is empty
    # special for test.wav, it must be a wav file, 8kHZ and 16bit
    # I get wav file by this cmd: arecord -D "plughw:CARD=Device" -d 5 -r 8000 -t wav -f S16_LE test.wav
```
  
  - Text to Voice (语音合成服务)
```
  api = baiduYuyin(API_KEY,API_SECRET)
  api.text2sound(output_msg,file_name); # output_msg is a list, file_name is a mp3 file that voice will storage
```
