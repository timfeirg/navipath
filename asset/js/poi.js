var markers = new L.FeatureGroup();
var path    = [] ;
var pathsToRecord   = {
  "type": "Feature",
  "geometry": {
    "type": "LineString",
    "coordinates": [
    ]
  },
  "properties": {
    "popupContent": "This is a path.",
    "isDeleted": false
  },
  "id": 1
};

var pathsTobePrint   = {
  "type": "Feature",
  "geometry": {
    "type": "LineString",
    "coordinates": [
    ]
  },
  "properties": {
    "from": "",
    "to": "",
    "popupContent": "This is a path.",
    "isDeleted": false
  },
  "id": 2
};

var testString = JSON.stringify({
"status": 0,
  "result": [
{
  "to": "232323",
  "from": "你好",
  "path": [
    [
    113.38023126125336,
    23.068657051493727
    ],
    [
      113.37982892990111,
      23.068198053152578
    ]
  ]
},
{
  "to": "232323",
  "from": "你妈逼",
  "path": [
    [
    113.38023126125336,
    23.068657051493727
    ],
    [
      113.37982892990111,
      23.068198053152578
    ],
    [
      113.37963581085205,
      23.06789698887407
    ],
    [
      113.37960898876189,
      23.067778537169982
    ]
  ]
}
]
});

// drawing layer for paths
var drawPathLayer = L.geoJson();

function addMarker(eventObj)
{
  coordinate = [eventObj.latlng.lng, eventObj.latlng.lat];
  path.push(coordinate);
  populate(eventObj.latlng);
  pathsToRecord.geometry.coordinates.push(coordinate);
  replacePath();
}

//New a geojson layer for paths
function newPath(){
  return L.geoJson(pathsToRecord);
}

var newPathLayer= newPath();

function populate(latlng){
  var marker =  L.marker(latlng);
  marker.bindPopup("<p>I am a geojson point and my location is ("+latlng.lat+" , "+latlng.lng+"</p>",
      { showOnMouseOver: true,});
  markers.addLayer(marker);
}

//Replace paths data in newPathLayer
function replacePath(){
  newPathLayer.clearLayers();
  newPathLayer.addData(pathsToRecord);
}

function polling(){
  $.get("path.json", {"status": 0}, function(data){
    console.log(data);
    generatePath(data);
  });
}

function generatePath(responseData){
  console.log(responseData);
  path_list = responseData.result
    for (var i=0; i<path_list.length; ++i) {
      single_path = path_list[i];
      pathsTobePrint.properties.from = single_path.from;
      pathsTobePrint.properties.to = single_path.to;
      pathsTobePrint.geometry.coordinates = single_path.path;
      drawPathLayer.addData(pathsTobePrint);
    }
}

function setPolling(){
  var intervalID = window.setInterval(polling, 1000);
}

