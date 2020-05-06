import service from './request.js'
// 获取验证码
export function GetSms(requestData){
    return service.request({
        // `url` 是用于请求的服务器 URL
        url: '/GetSms/',
        method: 'post', // default
        data:requestData
    })
}
//注册
export function signUp(RequestData){
    return service.request({
        url: '/register/',
        method: 'post', // default
        data:RequestData
    })
}
//登录
export function signIn(RequestData){
    return service.request({
        // `url` 是用于请求的服务器 URL
        url: '/login/',
        method: 'post', // default
        data:RequestData
    })
}

//重置密码
export function findPs(RequestData){
    return service.request({
        // `url` 是用于请求的服务器 URL
        url: '/findps/',
        method: 'post', // default
        data:RequestData
    })
}

//存取
export function addHabit(RequestData){
    return service.request({
        // `url` 是用于请求的服务器 URL
        url: '/details/',
        method: 'post', // default
        data:RequestData
    })
}

//查询
export function showHabit(requestData){
    return service.request({
        // `url` 是用于请求的服务器 URL
        url: '/habit/',
        method: 'post', // default
        data:requestData
    })
}
//调取
export function inputDetail(requestData){
    return service.request({
        // `url` 是用于请求的服务器 URL
        url: '/inputDetail/',
        method: 'post', // default
        data:requestData
    })
}
//添加每日打卡记录
export function addrecord(RequestData){
    return service.request({
        // `url` 是用于请求的服务器 URL
        url: '/GetDetail/',
        method: 'post', // default
        data:RequestData
    })
}
//删除某条记录
export function deletehabit(requestData){
    return service.request({
        // `url` 是用于请求的服务器 URL
        url: '/deleteDetail/',
        method: 'post', // default
        data:requestData
    })
}
//初始化时显示数据
export function showHabit1(requestData){
    return service.request({
        // `url` 是用于请求的服务器 URL
        url: '/showDetail/?username='+requestData.username + '&datetime=' +requestData.datetime ,
        method: 'get', // default
    })
}
//查询用户某一天的习惯完成情况
export function checkDetail(requestData2){
    return service.request({
        // `url` 是用于请求的服务器 URL
        url: '/checkDetail/',
        method: 'post', // default
        data:requestData2
    })
}
//初始化时显示用户当天的习惯完成情况
export function checkDetail1(requestData2){
    return service.request({
        // `url` 是用于请求的服务器 URL
        url: '/checkDetail1/?username='+requestData2.username + '&datetime=' + requestData2.datetime,
        method: 'get', // default
    })
}
//初始化显示用户所有习惯的完成情况
export function checkDetail2(requestData3){
    return service.request({
        // `url` 是用于请求的服务器 URL
        url: '/checkDetail2/?username='+requestData3.username,
        method: 'get', // default
    })
}

// 获取用户信息
export function addAdvice(requestData){
    return service.request({
        url: '/addAdvice/',
        method: 'post', // default
        data:requestData
    })
}
