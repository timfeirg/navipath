var markers = [] ;

var path    = [];
var paths =
{
  "type": "FeatureCollection",
  "features": [
  {
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
  },
  ]
};

function addMarker(eventObject)
{
  coordinate = [eventObject.latlng.lng, eventObject.latlng.lat]; 
  path.push(coordinate);
  marker     =  L.marker(eventObject.latlng);
  markers.push(marker);
  marker.addTo(map);
  paths.features[0].geometry.coordinates.push(coordinate);
  replacePath();
}

function onEachFeature(feature, layer) {
  var popupContent = ""
    if (feature.properties && feature.properties.popupContent) {
      popupContent += feature.properties.popupContent;
    }
  layer.bindPopup(popupContent);
}

//New a geojson layer for paths
function newPathLayer() {
  return L.geoJson(paths, {
    filter: function (feature, layer) {
      if (feature.properties) {
        return feature.properties.isDeleted !== undefined ? !feature.properties.isDeleted : true;
      }
      return false;
    },
    onEachFeature: onEachFeature
  });
}

//Replace paths data
function replacePath() {
  pathLayer.clearLayers();
  pathLayer.addData(paths);
}

