<template>
  <div class="box-container">
    <div class="chat-box">
        <div class="box-banner"></div>
        <div class="box-body">
            <ChatRow v-for="(data, index) in chatData" 
                :key="index" 
                :isRight="data.username === 'Me'" 
                :username="data.username" 
                :content="data.content"
                :audio="data.audio"
                :fakehtml="data.fake_html"
            />
        </div>
        <div class="box-end">
            <UserInput @submit="submitMesg" />
        </div>
    </div>
  </div>
</template>

<script>
import ChatRow from './ChatRow.vue'
import UserInput from './UserInput.vue'

const USERNAME = {
    0: "Bot",
    1: "Me"
}

export default {
  name: 'ChatContainer',
  data() {
    return {
        chatData: [{
            username: "Bot",
            content: "Hi! This is CovBot. I can assist you with anything you want to know about Covid-19. Try asking me questions about covid."
        }, {
            username: "Bot",
            content: "DISCLAIMER: Please note that the information provided here is not a substitute for advice from a medical professional."
        }] // [{username: "Me", content: "What is the weather today?"},{username: "Bot", content: "Today is windy. Today is windy.Today is windy Today is windy Today is windy."}]
        
    };
  },
  components: {
      ChatRow,
      UserInput
  },
  methods: {
    submitMesg ({content, audio = null, user = 1, fake_html = ''}) { // user 0: chatbot, 1: user
        console.log('submitMesg', content, user)
        let newData = { 
            username: USERNAME[user], 
            content: content || '', 
            audio,
            fake_html
        }
        this.chatData.push(newData)
        this.scrollToBottom()
    },
    scrollToBottom() {
        this.$nextTick(() => {
            var container = this.$el.querySelector(".box-body");
            container.scrollTop = container.scrollHeight;
        })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.box-container {
    position: absolute;
    width: 100%;
}
.chat-box {
    position: relative;
    display: flex;
    flex-direction: column;
    width: 50vh;
    height: 80vh;
    background: white;
    margin: 0 auto;
    border-radius: 8px;
    box-shadow: 6px 6px 5px 2px #9da0a66b;
}
.box-banner {
    width: 100%;
    background: #abdbdb;
    height: 60px;
    border-radius: 8px 8px 0 0;
}
.box-body {
    flex: 1;
    overflow: scroll;
}
.box-end {}
</style>
