<template>
  <div class="calender">
    <div class="top">
      <div class="top_date">
        {{year}}年{{month}}月
      </div>
      <div class="btn_wrap" >
        <ul style="list-style:none;">
          <li @click="handleShowNextMonth" title="下月">下月</li>
          <li @click="handleShowToday" class="today" title="今天">今天</li>
          <li @click="handleShowLastMonth" title="上月">上月</li>
        </ul>
      </div>
    </div>
    <div class="date_wrap">
        <ul class="week" style="list-style:none;">
            <li>周日</li>
            <li>周一</li>
            <li>周二</li>
            <li>周三</li>
            <li>周四</li>
            <li>周五</li>
            <li>周六</li>
        </ul>
        <ul class="day" style="list-style:none;">
          <li v-for="(item,index) in days" :key="index" :class="{now:nowLi==year.toString()+month.toString()+item.date,Colors1:standard[index] =='2',Colors2:standard[index] == '0',bgColors:index == current,change_now1:index == now1,change_now2:index == now2}" @click="show(item,index)" :style="item.style"  >
            <span>{{item.date}}</span>
            <img src="../assets/images/smile.png" :class="{Colors3:standard[index] == '1'}">
          </li>
        </ul>
    </div>
    <div class="habit">
        <ul v-for="(habit,index) in habits" :key="index" style="list-style:none;" class="habitlist">
          <li>
          <button type="button" id="delete" @click="deleteHabit(habit)">-</button>
          <span @click="toVisual(habit)" class="point">{{habit.title}}（{{habit.habit_object}}:{{habit.object_number}}）</span>
          <img src="../assets/images/star.png" id="star" :class="{finishColor:finished[habit.title] == 'true'}">
          </li>
        </ul>
        <button type="button" id="add" class="btn btn-primary btn-lg" @click="toAddhabit()">+</button>
    </div>
    
  </div>
</template>

