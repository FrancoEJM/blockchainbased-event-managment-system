import { useParams } from "react-router-dom";
import NavBar from "../../components/Navbar";
import { useEffect, useState, useRef } from "react";
import { formatDate, formatTime } from "../../utils/utils";
import { MapContainer, TileLayer, Marker } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import EventSigningButton from "../../components/Events/EventSigningButton";

function EventPage() {
  const { id } = useParams();
  const [event, setEvent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [markerPosition, setMarkerPosition] = useState([0, 0]);
  const mapRef = useRef(null);
  const [modalOpen, setModalOpen] = useState(false);

  useEffect(() => {
    console.log("ejecuto el useEffect");
    const fetchEvents = async () => {
      try {
        const response = await fetch(
          `${import.meta.env.VITE_BACKEND_URL}/api/event?id=${id}`
        );
        if (!response.ok) {
          throw new Error("Error al obtener el evento");
        }
        const data = await response.json();
        console.log("data", data);
        setEvent(data);
        setLoading(false);
        if (data.modalidad === 1) {
          setMarkerPosition([data.latitud, data.longitud]);
        }
      } catch (error) {
        console.error("Error:", error);
        setLoading(false);
      }
    };
    fetchEvents();
  }, [id]);

  const handleMarkerClick = () => {
    const [lat, lng] = markerPosition;
    const url = `https://www.google.com/maps?q=${lat},${lng}`;
    window.open(url, "_blank");
  };

  if (loading) {
    return (
      <>
        <NavBar></NavBar>
        <div>Cargando...</div>;
      </>
    );
  }

  if (!event) {
    return <div>Error al cargar el evento, es posible que ya no exista</div>;
  }

  return (
    <div>
      <NavBar />

      <div className="container mx-auto my-5 p-5 h-full">
        <div className="md:flex no-wrap md:-mx-2 h-full">
          {/* <!-- Left Side --> */}
          <div className="flex-grow md:w-2/3 md:mx-2">
            {/* <!-- Event --> */}
            <div className="bg-white p-3 border-t-4 border-violet-300 h-full flex flex-col justify-between">
              <div>
                <h1 className="text-gray-900 font-semibold text-2xl leading-8 my-1">
                  {event.nombre}
                </h1>
                <h3 className="text-gray-600 font-lg text-semibold leading-6">
                  <span className="bg-violet-400  p-1 rounded text-white text-sm">
                    {event.categorias.descripcion}
                  </span>
                </h3>
                <p className="overflow-y-auto text-base antialiased font-medium text-gray-500 hover:text-gray-600 leading-6 pr-16 mt-3 max-h-fit">
                  {event.descripcion}
                </p>
              </div>
              <ul className="bg-gray-100 text-gray-600 hover:text-gray-700 hover:shadow py-2 px-3 mt-3 divide-y rounded shadow-sm">
                <li className="flex items-center py-3">
                  <span className="font-semibold">Fecha</span>
                  <span className="ml-auto">
                    <span className="mx-3 font-semibold">
                      {formatDate(event.fecha)}
                    </span>
                    <span className="bg-violet-400 py-1 px-2 mx-3 rounded text-white text-sm">
                      {formatTime(event.hora_inicio)}
                    </span>
                    <span className="bg-violet-400 py-1 px-2 mx-3 rounded text-white text-sm">
                      {formatTime(event.hora_fin)}
                    </span>
                  </span>
                </li>
                <li className="flex items-center py-3">
                  <span className="font-semibold">Modalidad</span>
                  <span className="ml-auto font-semibold">
                    {event.modalidades.descripcion}
                  </span>
                </li>
                <li className="flex items-center justify-between py-2">
                  <span className="font-semibold">
                    Evento {event.privacidades.descripcion.toLowerCase()}
                  </span>
                  <span className="font-semibold">
                    <EventSigningButton />
                  </span>
                </li>
              </ul>
            </div>
          </div>
          {/* <!-- Right Side --> */}
          <div className="w-full md:w-1/3 mx-2 flex flex-col justify-between">
            {/* <!-- Map Section --> */}
            {event.modalidad == 1 && (
              <div className="bg-white shadow-sm rounded-sm mb-6">
                <div className="text-center block w-full text-blue-800 text-sm font-semibold rounded-lg hover:bg-gray-100 focus:outline-none focus:shadow-outline focus:bg-gray-100 hover:shadow-xs p-3 min-h-80">
                  <MapContainer
                    center={markerPosition}
                    zoom={13}
                    scrollWheelZoom={true}
                    className="w-full z-40"
                    style={{ height: "400px" }}
                    whenCreated={(mapInstance) => {
                      mapRef.current = mapInstance;
                    }}
                  >
                    <TileLayer
                      attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                      url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    />

                    <Marker
                      position={markerPosition}
                      eventHandlers={{ click: handleMarkerClick }}
                    />
                  </MapContainer>
                </div>
              </div>
            )}

            {/* <!-- Image --> */}
            <div className="bg-white shadow-sm rounded-sm">
              <div className="text-center flex items-center justify-center w-full text-blue-800 text-sm font-semibold rounded-lg hover:bg-gray-100 focus:outline-none focus:shadow-outline focus:bg-gray-100 hover:shadow-xs p-3 min-h-80 max-h-32 overflow-hidden">
                <img
                  src={`${import.meta.env.VITE_BACKEND_URL}${
                    event.imagenes[0].path
                  }`}
                  alt="card-image"
                  className="object-contain w-full h-full cursor-pointer"
                  onClick={() => setModalOpen(true)}
                />
              </div>
            </div>
          </div>
        </div>
      </div>
      {/* Modal */}
      {modalOpen && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
          onClick={() => setModalOpen(false)}
        >
          <div
            className="relative bg-white rounded-lg p-5 w-full max-w-3xl max-h-screen overflow-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <button
              className="absolute top-0 right-0 m-4 text-black text-xl font-bold"
              onClick={() => setModalOpen(false)}
            >
              &times;
            </button>
            <div className="flex items-center justify-center h-full">
              <img
                src={`${import.meta.env.VITE_BACKEND_URL}${
                  event.imagenes[0].path
                }`}
                alt="modal-image"
                className="object-contain max-w-full max-h-full"
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default EventPage;
