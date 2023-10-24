# chatbot-project




- Backend : Fastapi
- frontend : Vuejs3, node-js : v18.18.2, @vue/cli 5.0.8
- AI : chatgpt ( 프롬프트 엔지니어링 추가)
- 2023/10/24 (redis 추가 및 WIT.AI 서버 추가)

### Backend
- Infra : Docker
- Language : Python
- framework : FastAPI
- DB : postgresql,redis

### Frontend

- Infra : Docker
- Language : Javascript
- framework : Vuejs3


### AI 
- WIT.AI : meta 에서 공개한 문장 의도 분석기, 대답을 빨리줄수있는 문장의 intent 에 대해서는 redis 에 캐싱하여 사용자에게 빠른 응답을 제공한다.
- GPT : LLM 모델


### Architecture 

![image](https://github.com/wjs2063/chatbot-project/assets/76778082/951b4fc0-327c-4d8d-b123-f469ad9e1cfa)





### Cost

Project 구성 비용 :  
- 5달러(chatgpt API 이용)
- 실사용시 비용이 늘어날수있음.( 서버 + GPT API 비용)


 
### 결과예시


![스크린샷 2023-10-19 234936](https://github.com/wjs2063/chatbot-project/assets/76778082/8b39e331-ca95-4155-87d7-36568354f3f9)   


### USAGE 

#### frontend

```
npm install package.json

//dev
npm run serve

//product

npm run build

serve -l [port] dist

```


#### backend

```
docker compose up -d
```

in docker container  

```
cd /code

python -m pip install -r requirements.txt

cd /server/app

uvicorn main:app --host=0.0.0.0
```

필요시 

```
apk add gcc g++
```
