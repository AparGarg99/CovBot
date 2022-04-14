<template>
  <div class="input-container">
      <div class="send-options">
          <el-button type="text" @click="changeOpt(0)"><span :class="['option-label', {'active-opt': option === 0}]">Q&A</span></el-button>
          <el-button type="text" @click="changeOpt(1)"><span :class="['option-label', {'active-opt': option === 1}]">Fake tweet detection</span></el-button>
          <el-button type="text" @click="changeOpt(2)"><span :class="['option-label', {'active-opt': option === 2}]">Covid test using cough</span></el-button>
      </div>
      <div class="send-box">
            <el-button v-if="option===2" class="record-btn" :class="[{'red-btn': !loading && recording}]" @click="clickHandler">
                <span v-if="loading">Wait about 30s...</span>
                <span v-else-if="recording">Stop</span>
                <span v-else>Record</span>
            </el-button>
            <el-input v-else v-model="input" placeholder="Please input" />

            <el-button @click="sendMessage">send</el-button>
      </div>
  </div>
</template>

<script>
import { postMsg, uploadAudio } from '../api/api'
import useRecorder from '@/composables/useRecorder'

export default {
  name: 'UserInput',
  props: {},
  setup () {
    const { recording, audioBlob, audioWave, recordClickHandler } = useRecorder()

    return {
      recording,
      audioBlob,
      audioWave,
      recordClickHandler
    }
  },
  data() {
    return {
        input: '',
        option: 0,
        loading: false // doing the prediction
    };
  },
  components: {

  },
  methods: {
      sendMessage () {
          if (this.loading) {
              return
          }
          const content = this.input
          const option = this.option
          const audio = this.audioBlob
          const audioWave = this.audioWave
          
          if (content) {
            console.log('content', content)
            this.$emit('submit', {content, user: 1})
            this.input = ''

            postMsg({ content, option }).then(data => {
                this.$emit('submit', {content: data.message, user: 0, fake_html: data.html || ''})
            })
          } else if (audio) {
            this.$emit('submit', {audio: audioWave, user: 1, content: ''})
            this.loading = true
            uploadAudio({ audio }).then(data => {
                console.log('uploadAudio success', data)
                this.loading = false
                this.audioBlob = null
                this.$emit('submit', {content: data.message, user: 0})
            })
          } else {
              console.log('No any input content or audio data')
          }
          
      },
      changeOpt (option) {
          this.option = option
          let welcomemesg = ''
          if (option === 0) {
               welcomemesg = 'Now you can ask me some questions about covid.'
               this.$emit('submit', {content: welcomemesg, user: 0})
          } else if (option === 1) {
              welcomemesg = 'Please paste the news and I will tell you whether it is real.'
              this.$emit('submit', {content: welcomemesg, user: 0})
          } else {
              welcomemesg = 'Now try to record your cough audio and have a covid test. Click to start and click to stop.'
              this.$emit('submit', {content: welcomemesg, user: 0})
              // TODO the audio initialization

          }
          
      },
      clickHandler () {
          if (this.loading) {
              return
          }
          this.recordClickHandler()
      }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.input-container {
    position: relative;
    background: #abdbda;
    padding: 20px;
}
.option-label {
    background: white;
    text-align: left;
    font-size: 12px;
    padding: 5px;
    border-radius: 3px;
}
.option-label.active-opt {
    background: #66b1ff;
    color: white;
}
.send-box {
    display: flex;
}
.send-options {
    text-align: left;
}
.record-btn {
    flex: 1;
}
.red-btn, .red-btn.el-button:focus, .red-btn.el-button:hover {
    color: white;
    background: #cd8080;
}
</style>
