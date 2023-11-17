<script setup>
import axios from "axios";
import {ref} from "vue";

const videoId = ref('')
let res = ref('')
let summary = ref('')
const get_summarize = async () => {
    try {
        let response = await axios.post('http://www.codeplanet.site:50000/api/v1/items/summarize_video', {}, {
                params: {
                    "video_id": videoId.value
                },
            }
        )
        summary.value = response.data.content

    } catch (e) {
        res.value = 'Server Error'
        console.log(res.value)
        console.log(videoId.value)
    }


}

</script>

<template>
    <div>
        <h1>YouTube Video Summary</h1>
        <div>
            <label for="videoId">Enter YouTube Video ID:</label>
            <input v-model="videoId" type="text" id="videoId"/>
            <button @click="get_summarize">Get Summary</button>
        </div>
        <div v-if="summary">
            <h2>Summary:</h2>
            <p>{{ summary }}</p>
            <div v-html="summary"></div>
        </div>
    </div>
</template>

<style scoped>

</style>