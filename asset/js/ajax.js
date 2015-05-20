$("#new_path").click(function(e){
  // Stop form from submitting normally
  e.preventDefault();
  postParams = setPostParams();
  console.log(JSON.stringify(postParams));
  if (postParams.from=="" || postParams.to=="")
    alert("Please input from and to");
  else { 
    clearAll();
    $.post("path.json", postParams, function(data){
    });
  }
});

$("#navigate").click(function(e){
  // Stop form from submitting normally
  e.preventDefault();
  getParams = setGetParams();
  console.log(getParams);
  alert(getParams);
  if (getParams.from=="" || getParams.to=="")
    alert("Please input from and to");
  else { 
    $.get("path.json", getParams, function(data){
      alert(data);
    });
  }
});

$("#new_poi").click(function(e){
  // Stop form from submitting normally
  e.preventDefault();
  poiVal = document.getElementById("poi").value;
  if (poiVal=="")
    alert("Please input poi");
  else { 
    $.get("poi.json", {"poi": poiVal}, function(data){
    });
  }
});

function setPostParams(){
  from_tag = document.getElementById('from').value;
  to_tag   = document.getElementById('to').value;
  postData = {"status": 0, "path": JSON.stringify(path), "from": from_tag, "to": to_tag};
  return postData;
}

function setGetParams(){
  from_tag = document.getElementById('from').value;
  to_tag   = document.getElementById('to').value;
  getData = {"status": 0, "from": from_tag, "to": to_tag};
  return getData;
}

function clearAll(){
  pathsToRecord.geometry.coordinates = [];
  path  = [];
  newPathLayer.clearLayers();
  markers.clearLayers();
}
