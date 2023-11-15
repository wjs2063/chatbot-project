# chatbot-project

- Backend : Fastapi
- frontend : Vuejs3, node-js : v18.18.2, @vue/cli 5.0.8
- AI : chatgpt ( 프롬프트 엔지니어링 추가)
- 2023/10/24 (redis 추가 및 WIT.AI 서버 추가)


### 기능 
- 대화형 멀티턴 chatbot 시스템
- video_summarization 기능 추가 (2023-11-14)

### Backend
- Infra : Docker
- Language : Python
- framework : FastAPI
- DB : postgresql,redis

### API Gateway + ReverseProxy (Nginx)
- Nginx
- Nginx as a gateway server ( Routing)
- 적절한 Routing 기법을 통해 해당 용도에맞는 뒷단의 서버로 요청
- SPOF(Singloe Point Of Fail) 문제가 발생할수있다.( Gateway 서버가 모든부하를 받으니 이부분은 Scale out 기법을 통해 해결하도록한다. (Kubernetes 를 이용한 자동 scale out) 

### Frontend

- Infra : Docker
- Language : Javascript
- framework : Vuejs3


### AI 
- WIT.AI : meta 에서 공개한 문장 의도 분석기, 대답을 빨리줄수있는 문장의 intent 에 대해서는 redis 에 캐싱하여 사용자에게 빠른 응답을 제공한다.
- GPT : LLM 모델


### Architecture 
![image](https://github.com/wjs2063/chatbot-project/assets/76778082/53e78a85-32e6-44f7-aa4a-83ce4663bd59)



### chatbot 실행 로직 

1. Client 발화 요청
2. Wit.ai 에서 해당발화 특징 추출 응답
3. 해당 발화의 특징을 가진 key 를 redis 에서 검색, ( 있다면 바로 client 에게 응답제공 threshold 이상인값만 검색함)
4. 없다면 GPT 에게 질문
5. 응답을 redis 에 저장 ( threshold 이상인 발화에 대해서만 진행함)
6. 최종응답 반환


#### Add http MiddleWare 
- process_time 측정 middleware 추가 (2023-11-14)




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
