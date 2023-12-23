<script setup>
// // import axios from 'axios'
// import {ref} from "vue";
//
// let request_video_id = ref("");
// let video_id = ref("");
// let showButton = ref(true);
// const video_url = "http://localhost:50000/api/v1/streaming";



// function sleep(ms) {
//   return new Promise(resolve => setTimeout(resolve, ms));
// }

// async function download() {
//   try {
//     console.log(url, request_video_id.value);
//     await axios.post(url, {}, {
//       params: {
//         "video_id": request_video_id.value
//       }
//     })
//     await sleep(3000)
//     video_id.value = request_video_id;
//   } catch {
//     alert("요청에 실패했습니다. 새로고침후 다시 요청해주세요")
//   }
// }




// const get_streaming_url = () => {
//   console.log(video_url + "/" + request_video_id.value)
//   return video_url + "/" + request_video_id.value
// }

</script>

<template>
  <head>
    <title>FastAPI video streaming</title>
  </head>
<!--  <textarea v-model="request_video_id"></textarea>-->
<!--  <button @click="is_clicked()">영화 시청</button>-->
  <body>
<!--  <div v-if="is_clicked()">-->
<!--    <video width="1200" controls>-->
<!--      <source :src="get_streaming_url()" type="video/mp4"/>-->
<!--    </video>-->
<!--  </div>-->
  </body>
</template>

<style scoped>

</style>