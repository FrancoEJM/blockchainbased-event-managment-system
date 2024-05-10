import { useState } from "react";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  useMapEvents,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import icon from "leaflet/dist/images/marker-icon.png";

const iconUbicacion = new L.icon({
  iconUrl: icon,
  iconSize: [60, 55],
  iconAncho: [22, 94],
  shadowAnchor: [22, 94],
  popupAnchor: [-3, -76],
});

function LocationMarker({ setPosition }) {
  useMapEvents({
    click(event) {
      setPosition([event.latlng.lat, event.latlng.lng]);
    },
  });

  return null;
}

function Mapa() {
  const [markerPosition, setMarkerPosition] = useState([
    -39.833333, -73.231389,
  ]);

  return (
    <div style={{ height: "400px", width: "100%" }}>
      <MapContainer
        center={[-39.833333, -73.231389]}
        zoom={13}
        scrollWheelZoom={false}
        className="h-96 w-full"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <LocationMarker setPosition={setMarkerPosition} />
        <Marker position={markerPosition} icon={iconUbicacion}>
          <Popup>
            A pretty CSS3 popup. <br /> Easily customizable.
          </Popup>
        </Marker>
      </MapContainer>
    </div>
  );
}

export default Mapa;
