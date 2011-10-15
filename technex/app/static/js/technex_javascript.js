//timer.js

dateFuture1 = new Date(2011,8,15,23,59,59); 
function GetCount(ddate,iid){ 
 
 dateNow = new Date();
 amount = ddate.getTime() - dateNow.getTime();
 delete dateNow; 
  if(amount < 0){ 
  document.getElementById(iid).innerHTML="Now!"; 
 } 
 else{ 
  days=0;hours=0;mins=0;secs=0;out=""; 
 
  amount = Math.floor(amount/1000);
 
  days=Math.floor(amount/86400);
  amount=amount%86400; 
 
  hours=Math.floor(amount/3600);
  amount=amount%3600; 
 
  mins=Math.floor(amount/60);
  amount=amount%60; 
 
  secs=Math.floor(amount);
 
  if(days != 0){out += days +" "+((days==1)?"D":"D")+", ";} 
  out += (hours<=9?'0':'')+hours +" "+((hours==1)?"":"")+": "; 
  out += (mins<=9?'0':'')+mins +" "+((mins==1)?"":"")+": "; 
  out += (secs<=9?'0':'')+secs +" "+((secs==1)?"":"")+"DeadLine"; 
  out = out.substr(0,out.length-0); 
  document.getElementById(iid).innerHTML=out; 
 
  setTimeout(function(){GetCount(ddate,iid)}, 1000); 
 } 
} 
 
window.onload=function(){ 
 GetCount(dateFuture1, 'timer'); 
 }; 


//csrfsolver

// Function to get the VALUE of a cookie based on the KEY provided as a parameter.
// Used in the technex site to get the VALUE corresponding to csrftoken key.  Eg. getCookie['csrftoken'] while submitting the ajaxrequest.

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}




//text/javascript

$(document).ready(function(){
            $("#in").delay(1000).animate({marginTop:"105px"},"slow");
            $("#out").mouseenter(function(){
            $("#in").animate({marginTop:"0px"});
            });
            $("#out").mouseleave(function(){
            $("#in").delay(1000).animate({marginTop:"105px"});
            });  
            {% if registration_successful %}
                panelswitch(2,50);
            {% endif %}
            });    
		
	    function geteventinfo(){
	        $.ajax({
            url: "/eventspanel/",
            dataType: "html",   
            async: true,
            success: function(response){
                $("div#c5").html(response);
                panelswitch(4,50);
            }
            });
	        };
	        
	        
	        
	    
function ajaxrequest_event(eventname){
            $.ajax({
                url: "/events/",
                global: false,
                type: "POST",
                data: {event_name : eventname , csrfmiddlewaretoken : getCookie('csrftoken')},
                dataType: "html",
                async: true,
                success: function(response2){
                    global: event_obj = $.parseJSON(response2);
	                $.ajax({
                        url: "/eventinfo/",
                        dataType: "html",   
                        async: true,
                        success: function(response3){
                            $("div#c5").html(response3);
                        }
                    });
                }
            });

	    };




function ajaxrequest_mypage(){
            $.ajax({
                url: "/mypage/",
                type: "POST",
                data: {csrfmiddlewaretoken : getCookie('csrftoken')},
                dataType: "html",
                async: true,
                success: function(response4){
                            {% if user.is_authenticated %}
                                global: mypage_obj = $.parseJSON(response4);
                                event_notif_objects = mypage_obj.event_notifications;
                                for (i=0 ; event_notif_objects[i] != undefined ; i++) {
                                    $("div#c4 div#tabs-2").append(event_notif_objects[0].title + " : ");                    
                                    $("div#c4 div#tabs-2").append(event_notif_objects[0].body);
                                }
                            panelswitch(3,50);
                            {% else %}
                                document.location = "/accounts/login";
                            {% endif %}                              
                }
            });

	    };
