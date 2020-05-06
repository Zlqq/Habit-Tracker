// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
//引入Element-UI
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
// 引入api
import VueCompositionApi from '@vue/composition-api'; 
Vue.use(ElementUI);
Vue.use(VueCompositionApi);
import App from './App'
import echarts from 'echarts'
Vue.config.productionTip = false;
Vue.prototype.$echarts = echarts
new Vue({
  render: h => h(App),
}).$mount('#app')

