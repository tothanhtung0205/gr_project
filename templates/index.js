function getAnswer2() {
    console.log("con me mai");
}


                function getAnswer() {
                var input = document.getElementById("question").value;
                var settings = {
  "async": true,
  "crossDomain": true,
  "url": "http://127.0.0.1:8008/qa",
  "method": "POST",
  "headers": {
    "cache-control": "no-cache",
    "postman-token": "483f6741-7c85-77d7-a084-817812309624"
  },
  "data": input
}

$.ajax(settings).done(function (response) {
  console.log(response);
});

                }





//                    function getAnswer(){
//                        var serverResponse = "";
//                        var input = document.getElementById("question").value;
//                        var http = new XMLHttpRequest();
//                        var params = input;
//                        var url = "http://127.0.0.1:8008/qa";
//                        http.open("POST", url, true);
//                        http.setRequestHeader("Content-type", "text/plain; charset=UTF-8");
//                        document.getElementById("answer").innerHTML = "CON GA NAY"
//                        http.onreadystatechange= function() {
//                            if (this.readyState!==4) return; // not ready yet
//                            if (this.status===200) { // HTTP 200 OK
//                                serverResponse = this.responseText;
//                                console.log(serverResponse)
//                                document.getElementById("answer").innerHTML = "CON GA NAY"
//                            } else {
//                                // server returned an error. Do something with it or ignore it
//                            }
//                        };
//                        http.send(params);
//                      //  window.alert("submited !!!");
//                    }