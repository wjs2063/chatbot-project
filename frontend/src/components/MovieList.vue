<template>
  <div>
    <h2>Movie List</h2>
    <ul>
      <li v-for="movie in movies" :key="movie.video_name">
        <router-link :to="{ name: 'movieDetail', params: { video_name: movie.name }}">
          <button>{{ movie.name }}</button>
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      movies: []
    };
  },
  mounted() {
    // 서버에서 영화 목록을 받아오는 API 요청
    axios.get('http://localhost:50000/api/v1/streaming/movie-list?page=0') // 서버의 실제 URL로 변경
        .then(response => {
          this.movies = response.data;
          console.log(this.movies);
        })
        .catch(error => {
          console.error("API Error:", error);
        });
  },
};
</script>