<template>
  <div class="app-container">
    <div class="column1">
      <div class="header-container">
        <Title></Title>
      </div>
      <div class="mediaview">
        <MediaView></MediaView>
      </div>
      <div class="assessmentview">
        <AssessmentView></AssessmentView>
      </div>
    </div>

    <div class="column2">
      <ExplorationView></ExplorationView>
      <CorrectionView></CorrectionView>
    </div>
  </div>
  <!-- <Title></Title> -->
  <!-- <nav>
    <router-link to="/">Home</router-link> |
    <router-link to="/about">About</router-link>
  </nav>
  <router-view/> -->
</template>

<script>
import Title from './components/Title.vue';
import MediaView from './components/MediaView.vue';
import AssessmentView from './components/AssessmentView.vue';
import ExplorationView from './components/ExplorationView.vue';
import CorrectionView from './components/CorrectionView.vue';

export default {
  name: 'App',
  components: {
    Title,
    MediaView,
    AssessmentView,
    ExplorationView,
    CorrectionView,
  },
}
</script>

<style>
#app {
  font-family: 'Inter', Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;

  width: 100%;
  height: 100%;

  /* max-height: 100%; */
}

/* 1920*1080 */
.app-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  gap: 10px;
  padding: 10px 10px;
  background-color: #EAEBEC;
  box-sizing: border-box;
}

.column1 {
  /* 345*1064 */
  width: 18%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  /* overflow: hidden; */
  gap: 5px;
}

.header-container {
  /* width: 22%; */
  width: 100%;
}

.mediaview {
  /* width: 22%; */
  width: 100%;
}

.assessmentview {
  /* width: 22%; */
  width: 100%;
}

.column2 {
  /* 1160*1073 -> 1554*1073 */
  /* width: 60.4%; */
  width: 80.9%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  gap: 5px;
  /* box-sizing: border-box; */
}

/* nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
} */
</style>
