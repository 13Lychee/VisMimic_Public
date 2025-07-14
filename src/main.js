import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// 导入 Font Awesome
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { far } from '@fortawesome/free-regular-svg-icons';
import '@fortawesome/fontawesome-free/css/all.min.css';

// 导入字体
import 'typeface-inter'; // 导入 Inter 字体

library.add(far); // 导入 Font Awesome 图标

// 全局注册 FontAwesomeIcon 组件
// app.component('font-awesome-icon', FontAwesomeIcon);

createApp(App).use(router).component('font-awesome-icon', FontAwesomeIcon).mount('#app')

// createApp(App).use(router).mount('#app')