<template>
  <div id="wrap">
  <div id='back' @click="back"><i class="el-icon-arrow-left"></i></div>
  <el-table
    :data="datas"
    height="500"
    style="400px;">
    <el-table-column
      type="index"
      width="40">
    </el-table-column>
    <el-table-column
      prop="datetime"
      label="创建时间"
      width="120">
    </el-table-column>
    <el-table-column
      prop="title"
      label="习惯名称"
      width="120">
    </el-table-column>
    <el-table-column
      prop="object"
      label="目标"
      width="120"
      >
    </el-table-column>
  </el-table>

  </div>
</template>
<script>
import Vue from 'vue';
import { checkDetail2 } from '../utils/api.js';
export default {
  name: 'all',
  data(){
    return{
      datas:[]
    }
  },
  methods: {
     back(){
          this.$router.go(-1);
      }
   },
  created(){
      let requestData3 = {
        username: localStorage.getItem('xm')
      }
      var that = this
      checkDetail2(requestData3).then(function(res){
        let habit_datas =res.data.habit_result
        that.datas = []
        for(let i = 0;i < habit_datas.length;i++){
              var habit_data = []
              habit_data = habit_datas[i]
              var datetime = habit_data[1] + ''
              that.datas.push({title:habit_data[0],datetime:datetime.substr(0,4) + '-' + datetime.substr(4,2) + '-' +datetime.substr(6,2),object:habit_data[2] + '=' + habit_data[3] })
        }
      })
}
}
</script>
<style scoped>
  #wrap{
    background-color: whitesmoke;
    width: 400px;
    height:500px;
  }
  #back{
    position: absolute;
    z-index: 2;
    left: 7px;
    top: 13px;
    width: 30px;
    height: 30px;
    cursor: pointer;
  }
</style>