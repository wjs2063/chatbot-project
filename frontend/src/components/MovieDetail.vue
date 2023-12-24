<template>
  <div>
    <h2>{{ videoName }}</h2>
  </div>
    <div>
      <video width="500" controls>
        <source :src="get_streaming_url()" type="video/mp4">
      </video>
    </div>


</template>

<script>
// import axios from 'axios';
import {STREAMING_URL} from "@/constant/constant";

export default {
  data() {
    return {
      videoName: '',

    };
  },
  methods: {
    // sendApiRequest() {
    //   const apiUrl = `http://localhost:50000/api/v1/streaming/${this.videoName}`;
    //
    //   axios.get(apiUrl)
    //       .then(response => {
    //         console.log("API Response:", response.data);
    //       })
    //       .catch(error => {
    //         console.error("API Error:", error);
    //       });
    // },
    get_streaming_url() {
      return STREAMING_URL+ "/" + this.videoName;
    }
  },
  mounted() {
    this.videoName = this.$route.params.video_name;
  }
};
</script>

<style scoped>

</style>