
//封装axios
import axios from 'axios'
import { Message } from 'element-ui'; //在js单独引用
const server = axios.create({
    baseURL: 'http://127.0.0.1:5000/api',
    timeout: 15000,
    headers:{
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'
    }
  })  

// 添加请求拦截器
server.interceptors.request.use(function (config) {
    // 在发送请求之前做些什么
    if(config.method!='get' || config.method == 'get'){
        // config.data = qs.stringify(config.data);
        config.headers['Content-Type'] = 'application/json';
    }
    return config;
  }, function (error) {
    // 对请求错误做些什么
    return Promise.reject(error);
  });

// 添加响应拦截器
server.interceptors.response.use(function (response) {
    // 对响应数据做点什么
    let data = response.data
    if (data.resCode != 101){
      Message.error(data.message) 
      return Promise.reject(data);//响应错误后发送 error
    }else{
      return response;//响应成功后发送 success
    }
  }, function (error) {
    // 对响应错误做点什么
    return Promise.reject(error);
  });

export default server;