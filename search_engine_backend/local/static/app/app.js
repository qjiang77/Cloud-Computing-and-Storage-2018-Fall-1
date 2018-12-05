function mConst(e) {
    var t = momoConstants[e];
    return void 0 === t && console.warn("constant not found: ", e), t;
}

function momoInit() {
    return !0
}

function validateEmail(e) {
    return /[^@]+@[^@]+\.[^@]+/.test(e);
}

//TODO: Search Function
function getQueryParameter(e) {
    e = e.replace(/[\[]/,"\\[").replace(/[\]]/,"\\]");
    var t = new RegExp("[\\?&]" + e + "=([^&#]*)").exec(location.search);
    return null === t? "" : decodeURIComponent(t[1].replace(/\+/g," "));
}

//TODO: Time Display
function getActiveDateString() {
    return activeDateStringForDate(new Date);
}

function activeDateStringForDate(e) {
    var t = new Date(e);
    return t.getHours() < mConst("dateRollOverHour") && (t = new Date(t.getTime() - mConst("dateMsPerDay"))),
        t.getFullYear().toString() + "-" + m.utils.twoDigit(t.getMonth()+1)+"-"+m.utils.twoDigit(t.getDate());
}

function getActiveLocalDateTimeString(){
    return activeLocalDateTimeStringForDate(new Date);
}

function activeLocalDateTimeStringForDate(e) {
    var t=new Date(e);
    return t.getFullYear().toString()+"-"+m.utils.twoDigit(t.getMonth()+1)+"-"+m.utils.twoDigit(t.getDate())+"T"+m.utils.twoDigit(t.getHours())+":"+m.utils.twoDigit(t.getMinutes())+":"+m.utils.twoDigit(t.getSeconds());
}

function getDayName(e,t) {
    return mConst("dayNames"+(t?"Short":""))[e.getDay()];
}

function getMonthName(e,t) {
    return mConst("monthNames"+(t?"Short":""))[e.getMonth()];
}

function getDaysInMonth(e,t) {
    return new Date(e,parseInt(t)+1,0).getDate();
}

function dateDiffIntegerDays(e,t) {
    var i = new Date(e.valueOf());
    return (new Date(t.valueOf()).setHours(0,0,0,0)-i.setHours(0,0,0,0))/mConst("dateMsPerDay");
}

function dateIsYesterday(e) {
    return -1 === m.utils.dateDiffIntegerDays(new Date,e);
}

function dateIsToday(e) {
    return 0 === m.utils.dateDiffIntegerDays(new Date,e);
}

function dateIsTomorrow(e) {
    return 1 === m.utils.dateDiffIntegerDays(new Date,e);
}

function dateIsInLast7d(e) {
    var t=m.utils.dateDiffIntegerDays(new Date,e);
    return -7<t && t<=0;
}

function getHoursMinsStr(e,t) {
    void 0 === t && (t = m.models.customization.get("hour12clock"));
    var i, n = e.getHours();
    return (t ? (i = " " + (n < 12 ? "AM" : "PM"), 12 < n && (n -= 12), 0 === n && (n = 12), n) : (i = "", m.utils.twoDigit(n))) + ":" + m.utils.twoDigit(e.getMinutes()) + i;
}

function parseIsoDatetime(e) {
    var t = e.split(/[: T-]/).map(parseFloat);
    return new Date(t[0],t[1]-1,t[2],t[3]||0,t[4]||0,t[5]||0,0);
}

function toUTC(e) {
    return new Date(e.getTime()-e.getTimezoneOffset()*mConst("dateMsPerMin"));
}

function toLocalTime(e) {
    var t = new Date(e);
    return new Date(t.getTime()+t.getTimezoneOffset()*mConst("dateMsPerMin"));
}

function calcDayMs(e,t) {
    var i = e-new Date(e).setHours(0,0,0,0)-t*mConst("dateMsPerHour");
    return i<0 && (i+=mConst("dateMsPerDay")), i;
}

