<template>
  <div>
    <h2>{{ videoName }}</h2>
  </div>
    <div>
      <video width="1200" controls>
        <source :src="get_streaming_url()" type="video/mp4">
      </video>
    </div>


</template>

<script>
// import axios from 'axios';


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
      console.log('http://localhost:50000/api/v1/streaming/' + this.videoName)
      return 'http://localhost:50000/api/v1/streaming/' + this.videoName;
    }
  },
  mounted() {
    this.videoName = this.$route.params.video_name;
  }
};
</script>

<style scoped>

</style>