<template>
    <div id="register">
        <div class="register-wrap">
            <!-- 头像的开头 -->
            <div class="demo-type" >
                <div>
                  <el-avatar shape="circle" :size="70" fit="cover" :src = circleUrl ></el-avatar>
                </div>
            </div>
            <!-- 表单的开头 -->
            <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" class="login-form">
                <!-- 用户的电子邮箱 -->
                <el-form-item prop="username" class="item-form">
                    <el-input type="text" v-model="ruleForm.username" autocomplete="off" placeholder="请输入邮箱账号"></el-input>
                </el-form-item>
                 <!-- 用户的自定义名称 -->
                <el-form-item prop="xm" class="item-form">
                    <el-input type="text" 
                    v-model="ruleForm.xm" 
                    autocomplete="off" 
                    placeholder="用户名"
                    minlength="3" maxlength="8"
                    ></el-input>
                </el-form-item>
                <!-- 新密码 -->
                <el-form-item prop="password" class="item-form">
                    <el-input type="password"
                     v-model="ruleForm.password" 
                     autocomplete="off" 
                     placeholder="设置密码" 
                     minlength="6" maxlength="20"></el-input>
                </el-form-item>
                <!-- 二次密码确认 -->
                <el-form-item prop="passwords" class="item-form" v-show = PsButtonStatus>
                    <el-input type="password"
                     v-model="ruleForm.passwords" 
                     autocomplete="off" 
                     placeholder="重复密码" 
                     minlength="6" maxlength="20"   
                     ></el-input>
                </el-form-item>
                <!-- 获取验证码 -->
                <el-form-item prop="code" class="item-form">
                    <el-row :gutter="20">
                        <el-col :span="15">
                            <el-input v-model="ruleForm.code" placeholder="验证码" minlength="6" maxlength="6"></el-input>
                        </el-col>
                        <el-col :span="9">
                            <el-button type="success" class="block" @click="getSms()" v-bind:disabled = CodeButtonStatus.status>{{CodeButtonStatus.text}}</el-button>
                        </el-col>
                    </el-row>
                </el-form-item>
                <!-- 提交按钮 -->
                <el-form-item id="btn">
                    <el-button type="primary" @click="submitForm('ruleForm')" class="block" v-bind:disabled = RegisterButtonStatus>注册</el-button>
                </el-form-item>
                <div class="signIn"> 已有账号？ <router-link to="/login">点此登录</router-link></div>
            </el-form>
            <!-- 表单的结尾 -->
        </div>
    </div>
</template>
<script>
import { validateEmail,validatePass,validatevCode,validateNm, stripscript } from '../utils/validate.js';
import { GetSms, signUp } from '../utils/api.js';
import { ref, reactive, onMounted } from '@vue/composition-api'; 

