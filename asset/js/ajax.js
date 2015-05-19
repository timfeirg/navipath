$("#new_path").click(function(e){
  // Stop form from submitting normally
  e.preventDefault();
  postParams = setPostParams();
  alert(JSON.stringify(postParams));
  if (postParams.from=="" || postParams.to=="")
    alert("Please input from and to");
  else { 
    $.post("http://127.0.0.1:8888/path.json", postParams, function(data){
    });
  }
});


$("#navigate").click( function(e){
  // Stop form from submitting normally
  e.preventDefault();
  getParams = setGetParams();
  alert(JSON.stringify(getParams));
  if (getParams.from=="" || getParams.to=="")
    alert("Please input from and to");
  else { 
    $.get("http://127.0.0.1:8888/path.json", paths, function(data) {
      alert(data);
    });
  }
});


$("#new_poi").click( function(e){
  // Stop form from submitting normally
  e.preventDefault();
  poiVal = document.getElementById("poi").value
    if (poiVal=="")
      alert("Please input from and to");
    else { 
      $.get("127.0.0.1:8888/poi.json", {"poi": poiVal}, function(data) {
      });
    }
});


function setPostParams(){
  from_tag = document.getElementById('from').value;
  to_tag   = document.getElementById('to').value;
  postData = {"status": 0, "path": paths, "from": from_tag, "to": to_tag};
  return postData;
}

function setGetParams(){
  from_tag = document.getElementById('from').value;
  to_tag   = document.getElementById('to').value;
  getData = {"status": 0, "from": from_tag, "to": to_tag};
  return getData;
}

