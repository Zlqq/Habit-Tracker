<template>
  <div id="dtvisual">
    <div class="kinds" id="visual">
      
    </div>
<vue-slider ref='dateslider' v-model="dateEnd" :data="dateList" :enable-cross="false" :clickable='false' :contained='true' :lazy="true" @drag-end='updateSlider'></vue-slider>
    <div class="kinds" id="inputAttr">
      <div class="details" v-for="(attribute, i) in attributes" :key="i">
        
        
        <!-- <input type="text" width="200p"> -->
        <el-form :model="ruleForm" :rules="rules" ref="ruleForm" class="add-form">
            <span class="name">
          <label>{{attribute}}:</label>
            </span>
            <span class="dec"></span>
            <el-form-item prop="standard" class="item-form">
                    <el-input type="text" v-model.number="ruleForm.standard" autocomplete="off" placeholder="今日成就"></el-input>
            </el-form-item>
            
            <el-form-item>
                <el-button type="primary" @click="submitForm('ruleForm')" class="block">确认</el-button>
            </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>
<script>
import { GetSms, inputDetail, addrecord } from "../utils/api.js";
import { ref, reactive, onMounted } from '@vue/composition-api'; 
import ElementUI from 'element-ui';

import 'element-ui/lib/theme-chalk/index.css';
import echarts from "echarts";
import axios from "axios";
import Vue from "vue";
import vueSlider from 'vue-slider-component';
import 'vue-slider-component/theme/default.css'
export default {
  name: "visual",
  components: {
    vueSlider
  },

  data() {
      var checkStandard = (rule, value, callback) => {
        if (!value) {
          return callback(new Error('此项不能为空'));
        }
        setTimeout(() => {
          if (!Number.isInteger(value)) {
            callback(new Error('请输入数值'));
          } else {
              callback();
            }
        }, 1000);
      };
    return {
      dateMax:'',
      dateEnd:[],
      dateList:[],
      X:[],
      Y:[],
      object_number:0,
      Habitname: "",
      attributes: [],
      dates: [],
      indexes: [],
      currentdate:'',
      branch: "height",
      
      options: {
        title: {
          text: "Curve of Index",
          left: "50%",
          top:'5%',
          textAlign: "center"
        },
        tooltip: {},
        legend: {
          data: ["Index"]
        },
        xAxis: [
            {
          type: 'category',
          data: [2,3,4,5]
            }
        ],
        yAxis: {},
        series: [
          {
            name: "Run time",
            type: "line",
            data: [2,3,4,5,]
          }
        ]
      },
      habit: [],
      ruleForm:{
          standard:'',
      },
      rules:{
           standard: [
            { validator: checkStandard, trigger: 'blur' }
          ]
      }
    };
  }, 
  methods: {
      updateSlider() {
       
        
        var that = this
        let requestData = {
                username:localStorage.getItem('xm'),
                title:that.habit.title,
                
            }
            inputDetail(requestData).then(function(res) {
        let Xdata = res.data.result[1];
        let Ydata = res.data.result[0];
        let XList = [];
        let YList = [];
        
        for(var i = 0;i<Xdata.length;i++){
          if (parseInt(Xdata[i])>=parseInt(that.dateEnd[0]) && parseInt(Xdata[i])<=parseInt(that.dateEnd[1])){
            XList.push(Xdata[i])
            YList.push(Ydata[i])
          }

        }
      
        that.options['xAxis'][0]['data'] = XList
        that.options['series'][0]['data'] = YList
        // console.log(that.options['xAxis'][0]['data'])
let mychart = that.$echarts.init(document.getElementById("visual"));
    mychart.setOption(that.options);
    }); 
        
      },
      submitForm(formName) {
        // this.$refs.formName.validate((valid) => {
        //   if (valid) {
        //     alert('submit!');
        //     console.log("hi")
        //   } else {
        //     console.log('error submit!!');
        //     return false;
        //   }
        // });
        
        if (!Number.isInteger(this.ruleForm['standard'])) {
            this.$message.error("请输入数字！")
          } else {
            this.dateEnd=[]
              let RequestData = {
            title: this.habit.title,
            standard: this.ruleForm['standard'],
            date: this.currentdate,
            username:localStorage.getItem('xm'),
            attr:this.attributes,
            object_number:this.object_number
          }
          console.log(RequestData)
          var that = this
          addrecord(RequestData).then(response =>{
            let requestData2 = {
                username:localStorage.getItem('xm'),
                title:that.habit.title,
            }
            inputDetail(requestData2).then(function(res) {
        let Xdata = res.data.result[1];
        let Ydata = res.data.result[0];
        that.dateEnd = [];
        if(Xdata.length>=2){
          that.dateEnd.push(Xdata[0])
        that.dateEnd.push(Xdata[Xdata.length-1])
        
        }else{
          that.dateEnd = []
        }
        that.options['xAxis'][0]['data'] = Xdata
        that.options['series'][0]['data'] = Ydata
        
let mychart = that.$echarts.init(document.getElementById("visual"));
    mychart.setOption(that.options);
    
    });  
            that.$router.push({
              path: "/visual"
            })
            that.ruleForm['standard'] = ''
          }).catch(error =>{
            console.log(error)
          })
            }
        
      },
     
    },
  created() {
    this.habit = this.$route.query.habit;
    //从zx的页面拿到attr后期需要修改
    this.attributes.push(this.habit.habit_object);
    this.options["title"]["text"] = this.habit.title;
    this.object_number = this.habit.object_number
    
    //调取my页面的全局变量username
    let requestData = {
      username: localStorage.getItem('xm'),
      title: this.habit.title,
    };
    var that = this;
    inputDetail(requestData).then(function(res) {
        let Xdata = res.data.result[1];
        let Ydata = res.data.result[0];
        that.options['xAxis'][0]['data'] = Xdata
        that.options['series'][0]['data'] = Ydata
        that.dateList = Xdata
        if(Xdata.length>=2){
          that.dateEnd.push(Xdata[0])
        that.dateEnd.push(Xdata[Xdata.length-1])
        
        }else{
          that.dateEnd = []
        }
       
        
let mychart = that.$echarts.init(document.getElementById("visual"));
    mychart.setOption(that.options);
    });
  },
  mounted(){
    
   
    
    //获取当前日期
    var date = new Date();
    var year = date.getFullYear();
    var month = date.getMonth() + 1;
    var strDate = date.getDate();
    if (month >= 1 && month <= 9) {
      month = "0" + month;
    }
    if (strDate >= 0 && strDate <= 9) {
      strDate = "0" + strDate;
    }
    this.currentdate = year + month + strDate;
    
  }
  // mounted(){
  //    var that = this;
  //     console.log(this.branch)
  //   axios
  //      .get("/team_data", {
  //          params:{
  //              choose2:that.branch
  //          }

  //       })
  //       .then(function(response) {
  //         // that.multiselect_options = response.data.teams;
  //         vegaEmbed("#visual", response.data.figure, { mode: "vega-lite" })
  //       });
  //  }
};
</script>
<style scoped>

#dtvisual {
  text-align: center;
  width: 400px;
  position: relative;
  margin: auto;
  height: 550px;
  font-size: 100%;
  cursor: default;
  font-family: Arial, Helvetica, sans-serif;
}

#visual {
  height: 255px;
  
}
#inputAttr {
  height: 255px;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-box-pack: center;
  -webkit-box-align: center;

  display: -moz-box;
  -moz-box-orient: vertical;
  -moz-box-pack: center;
  -moz-box-align: center;

  display: -o-box;
  -o-box-orient: vertical;
  -o-box-pack: center;
  -o-box-align: center;

  display: -ms-box;
  -ms-box-orient: vertical;
  -ms-box-pack: center;
  -ms-box-align: center;

  display: box;
  box-orient: vertical;
  box-pack: center;
  box-align: center;
}
div.details {
  margin-top: 40px;
}
/* .dec{
        margin-left:20px;
        margin-right:20px;
    } */
input {
  border-radius: 6px;
  border: 1px solid black;
  height: 25px;
  margin-right: 20px;
}
span.name {
  display: block;
  text-align: left;
  height: 25px;
  float: left;
  width: 100px;
}
span.dec {
  margin-left: 20px;
  margin-right: 20px;
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

