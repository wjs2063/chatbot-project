

import {createRouter,createWebHistory} from "vue-router";
import Home from '../pages/HomePageindex.vue'
import Summarize from '@/pages/SummarizeVideo/SummarizeVideoindex.vue'
import Chatbot from '@/pages/ChatBot/ChatBotindex.vue'
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
                path : '/SummarizeVideo',
                name : 'SummarizeVideo',
                component : Summarize
            },
                        {
                path : '/ChatBot',
                name : 'ChatBot',
                component : Chatbot
            }
        ]
    }
)


export default router;