export default {
    name:"registerPage",
    setup(props, context){
    /* 
    ** 1. 声明data数据
    */
    // 头像引用地址
    const circleUrl = ref("https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png");
    // 注册按钮禁用状态
    const RegisterButtonStatus = ref(true);
    // 二次密码输入框显示状态
    const PsButtonStatus = ref(false);
    // 获取验证码按钮禁用状态
    const CodeButtonStatus = reactive({
      status: false,
      text:"获取验证码"
    });
    // 倒计时
    const timer = ref(null)
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
    // 验证昵称
    let validateXm = (rule, value, callback) => {
        ruleForm.xm = stripscript(value)
        value = ruleForm.xm
        if (value === '') {
          callback(new Error("请输入用户名"));
        } else if(validateNm(value)){
          callback(new Error("用户名为3至8位有效字符"));
        } else {
          callback();//如果验证无误输出true
        }
    };
    // 验证新密码
    let validatePassword = (rule, value, callback) => {
        // 过滤特殊字符
        ruleForm.password = stripscript(value)
        value = ruleForm.password
        if (value === '') {
          PsButtonStatus.value = false
          ruleForm.passwords = ''
          callback(new Error("请输入密码"));
        } else if (validatePass(value)) {
          PsButtonStatus.value = false
          ruleForm.passwords = ''
          callback(new Error("密码为6至20位数字+字母"));
        } else {
          PsButtonStatus.value = true
          callback();
        }
    };
    // 验证重复密码
    let validatePasswords = (rule, value, callback) => {
        // 过滤特殊字符
        ruleForm.passwords = stripscript(value)
        value = ruleForm.passwords
        if (value === '') {
          callback(new Error("请再次输入密码"));
        } else if (value != ruleForm.password) {
          callback(new Error("重复密码不正确"));
        } else {
          callback();
        }
    };
    // 验证验证码
    let validateCode = (rule, value, callback) => {
        if (value === "") {
          return callback(new Error("请输入验证码"));
        } else if (validatevCode(value)){
          return callback(new Error('验证码格式有误'));
        } else {
            callback();
        }
    };
    const ruleForm = reactive({
        username: '',
        xm:'',
        password: '',
        passwords:'',
        code: '',
    });
    // 验证四个文本框的有效性；blur表示失去焦点时候触发例如“validatePass”的规则
    const rules = reactive({
          username: [
            { validator: validateUsername, trigger: 'blur' }
          ],
          xm: [
            { validator: validateXm, trigger: 'blur' }
          ],
          password: [
            { validator: validatePassword, trigger: 'blur' }
          ],
          passwords: [
            { validator: validatePasswords, trigger: 'blur' }
          ],
          code: [
            { validator: validateCode, trigger: 'blur' }
          ]
    });
    /*************************************************************************************************************
     * 2. 【声明函数】
     */
    /** 
     * (1) 获取验证码
     */
    const getSms =(()=>{
      //前端测试邮箱有效性
      if (ruleForm.username == ''){
        context.root.$message.error("邮箱不能为空，请重试！")
        return false
      }
      if (validateEmail(ruleForm.username)){
        context.root.$message.error("邮箱格式有误，请重新输入！")
        return false
      }      
        // 改变验证码按钮状态
        CodeButtonStatus.status = true
        CodeButtonStatus.text = "发送中"
        // 定义请求数据
        let requestData = { 
          username:ruleForm.username
        }; 

        // 定时器、禁用验证码按钮【调用了myApis定义的接口】
        setTimeout(() =>{
            GetSms(requestData).then( response =>{   //服务器请求成功 获取验证码接口*******************获取验证码接口
              let data = response.data
              context.root.$message.success(data.message)  
              RegisterButtonStatus.value = false  //开放登录按钮
              countDown(30)  //启用计时器
              console.log(data)
            }).catch(error =>{  //服务器请求如果不成功
              CodeButtonStatus.status = false
              CodeButtonStatus.text = "再次获取"
              console.log(error)
            })
        },2000)
    });
    
    // (2) 提交表单
    const submitForm = (formName =>{
      context.refs[formName].validate((valid) => {
        if (valid) { //如果表单验证通过了做什么***********************************************************
          let RequestData = {
            username: ruleForm.username,
            xm: ruleForm.xm,
            password: ruleForm.password,
            code:ruleForm.code
          }
          console.log(RequestData)
          signUp(RequestData).then(response =>{  // 注册接口*********************************************注册接口
            let data = response.data
            context.root.$message.success(data.message)
            console.log(data)
            var that = context.root.$children[0]
            that.$router.push({
              path: "/login"
            })
          }).catch(error =>{
            console.log(error)
          })
        } else { //如果表单验证错误做什么******************************************************************
          context.root.$message.error("用户信息输入有误，请检查并重试！");
          return false;
        }
      })
    });
    // (3) 计时器
    const countDown = ((number) =>{
      //判断定时器是否存在，存在则清除
      if (timer.value) {clearInterval(timer.value);}
      //60和0不见了，bug
      let time = number
      timer.value = setInterval(() =>{
        time--;
        if (time === 0 ){
           clearInterval(timer.value)
           CodeButtonStatus.text = "再次获取"
           CodeButtonStatus.status = false
        }else{
          CodeButtonStatus.text = `${time}s`
        }
      },1000)
    });
    /*******************************************************************************************************
     * 3. 【把setup里面所需的对象return出去】
     */
    return{
      circleUrl,
      RegisterButtonStatus,
      CodeButtonStatus,
      PsButtonStatus,
      timer,
      ruleForm,
      rules,
      getSms,
      submitForm,
      countDown,
    }
  },
}
</script>
<style scoped>
#register { 
  background-color: whitesmoke;
  width:400px;
  height:500px;
  font-family: sans-serif, Arial, Helvetica;
}
.register-wrap {
  position: relative;
  top: 40px;  /*控制高度*/
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
  margin-bottom:10px; /*头像高度*/
}
.item-form{
  margin-bottom: 20px;  /*控制间隙*/
}
.signIn{
  position: relative;
  top: -10px;
  text-align: center;
  font-size: 60%;
}
</style>
