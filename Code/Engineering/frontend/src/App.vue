<template>
  <!-- <img class="app-logo" alt="Your song logo" src="./assets/banner.jpg"> -->
  <h2>CovBot: A covid assistant for everyone.</h2>
  <ChatContainer />
</template>

<script>
import ChatContainer from './components/ChatContainer.vue'

export default {
  name: 'App',
  components: {
    ChatContainer
  }
}
</script>

<style>
body {
  background: #f6f6f6;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 25px;
  
  position: fixed;
  overflow: hidden;
  width: 100vw;
  height: 100vh;
  left: 0;
}
::-webkit-scrollbar {
    width: 0px !important;
    height: 0px !important;
}
img.app-logo {
    width: 30%;
}
ul,ol {
  margin: 0;
}
</style>
