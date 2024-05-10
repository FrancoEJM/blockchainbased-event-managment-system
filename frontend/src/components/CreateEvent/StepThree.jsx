/* eslint-disable react/prop-types */
import { useState, useEffect, useRef } from "react";

import { MapContainer, TileLayer, Marker, useMapEvents } from "react-leaflet";
import "leaflet/dist/leaflet.css";

function LocationMarker({ setPosition, setState }) {
  useMapEvents({
    click(event) {
      setPosition([event.latlng.lat, event.latlng.lng]);
      setState({
        latitud: event.latlng.lat,
        longitud: event.latlng.lng,
      });
    },
  });

  return null;
}

const StepThree = ({
  modalidad,
  onLocationSelected,
  onAdressSelected,
  onImageUpload,
}) => {
  const [uploadedImage, setUploadedImage] = useState(null);
  const [markerPosition, setMarkerPosition] = useState([
    -39.833333, -73.231389,
  ]);

  const mapRef = useRef(null);

  const handleImageUpload = (event) => {
    const imageFile = event.target.files[0];
    const imageUrl = URL.createObjectURL(imageFile);
    setUploadedImage(imageUrl);
    onImageUpload(imageFile);
  };

  //Forzar actualización del mapa para carga correcta
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      window.dispatchEvent(new Event("resize"));
    }, 5000);

    return () => clearTimeout(timeoutId);
  }, []);

  return (
    <div className="flex flex-col sm:flex-row">
      {/* Izquierda */}
      <div
        className={`w-full ${
          modalidad == 2 ? "sm:mx-auto" : "sm:w-1/2"
        } p-4 bg-gray-50 border border-dashed border-gray-400 rounded-xl flex flex-col  mx-5 items-center`}
      >
        <label htmlFor="imageUpload" className="mb-4">
          <input
            type="file"
            id="imageUpload"
            accept="image/*"
            onChange={handleImageUpload}
            className="hidden"
          />
          <span className="ml-2 p-2 bg-violet-500 text-white cursor-pointer shadow-md hover:shadow-2xl">
            Seleccione una imágen para el evento
          </span>
        </label>
        {uploadedImage && (
          <div className="flex justify-center items-center flex-grow">
            <img
              src={uploadedImage}
              alt="Uploaded"
              className="max-h-96 max-w-full"
            />
          </div>
        )}
      </div>

      {/* Derecha (Solo si modalidad == 1) */}
      {modalidad == 1 && (
        <div className="w-full sm:w-1/2 p-4 bg-gray-50 border border-dashed border-gray-400 rounded-xl mx-5">
          <div style={{ height: "500px" }}>
            <label
              className="block tracking-wide text-grey-darker text-xs font-bold mb-2"
              htmlFor="direccion"
            >
              Dirección
            </label>
            <input
              className="appearance-none block w-full bg-grey-lighter text-grey-darker border border-red rounded py-3 px-4 mb-3"
              id="direccion"
              name="direccion"
              type="text"
              placeholder="Ingrese la dirección del evento y luego marque su ubicación en el mapa"
              onChange={(e) => {
                //setAddress(e.target.value);
                onAdressSelected(e.target.value);
              }}
            />
            <MapContainer
              center={[-39.833333, -73.231389]}
              zoom={13}
              scrollWheelZoom={true}
              className=" w-full"
              style={{ height: "400px" }}
              whenCreated={(mapInstance) => {
                mapRef.current = mapInstance;
              }}
            >
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />
              <LocationMarker
                setPosition={setMarkerPosition}
                setState={onLocationSelected}
              />
              <Marker position={markerPosition}></Marker>
            </MapContainer>
          </div>
        </div>
      )}
    </div>
  );
};

export default StepThree;
