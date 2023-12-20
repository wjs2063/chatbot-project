

import {createRouter,createWebHistory} from "vue-router";
import Home from '../pages/HomePageindex.vue'
import Summarize from '@/pages/summarizeVideo/SummarizeVideoindex.vue'
import Chatbot from '@/pages/chatbot/ChatBotindex.vue'
import VideoStreaming from '@/pages/video_streaming/VideoStreamingindex.vue'
import LoginForm from "@/pages/Login/LoginFormindex.vue";
const router = createRouter(
    {
        history :createWebHistory(),
        routes : [
            {
                path : '/',
                name : 'Home',
                component : Home
            },
            {
                path : '/summarizeVideo',
                name : 'summarizeVideo',
                component : Summarize
            },
                        {
                path : '/chatbot',
                name : 'chatbot',
                component : Chatbot
            },
            {
                path : '/video/streaming',
                name : 'streaming',
                component : VideoStreaming
            },
            {
                path : '/login',
                name : 'sign-up',
                component : LoginForm
            }
        ]
    }
)


export default router;



