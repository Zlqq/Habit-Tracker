<template>
    <div id="findps">
        <div class="findps-wrap">
            <div id="title">重置密码</div>
            <!-- 表单的开头 -->
            <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" class="demo-ruleForm">
                <!-- 邮箱账号 -->
                <el-form-item prop="username" class="item-form">
                    <el-input 
                    type='text'
                    v-model="ruleForm.username" 
                    autocomplete="off"
                    placeholder="请输入邮箱账号"></el-input>
                </el-form-item>
                <!-- 新密码 -->
                <el-form-item prop="password" class="item-form">
                    <el-input 
                     type="password"
                     v-model="ruleForm.password" 
                     autocomplete="off" 
                     placeholder="新密码" 
                     minlength="6" maxlength="20"></el-input>
                </el-form-item>
                <!-- 二次密码 -->
                <el-form-item prop="passwords" class="item-form" v-show = PsButtonStatus>
                    <el-input 
                     type="password"
                     v-model="ruleForm.passwords" 
                     autocomplete="off" 
                     placeholder="再次输入密码" 
                     minlength="6" maxlength="20"></el-input>
                </el-form-item>
                <!-- 验证码和按钮 -->
                <el-form-item prop="code" class="item-form">
                    <el-row :gutter="20">
                        <el-col :span="15">
                            <el-input
                            v-model="ruleForm.code"
                            placeholder="验证码"
                            minlength="6" maxlength="6"></el-input>
                        </el-col>
                        <el-col :span="9">
                            <el-button type="success" class="block" @click="getSms()" 
                            v-bind:disabled = CodeButtonStatus.status>{{CodeButtonStatus.text}}</el-button>
                        </el-col>
                    </el-row>
                </el-form-item>
                <!-- 重置按钮 -->
                <el-form-item>
                    <el-button type="primary" @click="submitForm('ruleForm')" class='block'
                    v-bind:disabled = ResetButtonStatus>确定</el-button>
                </el-form-item>
            </el-form>
            <!-- 表单的结尾 -->
            <div class="end">
                  <div class="signin"><router-link to="/login">返回登录</router-link></div>
                  <div class="signup"><router-link to="/register">前往注册>></router-link></div>
            </div>
        </div>
    </div>
</template>

<script>
import { validateEmail,validatePass,validatevCode,stripscript } from '../utils/validate.js';
import { ref, reactive, onMounted } from '@vue/composition-api'; 
import { GetSms, findPs } from '../utils/api.js';
export default {
    name:"findps",
    setup(props, context){
    // 二次密码输入框显示状态
    const PsButtonStatus = ref(false);
    // 重置按钮禁用状态
    const ResetButtonStatus = ref(true);
    // 获取验证码按钮文本
    const CodeButtonStatus = reactive({
      status: false,
      text:"获取验证码"
    });
    // 验证邮箱账号
    let validateUsername = (rule, value, callback) => {
        if (value === '') {
          callback(new Error("请输入邮箱账号"));
        } else if(validateEmail(value)){
          callback(new Error("邮箱格式有误"));
        } else {
          callback();
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
        password: '',
        passwords:'',
        code: '',
    });
    // 验证四个文本框的有效性
    const rules = reactive({
          username: [
            { validator: validateUsername, trigger: 'blur' }
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
    //*******************************************************************
    // 1. 获取验证码
    const getSms =(()=>{
      // 前端测试邮箱有效性
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
        setTimeout(() =>{
            GetSms(requestData).then( response =>{   //获取验证码服务器请求成功*************************
              let data = response.data
              context.root.$message.success(data.message)  
              ResetButtonStatus.value = false  //开放重置密码按钮
              countDown(30)  //启用计时器
            }).catch(error =>{  //服务器请求如果不成功
              CodeButtonStatus.status = false
              CodeButtonStatus.text = "再次获取"
              console.log(error)
            })
        },2000)
    });
    // 2. 提交表单
    const submitForm = (formName =>{
      context.refs[formName].validate((valid) => {
        if (valid) { //如果表单验证通过了做什么***********************************************************
          let RequestData = {
            username: ruleForm.username,
            password: ruleForm.password,
            code:ruleForm.code
          }
          console.log(RequestData)
          findPs(RequestData).then(response =>{  // 注册接口*********************************************注册接口
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
    // 倒计时
    const timer = ref(null)
    //3. 计时器
    const countDown = ((number) =>{
      //判断定时器是否存在，存在则清除
      if (timer.value) {clearInterval(timer.value);}
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
    return{
        rules,
        ruleForm,
        PsButtonStatus,
        submitForm,
        CodeButtonStatus,
        ResetButtonStatus,
        countDown,
        getSms,
        timer
    }
  },
}
</script>
<style scoped>
#findps{
  background-color: whitesmoke;
  width:400px;
  height:500px;
}
.findps-wrap {
  position: relative;
  top: 50px; /*控制高度*/
  width: 320px;
  height: 400px;
  margin: auto;
  /* border: 1px solid red; */
  text-align: center;
}
.block {
    display: block;
    width: 100%;
}
.login{
  position: relative;
  top: -15px;
  text-align: right;
  font-size: 60%;
  font-family:  Arial, Helvetica;
}
#title{
   /* border: 1px solid red; */
   height: 76px;
   font-size: 21px;
   font-weight: 500;
   font-family: "微软雅黑",Arial, Helvetica, sans-serif;
   text-align: center;
   color: #666666;
   padding-top: 15px;
}
.signin{
  text-align: center;
  /* border: 1px solid green; */
  border-right: 1px solid #ccc;
  grid-column-start: 2;
  grid-column-end:3;
}
.signup{
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
