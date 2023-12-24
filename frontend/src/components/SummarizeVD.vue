<script setup>
import axios from "axios";
import {ref} from "vue";
import {LLM_URL} from "@/constant/constant";

const videoId = ref('')
let res = ref('')
let summary = ref('')
const get_summarize = async () => {
    try {
        let response = await axios.post(LLM_URL + '/summarize-video', {}, {
                params: {
                    "video_id": videoId.value
                },
            }
        )
        summary.value = response.data.content

        console.log(summary.value)
    } catch (e) {
        res.value = 'Server Error'
        console.log(res.value)
        console.log(videoId.value)
    }
}
const formatWeatherSummary = (summary) => {
      return summary.replace(/\n/g, '<br>');
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
            <div v-html="formatWeatherSummary(summary)"></div>
        </div>
    </div>
</template>

<style scoped>

</style>