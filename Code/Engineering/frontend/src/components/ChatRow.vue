<template>
  <div :class="['row-container', { 'style-right': isRight }]"> 
      <div class="flex-left">
          <div class="avator"></div>
          <div class="username">{{ username }}</div>
      </div>
      <div class="flex-right">
        <div class="content-bg">
            <div class="content" v-if="content">
              {{ content }}
              <el-button type="text" @click="translation">
                <el-icon><DocumentCopy /></el-icon>
              </el-button>
            </div>
            <div class="fake-html" v-if="fakehtml"><span v-html="fakehtml"></span></div>
            <div class="translation" v-if="translatedText">
              {{ translatedText }}
            </div>
            <div class="audio" v-if="!content">
              <span><canvas id="canvas"></canvas>[audio]</span>
            </div>
        </div>
      </div>
  </div>
</template>

<script>
import { translate } from '../api/api'

export default {
  name: 'ChatRow',
  props: {
    isRight: {
      type: Boolean,
      default: false
    },
    username: String,
    content: String,
    audio: Object,
    fakehtml: String
  },
  data() {
    return {
      translatedText: ''
    };
  },
  components: {
    
  },
  mounted () {
    if (this.audio) {
      this.drawAudio()
    }
  },
  methods: {
    translation () {
      const content = this.content
      const lang = 'zh'
      
      if (!content) {
        return
      }

      if (this.translatedText) {
        this.translatedText = ''
        return
      }
      // https://cloud.google.com/translate/docs/basic/translating-text?hl=zh-cn#translate_translate_text-python
      translate({ content, lang }).then(data => {
        console.log('result of translation', data)
        this.translatedText = data.message
      })
    },
    drawAudio () {

      console.log('start drawAudio!!!!')

      let dataArray = this.audio,
        bufferLength = dataArray.length
      
      window.audio = this.audio

      const oCanvas = document.getElementById('canvas')
      const ctx = oCanvas.getContext("2d")

      // 填充背景色
      ctx.fillStyle = 'rgb(256, 256, 256)'
      ctx.fillRect(0, 0, oCanvas.width, oCanvas.height)

      // 设定波形绘制颜色
      ctx.lineWidth = 1
      ctx.strokeStyle = 'rgb(0, 0, 0)'

      ctx.beginPath()

      let sliceWidth = oCanvas.width * 1.0 / bufferLength, // 一个点占多少位置，共有bufferLength个点要绘制
          x = 0         // 绘制点的x轴位置

      for (let i = 0; i < bufferLength; i++) {
          let v = dataArray[i] / 128 // 128.0 // dataArray[i] / 128.0;
          let y = v * oCanvas.height / 2

          if (i === 0) {
              // 第一个点
              ctx.moveTo(x, y)
          } else {
              // 剩余的点
              ctx.lineTo(x, y)
          }
          // 依次平移，绘制所有点
          x += sliceWidth
      }

      ctx.lineTo(oCanvas.width, oCanvas.height / 2)
      ctx.stroke()
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.row-container {
    display: flex;
    justify-content: space-between;
}
.style-right {
    flex-direction: row-reverse;
}
.avator {
    width: 30px;
    height: 30px;
    background: bisque;
    border-radius: 50%;
    margin-top: 10px;
}
.style-right .avator, .style-right .content-bg {
    background: #abdbda;
}
.username {
    font-size: 12px;
}
.flex-left {
    width: 15%;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.flex-right {
    flex: 1;
    position: relative;
}
.content-bg {
    margin: 10px 20px;
    line-height: 30px;
    background: bisque;
    padding: 5px 20px;
    left: 0;
    border-radius: 5px;
}
.content {
    text-align: left;
}
.translation {
  text-align: left;
  font-size: 12px;
  color: #666666;
}
#canvas {
  height: 80px;
  width: 100%;
}
.fake-html {
  text-align: left;
  background: snow;
  font-size: 12px;
  margin-top: 10px;
  padding: 10px;
}
</style>
