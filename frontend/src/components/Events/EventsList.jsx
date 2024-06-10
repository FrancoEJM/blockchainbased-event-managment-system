import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { formatDate, formatTime } from "../../utils/utils";
function EventsList() {
  const [events, setEvents] = useState([]);
  const user_id = localStorage.id_usuario;
  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const response = await fetch(
          `${import.meta.env.VITE_BACKEND_URL}/api/events?id=${user_id}`
        );
        if (!response.ok) {
          throw new Error("Error al obtener los eventos");
        }
        const data = await response.json();
        console.log(data);
        setEvents(data);
      } catch (error) {
        console.error("Error:", error);
      }
    };

    fetchEvents();
  }, []);

  return (
    <>
      {events.map((evento) => (
        <div key={evento.id_evento} className="flex justify-center mx-5">
          <div className="w-full relative flex bg-clip-border bg-white text-gray-700 shadow-md max-w-6xl flex-row max-h-80 mt-5">
            <div className="relative w-2/5 m-0 overflow-hidden text-gray-700 bg-white rounded-r-none bg-clip-border shrink-0">
              {evento.imagenes.length > 0 && (
                <img
                  src={`${import.meta.env.VITE_BACKEND_URL}${
                    evento.imagenes[0].path
                  }`}
                  alt="card-image"
                  className="object-cover w-full h-full"
                />
              )}
            </div>
            <div className="p-6">
              <h6
                id="category"
                className="block mb-4 font-sans text-base antialiased font-semibold leading-relaxed tracking-normal text-gray-700 uppercase"
              >
                {evento.categorias.descripcion}
              </h6>
              <h4
                id="title"
                className="block mb-2 font-sans text-2xl antialiased font-semibold leading-snug tracking-normal text-blue-gray-900"
              >
                {evento.nombre}
              </h4>
              <p
                id="text"
                className="block mb-4 font-sans text-base antialiased font-normal leading-relaxed text-gray-700"
              >
                {evento.descripcion && evento.descripcion.length < 170
                  ? evento.descripcion
                  : evento.descripcion
                  ? evento.descripcion.slice(0, 170) + "..."
                  : "Sin descripción"}
              </p>

              <div className="grid grid-cols-4 gap-4">
                <div className="col-span-3">
                  <div className="grid grid-rows-4 gap-2">
                    <div className="row-span-1 flex items-center">
                      <div className="font-semibold">Fecha:</div>
                      <div id="date" className="ml-2">
                        {formatDate(evento.fecha)}
                      </div>
                    </div>
                    <div className="row-span-1 flex items-center">
                      <div className="font-semibold">Hora:</div>
                      <div id="hour" className="ml-2">
                        {formatTime(evento.hora_inicio)} -{" "}
                        {formatTime(evento.hora_fin)}
                      </div>
                    </div>
                    <div className="row-span-1 flex items-center">
                      {evento.modalidades && (
                        <>
                          <div className="font-semibold">Modalidad:</div>
                          <div
                            id={`modalidad-${evento.modalidades.id_modalidad}`}
                            className="ml-1"
                          >
                            {evento.modalidades.descripcion}
                          </div>
                          {evento.modalidades.id_modalidad === 1 &&
                            evento.direccion && (
                              <>
                                <div className="font-semibold ml-4">
                                  Dirección:
                                </div>
                                <div className="ml-1">{evento.direccion}</div>
                              </>
                            )}
                        </>
                      )}
                    </div>
                  </div>
                </div>
                <div className="col-span-1 row-span-3  items-center justify-center mt-4">
                  <Link
                    to={`/events/${evento.id_evento}`}
                    className="col-span-1 row-span-3  items-center justify-center mt-4"
                  >
                    <button className="px-4 py-2 bg-violet-400 text-white shadow hover:shadow-lg">
                      Quiero saber más
                    </button>
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      ))}
    </>
  );
}

export default EventsList;
