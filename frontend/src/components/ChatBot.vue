<script setup>
import {ref} from "vue";
import axios from "axios";
import BounceLoader from "@/components/BounceLoader.vue";

let message_datas = ref([]);
let user_message = ref('')
let chatbot_message = ref('')
let is_server_loading = ref(false);
const get_message = async () => {
    is_server_loading = true
    user_message.value = user_message.value.trim()
    let msg = user_message.value
    message_datas.value.push({"user": user_message.value})
    user_message.value = ''
    let body = {
        "messages": msg
    }
    try {
        let res = await axios.post('http://localhost:8000/api/v1/items/chat',
            JSON.parse(JSON.stringify(body))
        )
        chatbot_message.value = res.data["result"]

    } catch (e) {
        chatbot_message.value = "알아듣지 못했어요. 서버응답이 지연되고있을수 있으니 잠시후에 다시 찾아주세요."
    }
    message_datas.value.push({"server": chatbot_message.value})
    is_server_loading = false;

}
</script>

<template>
    <section style="background-color: #eee;">
        <div class="container py-5">

            <div class="row d-flex justify-content-center">
                <div class="col-md-8 col-lg-6 col-xl-4">

                    <div class="card" id="chat1" style="border-radius: 15px;">
                        <div
                            class="card-header d-flex justify-content-between align-items-center p-3 bg-info text-white border-bottom-0"
                            style="border-top-left-radius: 15px; border-top-right-radius: 15px;">
                            <i class="fas fa-angle-left"></i>
                            <p class="mb-0 fw-bold">AI ChatBot</p>
                            <i class="fas fa-times"></i>
                        </div>
                        <div class="card-body">

                            <div class="d-flex flex-row justify-content-start mb-4">
                                <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava1-bg.webp"
                                     alt="avatar 1" style="width: 45px; height: 100%;">
                                <div class="p-3 ms-3"
                                     style="border-radius: 15px; background-color: rgba(57, 192, 237,.2);">
                                    <p class="small mb-0">안녕하세요. 저는 당신을 도와줄 Chatbot 입니다. 저에게 무엇이든 물어보세요!
                                        도와드릴게요!
                                    </p>
                                </div>
                            </div>

                            <div v-for="messages in message_datas" :key="messages">
                                <div v-if=" 'server' in messages" class="d-flex flex-row justify-content-start mb-4">
                                    <img
                                        src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava1-bg.webp"
                                        alt="avatar 1" style="width: 45px; height: 100%;">
                                    <div class="p-3 ms-3"
                                         style="border-radius: 15px; background-color: rgba(57, 192, 237,.2);">
                                        <p class="small mb-0"> {{ messages['server'] }}
                                        </p>
                                    </div>
                                </div>
                                <div v-else>
                                    <div class="d-flex flex-row justify-content-end mb-4">
                                        <div class="p-3 me-3 border"
                                             style="border-radius: 15px; background-color: #fbfbfb;">
                                            <p class="small mb-0">{{ messages['user'] }}</p>
                                        </div>
                                        <img
                                            src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava6-bg.webp"
                                            alt="avatar 1" style="width: 45px; height: 100%;">
                                    </div>
                                </div>
                            </div>

                            <div v-if="is_server_loading === true">
                                <img
                                    src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava1-bg.webp"
                                    alt="avatar 1" style="width: 45px; height: 100%;">
                                <div class="p-3 ms-3">
                                    <BounceLoader />
                                </div>
                            </div>

                            <div class="form-outline">
                                <textarea class="form-control" id="textAreaExample" rows="4"
                                          @keyup.enter="get_message" v-model="user_message"></textarea>
                                <label class="form-label" for="textAreaExample">Type your message</label>
                            </div>


                        </div>
                    </div>

                </div>
            </div>

        </div>
    </section>
</template>

<style scoped>

#chat1 .form-outline .form-control ~ .form-notch div {
    pointer-events: none;
    border: 1px solid;
    border-color: #eee;
    box-sizing: border-box;
    background: transparent;
}

#chat1 .form-outline .form-control ~ .form-notch .form-notch-leading {
    left: 0;
    top: 0;
    height: 100%;
    border-right: none;
    border-radius: .65rem 0 0 .65rem;
}

#chat1 .form-outline .form-control ~ .form-notch .form-notch-middle {
    flex: 0 0 auto;
    max-width: calc(100% - 1rem);
    height: 100%;
    border-right: none;
    border-left: none;
}

#chat1 .form-outline .form-control ~ .form-notch .form-notch-trailing {
    flex-grow: 1;
    height: 100%;
    border-left: none;
    border-radius: 0 .65rem .65rem 0;
}

#chat1 .form-outline .form-control:focus ~ .form-notch .form-notch-leading {
    border-top: 0.125rem solid #39c0ed;
    border-bottom: 0.125rem solid #39c0ed;
    border-left: 0.125rem solid #39c0ed;
}

#chat1 .form-outline .form-control:focus ~ .form-notch .form-notch-leading,
#chat1 .form-outline .form-control.active ~ .form-notch .form-notch-leading {
    border-right: none;
    transition: all 0.2s linear;
}

#chat1 .form-outline .form-control:focus ~ .form-notch .form-notch-middle {
    border-bottom: 0.125rem solid;
    border-color: #39c0ed;
}

#chat1 .form-outline .form-control:focus ~ .form-notch .form-notch-middle,
#chat1 .form-outline .form-control.active ~ .form-notch .form-notch-middle {
    border-top: none;
    border-right: none;
    border-left: none;
    transition: all 0.2s linear;
}

#chat1 .form-outline .form-control:focus ~ .form-notch .form-notch-trailing {
    border-top: 0.125rem solid #39c0ed;
    border-bottom: 0.125rem solid #39c0ed;
    border-right: 0.125rem solid #39c0ed;
}

#chat1 .form-outline .form-control:focus ~ .form-notch .form-notch-trailing,
#chat1 .form-outline .form-control.active ~ .form-notch .form-notch-trailing {
    border-left: none;
    transition: all 0.2s linear;
}

#chat1 .form-outline .form-control:focus ~ .form-label {
    color: #39c0ed;
}

#chat1 .form-outline .form-control ~ .form-label {
    color: #bfbfbf;
}
</style>