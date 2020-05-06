<template>
    <div class="new">
        <div class="add-wrap">
            <el-form :model="ruleForm" :rules="rules" ref="ruleForm" class="add-form">
            <el-form-item prop="title" class="item-form">
                    <el-input type="text" v-model="ruleForm.title" autocomplete="off" placeholder="请输入新习惯"></el-input>
            </el-form-item>
            <el-form-item prop="object" class="item-form">
                    <el-input type="text" v-model="ruleForm.object" autocomplete="off" placeholder="目标属性，例：步数" style="width:55%"></el-input>
            </el-form-item>
            <el-form-item prop="number" class="item-form" style="width:40%;margin-left:192px;margin-top:-60px;">
                     <el-input type="text" v-model="ruleForm.number" autocomplete="off" placeholder="目标，例：300" ></el-input>
            </el-form-item>
            <el-form-item prop="datetime" class="item-form" style="margin-top:-8px;">
                    <span style="font-size:15px;">请选择习惯开始的时间</span>
                    <el-input type="date" v-model="ruleForm.datetime" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="submitForm('ruleForm')" class="block">确定</el-button>
            </el-form-item>
        </el-form>
    </div>
    </div>
</template>
<script>
    import { GetSms, addHabit } from '../utils/api.js';
    import { ref, reactive, onMounted } from '@vue/composition-api'; 
    import Vue from "vue";

export default {
    name:'Addhabit',
    setup(props, context){
        //验证标题
    let validateTitle = (rule, value, callback) => {
        let reg = /^[\u4E00-\u9FA5A-Za-z]/;
        ruleForm.title = stripscript(value)
        value = ruleForm.title
        if (value === '') {
          callback(new Error("该项不能为空"));
        } else if(!reg.test(value)){
          callback(new Error("不可输入数字"));
        }else {
          callback();//如果验证无误输出true
        }
    };
    let validateObject = (rule, value, callback) => {
        let reg = /^[\u4E00-\u9FA5A-Za-z]/;
        ruleForm.object = stripscript(value)
        value = ruleForm.object
        if (value === '') {
          callback(new Error("该项不能为空"));
        } else if(!reg.test(value)){
          callback(new Error("不可输入数字"));
        }else {
          callback();//如果验证无误输出true
        }
    };
        let validateNumber = (rule, value, callback) => {
        let reg = /^[0-9]/;
        ruleForm.number = stripscript(value)
        value = ruleForm.number
        if (value === '') {
          callback(new Error("该项不能为空"));
        } else if(!reg.test(value)){
          callback(new Error("只可输入数字"));
        }else {
          callback();//如果验证无误输出true
        }
    };
    let validateDatetime = (rule, value, callback) => {
        value = parseInt(ruleForm.datetime.substr(0,4) + ruleForm.datetime.substr(5,2) + ruleForm.datetime.substr(8,2))
        var year = new Date().getFullYear().toString()
        var month = new Date().getMonth()+1
        var date = new Date().getDate()
        if(month > 9){
          month = (new Date().getMonth()+1).toString()
        }
        else{
          month = "0" + (new Date().getMonth()+1).toString()
        }
        if(date > 9){
          date = new Date().getDate().toString()
        }
        else{
          date = "0" + new Date().getDate().toString()
        }
        var now_datetime = parseInt(year + month + date)
        if (value === '') {
          callback(new Error("该项不能为空"));
        } else if(value < now_datetime){
          callback(new Error("请选择当天或之后的日期"));//无法选择前一天
        }else {
          callback();//如果验证无误输出true
        }
    };

    const rules = reactive({
          title: [
            { validator: validateTitle, trigger: 'blur' }
          ],
          object: [
            { validator: validateObject, trigger: 'blur' }
          ],
        datetime: [
            { validator: validateDatetime, trigger: 'blur' }
          ],
        number: [
            { validator: validateNumber, trigger: 'blur' }
          ]
    });

    const ruleForm = reactive({
        title:'',
        object: '',
        number:'',
        year: '',
        month:'',
        date: '',
        datetime:''
    });

    const stripscript = (str =>{
        var pattern = new RegExp("[`~!@#$^&*()=|{}':;',\\[\\].<>/?~！@#￥……&*（）&;—|{ }【】‘；：”“'。，、？]")
        var rs = "";
        for (var i = 0; i < str.length; i++) {
                rs = rs + str.substr(i, 1).replace(pattern, '');
        }
        return rs;
    });
    const submitForm = (formName =>{
      context.refs[formName].validate((valid) => {
        if (valid) { //如果表单验证通过了做什么***********************************************************
          let RequestData = {
            username: localStorage.getItem('xm'),
            title: ruleForm.title,
            object: ruleForm.object,
            number:parseInt(ruleForm.number),
            datetime:parseInt(ruleForm.datetime.substr(0,4) + ruleForm.datetime.substr(5,2) + ruleForm.datetime.substr(8,2))
          }
          addHabit(RequestData).then(response =>{
              var that = context.root.$children[0]
              that.$router.push({
              path: "/"
              })
            }).catch(error =>{
              console.log(error)
            })
        }
        else { //如果表单验证错误做什么******************************************************************
          context.root.$message.error("用户信息输入有误，请检查并重试！");
          return false;
        }
      })
    });
    onMounted(()=>{
    });
    return{
      ruleForm,
      rules,
      submitForm,
      stripscript
    }
    }
    }
</script>
<style scoped>
.new{
    background-color: whitesmoke;
    width: 400px;
    height: 500px;
    font-family: Arial, Helvetica, sans-serif;
}
.add-wrap{
    position: relative;
    top: 40px;  /*控制高度*/
    width: 320px;
    height: 300px;
    margin: auto;
}
.block {
    display: block;
    width: 100%;
}
.item-form{
    margin-bottom: 20px;  /*控制间隙*/
}
</style>