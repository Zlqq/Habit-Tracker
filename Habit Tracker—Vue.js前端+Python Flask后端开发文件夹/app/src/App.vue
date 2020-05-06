<template>
  <div id="app">
    <div id="all"> 
      <div class="calender" ><router-view></router-view></div>
      <div class="tarbar">
        <!-- 第一个home键 -->
        <div class="home"><router-link to="/" style="text-decoration:none;color:black">
          <i class="el-icon-s-home" :style = bgcolor.home @click = "changeHome"></i></router-link >
        </div>
        <div class='homes' :style = bgcolor.home>主页</div>
        <!-- 第二个my键 -->
        <div class="my"> 
          <router-link :to = target style="text-decoration:none;color:black">
          <i class="el-icon-s-custom" :style = bgcolor.my @click= "changeMy"></i></router-link>
        </div>
        <div class="mys" :style = bgcolor.my>我的</div>
      </div>
    </div>
  </div>
</template>

<script>
import echarts from "echarts";
import Vue from "vue";
import VueRouter from "vue-router";
import 'bootstrap/dist/css/bootstrap.min.css'
import Mycalender from './pages/calender.vue';  //sammy1
import Addhabit from "./pages/details.vue";  //sammy2
import all from "./pages/all.vue";  //sammy3
import visual from './pages/visual.vue';
import login from './pages/login.vue';  //cassie1
import register from './pages/register.vue'; //cassie2
import my from './pages/my.vue'; //cassie3
import findps from './pages/findps.vue'; //cassie4
import msgboard from './pages/msgboard.vue' //cassie5
Vue.use(VueRouter);

var router = new VueRouter({
  routes: [
    // { path: "/", redirect:"login"},
    { path: "/", component: Mycalender },
    { path: "/details", component: Addhabit },
    { path: "/all", component: all },
    { path: "/visual",component:visual},
    { path: "/login", component: login, name:'login' },  //cassie1
    { path: "/register",component:register}, //cassie2
    { path: "/my", component:my,name:'my'}, //cassie3
    { path: "/findps", component:findps,name:'findps'}, //cassie4
    { path: "/msgboard", component:msgboard,name:'msgboard'}, //cassie5
  ]
});

export default  {
  name: 'app',
  router:router,
  data(){
    return{
      target:{
        name:"",
        query:{},
      },
      bgcolor:{
        home: "color:black;" ,
        my: "color:black;" 
      }
    }
  },
  methods:{
    initials(){
    var myPageShow = JSON.parse(localStorage.getItem("myPageShow"))
    var myXm = JSON.parse(localStorage.getItem("xm"))
    if (!myPageShow && !myXm){
      this.target.name = 'login'
      this.target.query = {}
      }
    else{
      this.target.name = myPageShow
      this.target.query = {xm:myXm}
    }
   },
   changeMy(){
    this.bgcolor.my = "color:#1989fa;"
    this.bgcolor.home = "color:black;" 
   },
   changeHome(){
    this.bgcolor.my = "color:black;"
    this.bgcolor.home = "color:#1989fa;"
   }
  },
  mounted(){
    this.initials();
  }
}
</script>
<style>
#all{
  position:relative;
  width:400px;
  height:550px;
  margin:auto;
  display:grid;
  grid-template-columns:200px 200px;
  border: 1px solid rgb(75,75,75,.25);
	/* box-shadow: 0 0 15px 5px rgb(44,82,100,.50); */
  overflow: hidden;
}
.tarbar{
  position: absolute;
  z-index:2;
  bottom: 0;
  height:50px;
  width:400px;
  border-top:1px solid rgb(225, 225, 225);
  display: grid;
  grid-template-columns:200px 200px;
  grid-template-rows:30px 20px;
}
.home,.my{
  text-align: center;
  font-size: 180%;
}
.homes,.mys{
  text-align: center;
  font-size: 12px;
}
.my{
  grid-column:2/3;
  grid-row:1/2;
}
.el-icon-s-custom,.el-icon-s-home{
  position: absolute;
  top: 5px;
  width:50%;
}
.el-icon-s-custom{
  right: 0;
}
.el-icon-s-home{
  left: 0;
}
</style>