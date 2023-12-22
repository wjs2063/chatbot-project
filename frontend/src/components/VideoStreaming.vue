<script setup>
import axios from 'axios'
import {ref} from "vue";

let videoId = ref("");
let showButton = ref(true);
const url = "http://localhost:50000/api/v1/streaming/download";
const video_url = "http://localhost:50000/api/v1/streaming";

async function download() {
  try {
    console.log(url, videoId.value);
    await axios.post(url, {}, {
      params: {
        "video_id": videoId.value
      }
    })

  } catch {
    alert("요청에 실패했습니다. 새로고침후 다시 요청해주세요")
  }
}

const is_filled = () => {
  if (videoId.value) return true
  return false
}
const dynamic = () => {
  console.log(video_url + "/" + videoId.value)
  return video_url + "/" + videoId.value
}

</script>

<template>
  <head>
    <title>FastAPI video streaming</title>
  </head>
  <textarea v-model="videoId"></textarea>
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