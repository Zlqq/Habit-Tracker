<template>
    <div id="login">
        <div class="login-wrap">
            <!-- 头像的开头 -->
            <div class="demo-type" >           
                  <el-avatar shape="circle" :size="70" fit="cover" :src = circleUrl ></el-avatar>
            </div>
            <!-- 表单的开头 -->
            <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" class="login-form">
                <!-- 邮箱号 -->
                <el-form-item prop="username" class="item-form">
                    <el-input type="text" v-model="ruleForm.username" autocomplete="off" placeholder="请输入邮箱账号"></el-input>
                </el-form-item>
                <!-- 密码 -->
                <el-form-item prop="password" class="item-form">
                    <el-input type="password"
                     v-model="ruleForm.password" 
                     autocomplete="off" 
                     placeholder="密码" 
                     minlength="6" maxlength="20"></el-input>
                </el-form-item>
                <!-- 提交按钮 -->
                <el-form-item>
                    <el-button type="primary" @click="submitForm('ruleForm')" class="block">登录</el-button>
                </el-form-item>
                <!-- 去注册、去找回密码 -->
                <div class="end">
                  <div class="signup"><router-link to="/register">注册账号</router-link></div>
                  <div class="findps"><router-link to="/findps">忘记密码？</router-link></div>
                </div>
                    
            </el-form>
            <!-- 表单的结尾 -->
        </div>
    </div>
</template>
<script>
import Vue from 'vue';
import { stripscript, validatePass, validateEmail } from '../utils/validate.js';
import { signIn } from '../utils/api.js';
import { ref, reactive, onMounted } from '@vue/composition-api'; 
export default {
    name:"login",
    setup(props, context){
    // 放置data数据，生命周期，自定义的函数
    /*****************************************************************************************************
     * 1. 声明data
     */
    const circleUrl = ref("https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png");
    const ruleForm = reactive({
      username: '',
      password: '',
    });
    // 验证用户名
    let validateUsername = (rule, value, callback) => {
        if (value === '') {
          callback(new Error("请输入邮箱账号"));
        } else if(validateEmail(value)){
          callback(new Error("邮箱格式有误"));
        } else {
          callback();//如果验证无误输出true
        }
      };
    // 验证密码
    let validatePassword = (rule, value, callback) => {
        // 过滤特殊字符
        ruleForm.password = stripscript(value)
        value = ruleForm.password
        let reg = /^(?!\D+$)(?![^a-zA-Z]+$)\S{6,20}$/
        if (value === '') {
          callback(new Error("请输入密码"));
        } else if (validatePass(value)) {
          callback(new Error("密码为6至20位数字+字母"));
        } else {
          callback();
        }
      };
    // 验证三个文本框的有效性；blur表示失去焦点时候触发例如“validatePass”的规则
    const rules = reactive({
          username: [
            { validator: validateUsername, trigger: 'blur' }
          ],
          password: [
            { validator: validatePassword, trigger: 'blur' }
          ]
    });
    /********************************************************************************************************
     * 2. 声明函数
     */
    //(1) 提交表单
    const submitForm = (formName =>{
          context.refs[formName].validate((valid) => {
          if (valid) {
            let RequestData = {
                username: ruleForm.username,
                password: ruleForm.password,
            }
            signIn(RequestData).then(response =>{ //*********************************************登录接口
                let data = response.data
                context.root.$message.success(data.message)
                // 前端返回当前用户名的昵称&本地储存
                let frontXm = data.xm
                localStorage.setItem('myPageShow',JSON.stringify('my'));
                localStorage.setItem('xm',JSON.stringify(frontXm));
                //登录成功,页面跳转***************************************************利用query或者param传参
                var that = context.root.$children[0]
                that.$router.push({
                  path: "/my",
                  query:{
                    xm:frontXm
                  }                
              })             
                that.$router.go(0);
            }).catch(error =>{
                console.log(error)
            })
          }else {
              context.root.$message.error("用户名或密码不正确！")
              return false;
          }
        });
    })
    /********************************************************************************************************
     * 3. 把setup装封里的所有数据return出去
     */
    return{
      circleUrl,
      ruleForm,
      rules,
      submitForm
    }
  },
}
</script>
<style scoped>
#login { 
  background-color: whitesmoke;
  width:400px;
  height:500px;
  font-family:sans-serif, Arial, Helvetica;
}
.login-wrap {
  position: relative;
  top: 40px; /*控制高度*/
  width: 320px;
  height: 300px;
  margin: auto;
  /* border: 1px solid red; */
}
.block {
  display: block;
  width: 100%;
}
.demo-type{
  text-align:center; 
  margin-bottom:10px;   /*控制头像高度*/
}
.item-form{
  margin-bottom: 30px;  /*控制input间隙*/
}
.signup{
  text-align: center;
  /* border: 1px solid green; */
  border-right: 1px solid #ccc;
  grid-column-start: 2;
  grid-column-end:3;
}
.findps{
  text-align: center;
  /* border: 1px solid red; */
  grid-column-start: 3;
  grid-column-end:4;
}
.end{
  display: grid;
  /* border: 1px solid black; */
  grid-template-columns: 1fr 1fr 1fr 1fr;
  width: 100%;
  font-size: 70%;
}
</style>



