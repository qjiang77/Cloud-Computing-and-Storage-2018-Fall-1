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


function listenEnterEvent() {
	var form = document.getElementById("search-form");
	//var input = document.getElementsByName("search")[0];
	//alert(input.value);
	// Execute a function when the user releases a key on the keyboard
	form.addEventListener("keyup", function(event) {
  	// Cancel the default action, if needed
  		event.preventDefault();
  		// Number 13 is the "Enter" key on the keyboard
		
			  		
		if (event.keyCode === 13) {
			var input = document.getElementsByName("search")[0];
			//alert(input.value);			
			if (input.value == ""){
				alert("Please input what you want to search.");			
			}
			else{
				form.submit();
			}
  		}
	});
}
