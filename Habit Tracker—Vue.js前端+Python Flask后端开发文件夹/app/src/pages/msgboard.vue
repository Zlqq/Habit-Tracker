<template>
    <div class="package">
        <div class="top">
            <div @click="back"><i class="el-icon-arrow-left"></i></div>
            <div>意见反馈</div>
        </div>
        <div class="wrap">
            <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" class="ruleForm">
                <el-form-item prop="advice" class="item">
                    <el-input
                    @input="write"
                    type = 'textarea'
                    v-model="ruleForm.advice"
                    autocomplete="off"
                    :rows = '5'
                    placeholder="请输入问题或建议"
                    maxlength = "200"></el-input>
                </el-form-item>
                <div class="sum">{{number}}/<span>200</span></div>

                <el-form-item  prop="contact" class="item">
                    <el-input 
                    v-model="ruleForm.contact"
                    autocomplete="off"
                    placeholder = '请输入联系方式便于我们联系到您'
                    maxlength = "30"></el-input>
                </el-form-item>

                <el-form-item class="item">
                    <el-button type="primary"
                     @click="submitForm('ruleForm')"
                     class="block"
                    >提交反馈</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<script>
import { addAdvice } from '../utils/api.js';
import { stripscript } from '../utils/validate.js';
export default {
    name:"msgboard",
    data() {
       var validateAdvice = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('内容不能为空！'));
        }else {
          callback();
        }
      };
      var validateContact = (rule, value, callback) => {
        this.ruleForm.contact = stripscript(value)
        if (value === '') {
          callback(new Error('请输入您的联系方式！'));
        } else {
          callback();
        }
      };
      return {
        number:'0',
        ruleForm: {
          advice: '',
          contact: '',
        },
        rules: {
          advice: [
            { validator: validateAdvice, trigger: 'blur' }
          ],
          contact: [
            { validator: validateContact, trigger: 'blur' }
          ],
        },
      };
    },
    methods: {
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
             let RequestData = {
                xm: JSON.parse(localStorage.getItem("xm")),
                contact: this.ruleForm.contact,
                advice: this.ruleForm.advice,
                submitTime:this.CurrentDateTime()
            }
            window.console.log(RequestData)
            addAdvice(RequestData).then(response =>{ 
                let data = response.data
                this.$message.success(data.message)            
                this.$router.go(0);
            }).catch(error =>{
                console.log(error)
            })
          } else {
            this.$message.error("请先完成所有题目！")
            return false;
          }
        });
      },
      write(){
          var txtVal = this.ruleForm.advice.length;
          this.number = txtVal
      },
      back(){
          this.$router.go(-1);
      },
      CurrentDateTime() {
        let date = new Date();
        let y = date.getFullYear();
        let MM = date.getMonth() + 1;
        MM = MM < 10 ? "0" + MM : MM;
        let d = date.getDate();
        d = d < 10 ? "0" + d : d;
        let h = date.getHours();
        h = h < 10 ? "0" + h : h;
        let m = date.getMinutes();
        m = m < 10 ? "0" + m : m;
        let s = date.getSeconds();
        s = s < 10 ? "0" + s : s;
        return y + "-" + MM + "-" + d + " " + h + ":" + m + ":" + s;
        }
    }
  }
</script>
<style scoped>
.package{
    background-color: whitesmoke;
    width:400px;
    height:500px;
}
.top{
    border-bottom:1px solid rgb(225, 225, 225);
    display: grid;
    grid-template-columns: 30% 40% 30%;
    width: 100%;
    height: 40px;
    padding-top: 7px;
}
.top div:nth-child(1){
    padding-left: 5px;
    cursor:pointer;
}
.top div:nth-child(2){
    grid-column: 2/3;
    text-align: center;
    font-weight: 600;
    font-size: 105%;
}
.wrap{
    width: 100%;
}
.block{
    display: block;
    width: 90%;
    margin: auto;
}
.sum{
    position: absolute;
    z-index: 2;
    right: 10px;
    top: 133px;
    font-size: 15px;
    width: 50px;
    text-align: right;
}
.sum span{
    color: grey;
}
</style>

