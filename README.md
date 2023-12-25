# chatbot-project


### Architecture 
<img width="700" alt="image" src="https://github.com/wjs2063/chatbot-project/assets/76778082/12fddb4c-30e5-4218-85d0-e68820970eb0">

#### Backend(WAS)
- Infra : Docker
- Language : Python
- framework : FastAPI
- DB : postgresql,redis

#### API Gateway + ReverseProxy (Nginx)
- Nginx ( frontend 정적파일 제공)
- Nginx as a gateway server (upstream Routing)
- 처리율 제한장치 by rate limit (ip 기반적용 예정)
- SPOF(Singloe Point Of Fail) 문제가 발생할수있다.( Gateway 서버가 모든부하를 받으니 이부분은 Scale out 기법을 통해 해결하도록한다. (Kubernetes 를 이용한 자동 scale out,이후 적용 예정)

#### Frontend

- Infra : Docker
- Language : Javascript
- framework : Vuejs3

#### Auth 
1. access_token & refresh_token 

#### Streaming 
1. Movie Streaming 

### AI 
- WIT.AI : meta 에서 공개한 문장 의도 분석기, 대답을 빨리줄수있는 문장의 intent 에 대해서는 redis 에 캐싱하여 사용자에게 빠른 응답을 제공한다.
- GPT : LLM 모델




- Backend : Fastapi
  - 선정이유 : default 비동기 지원 및 해당 프로젝트는 데부분 File I/O 및 Network I/O 이므로 파이썬도 충분한 성능을 낼수있다고판단, 그리고 빠른 개발속도 
- frontend : Vuejs3, node-js : v18.18.2, @vue/cli 5.0.8
- AI : chatgpt ( 프롬프트 엔지니어링 추가)
- 2023/10/24 (redis 추가 및 WIT.AI 서버 추가)


### 기능 
- 대화형 멀티턴 chatbot 시스템
- video_summarization 기능 추가 (2023-11-14)
- video_streaming 기능 추가 (2023-12-07)
- video_streaming 빨리감기 되감기 기능추가(2023-12-21)

### Video Streaming 
 ~~youtube video_id 를 가지고 준비요청을 보내면 서버에서 다운로드후 영상 스트리밍~~

 ~~개선사항 : youtube가 아니더라도 저작권에 걸리지않는 영화를 스트리밍 진행 (현재는 유튜브만 가능)~~

- 개선사항 : 저작권에 걸리지않는 영화목록 스트리밍 기능 추가
<img width="300" alt="image" src="https://github.com/wjs2063/chatbot-project/assets/76778082/219c7360-439c-41ac-b558-8a516544e68b">
<img width="300" alt="image" src="https://github.com/wjs2063/chatbot-project/assets/76778082/16d7ce0a-c6dd-4efb-8d3b-07a0e3ff1783">



### Video Summarize 기대효과
- video_summarization := 바빠서 영상을 차마 다 보지못하거나, 기상청 예보같은(5~6분) 결론만필요한 영상들에대해 빠르게 요약결과를 내어줄수있다. (이미 요청한 동영상 요약결과는 0.3초만에 받아볼수있음)
- https://www.youtube.com/watch?v=fb8FalIe0Ig (15분) X-process_time = 95초
- https://www.youtube.com/watch?v=IEEgpggMKBs (6분 %6초) X-process_time = 57초
- <img width="300" alt="image" src="https://github.com/wjs2063/chatbot-project/assets/76778082/55777adb-0beb-4cff-931c-7d5df942c8d3">



### Chatbot 기대효과
사용자의 질문에 맞는 응답제공

<img width="300" alt="image" src="https://github.com/wjs2063/chatbot-project/assets/76778082/8b39e331-ca95-4155-87d7-36568354f3f9">






### llms-chatbot 실행 로직 

1. Client 발화 요청
2. Wit.ai 에서 해당발화 특징 추출 응답
3. 해당 발화의 특징을 가진 key 를 redis 에서 검색, ( 있다면 바로 client 에게 응답제공 threshold 이상인값만 검색함)
4. 없다면 GPT 에게 질문
5. 응답을 redis 에 저장 ( threshold 이상인 발화에 대해서만 진행함)
6. 최종응답 반환


#### Add http MiddleWare 
- process_time 측정 middleware 추가 (2023-11-14)


### 비디오 출처 (공유마당)
- convert wmv to mp4
- ffmpeg 사용 
```
convert_script.sh
``` 


### Cost

Project 구성 비용 :  
- 5달러(chatgpt API 이용)
- 실사용시 비용이 늘어날수있음.( 서버 + GPT API 비용)


 

### USAGE 

#### Nginx 
```
/etc/nginx/conf.d/chatbot-route.conf
/etc/nginx/nginx.conf

해당경로에 conf 파일 넣어두기

/code/dist -> static files 경로 


```


#### frontend

```
npm install package.json

//dev
npm run serve

//product

npm run build

dist 파일 Nginx 컨테이너의 /code에 두기 

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

or

gunicorn -w 4 -b 0.0.0.0:8000 --bind unix:/tmp/myapi.
sock main:app --worker-class uvicorn.workers.UvicornWorker
```

필요시 

```
apk add gcc g++ linux-headers
```
