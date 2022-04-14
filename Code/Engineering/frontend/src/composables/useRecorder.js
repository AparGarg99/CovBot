import { ref } from 'vue'
import Recorder from 'js-audio-recorder';

export default function useRecorder() {
  const recorder = new Recorder({
    sampleBits: 16,                 // 采样位数，支持 8 或 16，默认是16
    sampleRate: 16000,              // 采样率，支持 11025、16000、22050、24000、44100、48000，根据浏览器默认值，我的chrome是48000
    numChannels: 1,                 // 声道，支持 1 或 2， 默认是1
  })

  window.recorder = recorder
  window.datatimer = null
  
  const recording = ref(false)
  const audioBlob = ref()
  const audioWave = ref()
  

  const getDataArray = () => {
    console.log('start getDataArray!')
    window.datatimer = setInterval(() => {
      const wave = recorder.getRecordAnalyseData()
      // const threshold = 10
      // const ifEffective = !! wave.filter(data => (data - 128 > threshold || 128 - data > threshold)).length
      // console.log('getting wave data', ifEffective, wave)

      const current = audioWave._rawValue || []
      const newWave = [...current, ...wave] // 这么写不太好，应该用reactive来达到响应式
      audioWave.value = newWave

      // if (ifEffective) {
      //   console.log('start getDataArray!')
      // }
    }, 200)
  }
  
  const recordClickHandler = () => {
    const old = recording.value
    print('!!! recordClickHandler', old)
    if (!old) { // if not recording, click to start record

      recorder.start().then(() => {
        // scuessfully start to record
        console.log('===>[Recorder start successfully]')
      }, (error) => {
        // start error
        console.log(`===>[Recorder start error] ${error.name} : ${error.message}`)
      });
      getDataArray();
    } else {
      setTimeout(() => {
        recorder.stop();
        clearInterval(window.datatimer)
        audioBlob.value = recorder.getWAVBlob()
      }, 0)
    }
    recording.value = !old
  }

//   onMounted(getUserRepositories)
//   watch(user, getUserRepositories)

  return {
    recording,
    audioBlob,
    audioWave,
    recordClickHandler
  }
}