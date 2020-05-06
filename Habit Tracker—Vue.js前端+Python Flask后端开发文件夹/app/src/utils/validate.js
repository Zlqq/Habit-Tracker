/**
 * 验证区域
 */
//验证邮箱
export function validateEmail(value){
    let reg = /^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/;
    return !reg.test(value) ? true : false
}
//验证昵称
export function validateNm(value){
    let reg = /^[\u4E00-\u9FA5A-Za-z0-9]{3,8}$/
    return !reg.test(value) ? true : false
}
//验证密码
export function validatePass(value){
    let reg = /^(?!\D+$)(?![^a-zA-Z]+$)\S{6,20}$/;
    return !reg.test(value) ? true : false;
}
//验证验证码
export function validatevCode(value){
    let reg = /^[0-9A-Za-z]{6}$/
    return !reg.test(value) ? true : false
}
/**
 * 过滤特殊字符
 */
export function stripscript(str) {
    var pattern = new RegExp("[`~!@#$^&*()=|{}':;',\\[\\].<>/?~！@#￥……&*（）&;—|{ }【】‘；：”“'。，、？]")
    var rs = "";
    for (var i = 0; i < str.length; i++) {
        rs = rs + str.substr(i, 1).replace(pattern, '');
    }
    return rs;
}


