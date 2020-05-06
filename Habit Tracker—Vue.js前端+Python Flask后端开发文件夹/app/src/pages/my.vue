<template>
  <div id="my">
      <div class="exit">
        <el-button circle plain icon = "el-icon-switch-button" id="btn" @click="exit" ></el-button>
      </div>
       <div class="avatar">   
          <img src="../assets/1.jpg">
      </div>
      <div class="msg">
          欢迎您！{{xm}}
      </div>
      <div class="wrap">
        <div><img src="../assets/3.png" @click="addHabits"></div><div>创建新习惯</div>
        <div><img src="../assets/4.png" @click="checkAll"></div><div>已归档习惯</div>
        <div><img src="../assets/2.png" @click="download"></div><div>用户手册</div>
        <div><img src="../assets/1.png" @click="addMsg"></div><div>意见反馈</div>
      </div>
  </div>
</template>
<script>
import Vue from 'vue';
import { reactive, ref, isRef, toRefs, onMounted, watch } from '@vue/composition-api';
export default {
  name: 'my',
  data(){
    return{
      xm:this.$route.query.xm,
    }
  },
  methods:{
    addHabits(){
      this.$router.push({
        path: "/details"
     })
    },
    addMsg(){
      this.$router.push({
        path:"/msgboard"
      })
    },
    checkAll(){
       this.$router.push({
        path:"/all"
      })
    },
    download() {
        // window.location.href = "../../static/用户使用手册.docx";
        // window.location.href = "../../static/用户使用手册.pdf";
        // window.open("../../static/用户使用手册.pdf")
        window.open("./static/Help.pdf")
    
    },
    exit(){
       localStorage.removeItem("myPageShow");
       localStorage.removeItem("xm");
       this.$router.push({
         path: "/login"
       }),
       this.$router.go(0)
    },
  },
 mounted(){
   //设置一个全局变量则每个页面都可以拿到当前登陆的用户名
      Vue.prototype.$username = this.xm;
 }
}
</script>
<style scoped>
#my{
  background-color: whitesmoke;
  width:400px;
  height:500px;
  text-align: center;
  font-family:"黑体", "Microsoft YaHei", Arial, Helvetica, sans-serif;
}
.avatar{
  position: relative;
  top:10px;
  margin: auto;
  width: 100px;
  height: 100px;
  overflow: hidden;
  border-radius: 50%;
}
.avatar img{
  width: 100px;
}
.msg{
  position:relative;
  top:20px;
  width:100%;
  height:40px;
  font-size: 1.5em;
}
.exit{
  width:100%;
  height: 50px;
  text-align: right;
}
.btn{
  position: relative;
  top:100px;
  font-family:"Microsoft YaHei", Arial, Helvetica, sans-serif;
}
#btn{
  margin-top: 20px;
  margin-right: 25px;
}
.wrap{
  position: relative;
  margin: auto;
  top: 25px;
  width:300px;
  height: 250px;
  /* border: 1px solid red; */
  display: grid;
  grid-template-columns:50% 50%;
  grid-template-rows:35% 15% 35% 15%;
}
.wrap div{
  /* border: 1px solid red; */
  text-align: center;
}
.wrap div img{
  position: relative;
  margin: auto;
  width: 80px;
  cursor: pointer;
  transition: all 0.5s;
}
.wrap div img:hover{
  transform:scale(1.1);
}
.wrap div:nth-child(3){
 grid-column:2/3;
 grid-row: 1/2;
}
.wrap div:nth-child(7){
   grid-column:2/3;
   grid-row: 3/4;
}
</style>