function dateAdd(e,t,i) {
    var n = new Date(e);
    var o = function() {n.getDate()!==e.getDate()&&n.setDate(0)};
    switch(t.toLowerCase()) {
        case "year":
            n.setFullYear(n.getFullYear()+i),o();
            break;
        case "quarter":
            n.setMonth(n.getMonth()+3*i),o();
            break;
        case "month":
            n.setMonth(n.getMonth()+i),o();
            break;
        case "week":
            n.setDate(n.getDate()+7*i);
            break;
        case "day":
            n.setDate(n.getDate()+i);
            break;
        case "hour":
            n.setTime(n.getTime()+36e5*i);
            break;
        case "minute":
            n.setTime(n.getTime()+6e4*i);
            break;case"second":n.setTime(n.getTime()+1e3*i);
            break;
        default:
            n=void 0;
    }
    return n;
}

//TODO: Position
function topPosition(e) {
    return e.offset().top;
}

function rightPosition(e) {
    return e.offset().left + e.outerWidth();
}

function leftPosition(e) {
    return e.offset().left;
}

function bottomPosition(e) {
    return e.offset().top + e.outerHeight();
}

function distanceBelow(e, t, i) {
    var n = bottomPosition(e) - bottomPosition(t);
    return i && (n += i), n;
}

function smoothScrollToElement(e,t,i,n,o,a,s) {
    void 0 === a && (a=mConst("timeSmoothScroll")),
    void 0 ===s&&(s=mConst("minMarginSmoothScroll")),
    void 0===n&&(n=0);
    var r=distanceBelow(e,t,s);
    setTimeout(function() {
        0<r?t.animate({scrollTop:r},{duration:a,complete:function(){
            smoothScrollHelper(e,i,o)}
        }):smoothScrollHelper(e,i,o)
    },n);
}

function smoothScrollHelper(e,t,i) {
    t&&e.addClass("pulse"),i&&i();
}

function removePulseClass(e) {
    "pulse"!==e.originalEvent.animationName&&"pulselight"!==e.originalEvent.animationName||$(e.target).removeClass("pulse");
}

function scrollToBottom(e) {
    var t=e[0];
    t.scrollTop=t.scrollHeight;
}

function capitalizeWords(e) {
    var i=e.split(" ");
    return i.forEach(function(e,t){i[t]=e.charAt(0).toUpperCase()+e.slice(1)}),i.join(" ");
}

function submitStats(e){}

//TODO: Check input
function handleDblclickFromDashboard(e) {
    e.manager.dblclickFromDashboard&&(e.manager.dblclickFromDashboard=!1,
        setTimeout(function(){e.dblclickFromDashboardCb()},0));
}

function flashInputLengthError(e) {
    toggleClassTwice(e,mConst("classInputLengthError"));
}

function checkForInputMaxLengthError(e) {
    e.is("input")&&e.val().length>=e.attr("maxlength")&&flashInputLengthError(e);
}

function updateCharCount(e,t,i,n) {
    var o=$(e.currentTarget.form);
    n=n||o.find("input");
    var a=o.find(".char-count"),s=n.val().length,r=t.inputLengthMaxDatabase-s;
    a.text(r).removeClass("warn over"),
        a.toggle(s>=t.inputLengthShow),
        n.removeClass("over"),
        s>t.inputLengthMaxDatabase?(a.addClass("over"),
            n.addClass("over")):s>=t.inputLengthWarn&&a.addClass("warn"),
    i&&i(o,s,r);
}

function scrollToEndOfInput(e,t) {
    void 0===t&&(t=0);
    var i=e[0];
    i.scrollWidth>i.clientWidth&&(0!==e.scrollLeft()&&e.scrollLeft(0),e.animate({scrollLeft:i.scrollWidth-i.clientWidth},t));
}

function setEndOfContenteditable(e) {

}




























