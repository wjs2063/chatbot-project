<script setup>
//import chatbot from "@/components/chatbot.vue";
//import Home from '@/pages/HomePageindex.vue'
</script>


<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <router-link class="navbar-brand" to="/">Home</router-link>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav mr-auto">
        <li class="nav-item-login">
          <router-link class="nav-link" to="/login">로그인</router-link>
        </li>

        <li class="nav-item active">
          <router-link class="nav-link" to="/SummarizeVideo">영상요약</router-link>
        </li>
        <li class="nav-item-chatbot">
          <router-link class="nav-link" to="/chatbot">챗봇</router-link>
        </li>
        <li class="nav-item-streaming">
          <router-link class="nav-link" to="/video/streaming">저작권 만료 영화 보기</router-link>
        </li>
        <!--        <li class="nav-item-login">-->
        <!--          <router-link class="nav-link" to="/login">로그인</router-link>-->
        <!--        </li>-->
      </ul>
      <!--            <form class="form-inline my-2 my-lg-0">-->
      <!--                <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">-->
      <!--                <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>-->
      <!--            </form>-->
    </div>
  </nav>

  <router-view/>


</template>


<style scoped>

</style>