<script>
  import { GetSms, showHabit,deletehabit,showHabit1,checkDetail,checkDetail1,checkDetail2 } from '../utils/api.js';
  import Vue from "vue";
  export default {
    name: 'calender',
    data () {
      return {
        year:'',
        month:'',
        days:[],
        nowLi:'',
        habits:[],
        current:-1,
        now1:'',
        now2:'',
        title:'',
        datetime:'',
        finished:{},
        finished_total:{},
        standard:[],
        stand:'',
        habit_total:{}
    }
  },
  methods:{
    //控制当前日期显示特殊样式
    handleShowDateStyle(){
      let now = new Date()
      this.nowLi=now.getFullYear().toString()+(now.getMonth()+1).toString()+now.getDate().toString()
      for(let i=0;i<this.standard.length;i++){
        this.stand = ''
        this.stand = this.standard[i]
      }
    },
    //得到当前年这个月分有多少天
    getDays(Y,M){
      let day = new Date(Y, M, 0).getDate()
      return day;
    },
    //得到当前年，这个月的一号是周几
    getWeek(){
        let now = new Date()
        now.setFullYear(this.year)
        now.setMonth(this.month-1)
        now.setDate(1);
        let week = now.getDay();
        return week;
    },
    pushDays(){
            //将这个月多少天加入数组days
            for(let i = 1; i<=this.getDays(this.year,this.month);i++){
              this.days.push({date:i,style:"opacity:1",symbol:"2"})
            }
            //将下个月要显示的天数加入days
            for(let i = 1;i<=35-this.getDays(this.year,this.month)-this.getWeek(this.year,this.month);i++){
              this.days.push({date:i,style:"opacity:0",symbol:"1"})
            }
            //将上个月要显示的天数加入days
            for(let i=0;i<this.getWeek(this.year,this.month);i++){
              var lastMonthDays=this.getDays(this.year,this.month-1)
                this.days.unshift({date:lastMonthDays-i,style:"opacity:0",symbol:"1"})
            }
    },
    //得到当天的日期
    getDate(){
            let now = new Date();
            this.year = now.getFullYear();
            this.month = now.getMonth()+1;
            this.pushDays();        
    },
    //下个月
    handleShowNextMonth(){
       this.days=[];
      if(this.month<12){
        this.month=this.month+1;
         this.pushDays();
      }else{
        this.month= this.month=1;
        this.year=this.year+1;
        this.pushDays();
      }
      if(this.month != new Date().getMonth()+1){
        this.habits = [];
        this.standard = [];
        this.showAll();
      }
      else{
        this.standard = [];
        this.showList();
        this.showFinished();
        this.showAll();
      }
    },
    handleShowToday(){
      this.days=[];
      let now = new Date();
      this.year=now.getFullYear();
      this.month=now.getMonth()+1;
      this.pushDays();
    },
    //上个月
    handleShowLastMonth(){
       this.days=[];
      if(this.month>1){
         this.month=this.month-1;
      this.pushDays();
      }else if( this.year>1970){
        this.month=12;
        this.year=this.year-1;
        this.pushDays();
      }
      else{
        this.$message.error("不能查找更远的日期！")
      }
      if(this.month != new Date().getMonth()+1){
        this.habits = [];
        this.standard = [];
        this.showAll();
        }
      else{
        this.standard = [];
        this.showList();
        this.showFinished();
        this.showAll();
      }
  },
  //获取日期的索引
  getIndex(day){
    for(let i=0;i<this.days.length;i++){
      if(this.days[i].symbol == "2"){
        if(this.days[i].date == day){
          return i
        }
      }
    }
  },
  //获取当天日期
  getnowDate(){
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
      return now_datetime
  },
//获取当前点击时的日期
getnowClickdate(year,month,date){
      var now_year = ''
      var now_month = ''
      var now_date = ''
      now_year = year
      if(month > 9){
        now_month = month
      }
      else{
        now_month = "0" + month
      }
      if(date > 9){
        now_date =  date
      }
      else{
          now_date = "0" + date
      }
      var now_date = parseInt(now_year + now_month + now_date)
      return now_date
},
  //显示习惯
  show(item,index){
      let requestData = {
        username:localStorage.getItem('xm'),
        year:this.year,
        month:this.month,
        date:item.date
      }
      var that = this
      showHabit(requestData).then(function(res){
        let data = res.data.result
        var habit = []
        that.habits = []
        var now_date = that.getnowClickdate(that.year,that.month,item.date)
        for(let i = 0;i < data.length;i++){
              var habit_data = []
              habit_data = data[i]
              that.habits.push({title:habit_data[2],habit_object:habit_data[3],object_number:habit_data[4],datetime:now_date})
        }
      })
      //显示习惯的完成情况
      let requestData2 = {
        username:localStorage.getItem('xm'),
        datetime:this.getnowClickdate(this.year,this.month,item.date)
      }
      var that = this
      checkDetail(requestData2).then(function(res){
        let data = res.data.result
        that.finished = {}
        for(let i=0;i<data.length;i++){
          var title = data[i][0]
          var datetime = data[i][1]
          that.finished[title] = datetime
        }
      })
      var now_date=new Date().getDate().toString()
      if(index ==this.getIndex(now_date)){
        this.current=''
        this.now1 = index
      }else{
        this.now1=''
        this.now2=''
        this.current = index
        this.now2 = this.getIndex(this.nowLi.substr(5,2))
      }
    },
    //删除习惯
    deleteHabit(habit){
      let requestData={
        username:localStorage.getItem('xm'),
        title:habit.title
      }
      var that = this
      deletehabit(requestData).then(function(res){
        that.standard = [];
        that.showList();
        that.showFinished();
        that.showAll();
      })
    },
    //进入添加习惯页面
    toAddhabit(){
      var un = localStorage.getItem('xm')
      if(!un){
        this.$message.error("您尚未登录，请前往登录！");
        this.$router.push({
          path:"/login"
        })
    } 
    else{
        this.$router.push({
        path:"/details"
        })
    }
    },
    //进入可视化部分
    toVisual(habit){
      var now_datetime = this.getnowDate()
      if(now_datetime >= habit.datetime){
        this.$router.push({
          path:"/visual",
          query:{
            habit:habit
          }
        })
      }
      else{
        this.$message.error("时间还没到这一天哦！")
      }
    },
    //初始化显示当天的习惯列表
    showList(){
      let requestData = {
        username:localStorage.getItem('xm'),
        datetime:this.getnowDate()
      }
      var that = this
      showHabit1(requestData).then(function(res){
        let data = res.data.result
        var habit = []
        that.habits = []
        var now_datetime = that.getnowDate()
        for(let i = 0;i < data.length;i++){
              var habit_data = []
              habit_data = data[i]
              that.habits.push({title:habit_data[2],habit_object:habit_data[3],object_number:habit_data[4],datetime:now_datetime})
        }
      })
      },
    //初始化显示当天的习惯完成情况
  showFinished(){
      let requestData2 = {
        username: localStorage.getItem('xm'),
        datetime: this.getnowDate()
      }
      var that = this
      checkDetail1(requestData2).then(function(res){
        let data = res.data.result
        that.finished = {}
        for(let i=0;i<data.length;i++){
          var title = data[i][0]
          var finished = data[i][1]
          that.finished[title] = finished
        }
      })
    },
    //初始化显示用户全部的习惯完成情况
  showAll(){
    let requestData3 = {
      username: localStorage.getItem('xm')
    }
    var that = this
    checkDetail2(requestData3).then(function(res){
      let inputDetail_data = res.data.inputDetail_result
      let habit_datas =res.data.habit_result
      that.finished_total = {}
      that.habit_total = {}
      for(let i=0;i<inputDetail_data.length;i++){
        var datetime = inputDetail_data[i][0]
        var finished = inputDetail_data[i][1]
        if(datetime in that.finished_total){
          if(finished == 'true'){
            that.finished_total[datetime] +=1
          }
          else{
            that.finished_total[datetime] +=0
          }
        }
        else{
          if(finished == 'true'){
              that.finished_total[datetime] = 1
          }
          else{
              that.finished_total[datetime] = 0
          }
        }
      }
      var each_days = []
      for(let i=0;i<that.days.length;i++){
          var month = ''
          var date=''
          if(that.month >9){
            month = that.month
          }
          else{
            month = "0" + that.month
          }
          if(that.days[i].symbol == "2"){
            if(that.days[i].date > 9){
              date = that.days[i].date
            }
            else{
              date = "0" + that.days[i].date
            }
          }
          else{
            date = "32"
          }
          var each_day = parseInt(that.year + month +date)
          each_days.push(each_day)
        }
      for(let i=0;i<habit_datas.length;i++){
        for(let j=0;j<each_days.length;j++){
          var nowdate = each_days[j]
          if(nowdate.toString().substr(6,2) == "32"){
            that.habit_total[nowdate] = 0
          }
          else{
            if(habit_datas[i][1] <= nowdate){
              if(nowdate in that.habit_total){
                that.habit_total[nowdate] +=1
              }
              else{
              that.habit_total[nowdate] =1
              }
            }
            else{
              // console.log("hello")
            }
          }
        }
      }
      for(let i=0;i<each_days.length;i++){
        var each_day = each_days[i].toString()
        var standard = ''
        var count = that.finished_total[each_days[i]]
        if(!count){
          standard = '0'
        }
        else{
          if(count == that.habit_total[each_days[i]]){
            standard = '1'
          }
          else if(count >0 && count < that.habit_total[each_days[i]]){
            standard = '2'
          }
          else{
            standard = '0'
          }
        }
        that.standard.push(standard)
      }
    })
    }
  },
  //初始化
  created(){
    this.showList();
    this.showFinished();
    this.showAll();
},
  mounted(){
    this.getDate();
    this.handleShowDateStyle();
  }
}
</script>
<style scoped>
.calender{
  position: relative;
  width: 400px;
  height:500px;
  z-index: 1;
  background-color: whitesmoke;
  font-family:sans-serif;
  overflow: hidden;
}
.calender>.habit{
  position: relative;
  float: left;
  display:block;
  width: 100%; 
  z-index: -1;
  min-height: 165px;
  max-height: 165px; 
  overflow:auto;
  /* border: 1px solid red; */
}
.top{
  height:70px;
  position:relative;
  color:black;
  background-color:#308ff0;
}
.top_date{
  text-align:center;
  padding-top:15px;
  color:#fff;
  display:block;
}
.btn_wrap{
  flex: 1;
  text-align: right
}
.btn_wrap ul{
  display: flex;
  flex-direction: row-reverse
}
.btn_wrap ul li{
  padding: 10px 20px;
  border: 1px solid #ddd;
  font-size: 16px;
  line-height: 20px;
  cursor: pointer;
}
.btn_wrap ul li:first-child{
   border:none;
   width: 100px;
  height: 20px;
  display: block;
  position: absolute;
  left: 50%;
  top: 50%;
  margin-top: -20px;
  margin-left: 70px;
  color:#fff
}
.btn_wrap ul li:last-child{
  border: none;
  width: 100px;
  height: 20px;
  display: block;
  position: absolute;
  left: 50%;
  top: 50%;
  margin-top: -20px;
  margin-left: -200px;
  color:#fff;
}
.btn_wrap .today{
  border:none;
  width: 100px;
  height: 20px;
  display: block;
  position: absolute;
  left: 50%;
  top: 50%;
  margin-top: 1px;
  margin-left: -65px;
  color:#fff;
}
.date_wrap{
  width:100%;
  /* height:260px; */
  display: block;
  float: left;
  height: auto;
  position:relative;
  margin-left:-3px;
  background-color:white;
}
.week{
  display: flex;
  height:23px;
  flex-direction: row;
  padding-left: 23px;
  padding-top:3px;
  font-size: 13px;
  color:#308ff0;
}
.week li{
  width: 14.28%;
}
.day{
  display: flex;
  flex-direction: row;
  padding-left:20px;
  font-size: 14px;
  flex-wrap: wrap;
  margin-top:-15px;
}
.day li{
  width: 14.28%;
  padding-left:10px;
  padding-top:15px;
  box-sizing:border-box;
}
.now{
  color:blue;
  font-weight:900;
}

#add{
  position: absolute;
  top: 20px;
  right: 20px;
  border-radius: 100%;
  width:3rem;
  height:3rem;
  z-index: 1;
}
.bgColors{
  color: red;
  font-weight:900;
}
.change_now2{
    color: black;
    font-weight:normal;
}
.change_now1{
  color: blue;
  font-weight:900;
}
#delete{
  width:35px;
  height:35px;
  background-color:whitesmoke;
  border:none;
  outline:none;
  color:red;
  font-size:20px;
  font-weight:900;
  margin-left:-40px;
}
.habitlist li .finishColor{
  width:33px;
  height:33px;
  margin-left:20px;
  margin-bottom: 4px;
  opacity:1;
}
.day li .Colors3{
  width:30px;
  height:30px;
  z-index:-1;
  margin-left:-23px;
  opacity:1;
}
.habitlist li img{
  width:35px;
  height:35px;
  margin-left:80px;
  opacity:0;
}
.day li img{
  width:30px;
  height:30px;
  z-index:-1;
  margin-left:-23px;
  opacity:0;
}
.point{
  cursor: pointer;
}
</style>