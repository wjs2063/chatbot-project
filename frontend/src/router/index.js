

import {createRouter,createWebHistory} from "vue-router";
import Home from '../pages/HomePageindex.vue'
import Summarize from '@/pages/summarizeVideo/SummarizeVideoindex.vue'
import Chatbot from '@/pages/chatbot/ChatBotindex.vue'
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
            }
        ]
    }
)


export default router;



