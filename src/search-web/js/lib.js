function startTime() {
    var today=new Date()
    var h=today.getHours()
    var m=today.getMinutes()
    var s=today.getSeconds()
// add a zero in front of numbers<10
    m=checkTime(m)
    s=checkTime(s)
    document.getElementById('currentTime').innerHTML=h+":"+m
    t=setTimeout('startTime()',500)
}

function checkTime(i) {
    if (i<10) {i="0" + i}
    return i
}

function greetUser() {
    var today = new Date()
    var h = today.getHours()
    var time = ""
    if(h < 12) {
        time = "morning"
    }else if(h > 11 && h < 19){
        time = "afternoon"
    }else {
        time = "evening"
    }

    document.getElementById('greeting').innerHTML="Good"+" "+time+","
    t = setTimeout('greetUser()', 500)
}

