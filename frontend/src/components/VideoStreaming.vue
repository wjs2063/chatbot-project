<script setup>
import axios from 'axios'
import {ref} from "vue";

let request_video_id = ref("");
let video_id = ref("");
let showButton = ref(true);
const url = "http://localhost:50000/api/v1/streaming/download";
const video_url = "http://localhost:50000/api/v1/streaming";

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function download() {
  try {
    console.log(url, request_video_id.value);
    await axios.post(url, {}, {
      params: {
        "video_id": request_video_id.value
      }
    })
    await sleep(3000)
    video_id.value = request_video_id;
  } catch {
    alert("요청에 실패했습니다. 새로고침후 다시 요청해주세요")
  }
}

const is_filled = () => {
  if (video_id.value) return true
  return false
}
const dynamic = () => {
  console.log(video_url + "/" + request_video_id.value)
  return video_url + "/" + request_video_id.value
}

</script>

<template>
  <head>
    <title>FastAPI video streaming</title>
  </head>
  <textarea v-model="request_video_id"></textarea>
  <button v-if="showButton" @click="download()">요청 보내기</button>
  <body>
  <div v-if="is_filled()">
    <video width="1200" controls>
      <source :src="dynamic()" type="video/mp4"/>
    </video>
  </div>
  </body>
</template>

<style scoped>

</style>