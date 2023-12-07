<script setup>

</script>

<template>
  <head>
    <title>FastAPI video streaming</title>
  </head>
  <body>
  <video width="1200" controls>
    <source src="http://localhost:50000/api/v1/streaming" type="video/mp4"/>
  </video>
  </body>
</template>

<style scoped>

</style>