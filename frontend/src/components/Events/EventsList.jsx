import { Link } from "react-router-dom";
function EventsList() {
  const JSONTest = [
    {
      id: 1,
      categoria: "Inteligencia Artificial",
      titulo: "Conferencia sobre Avances en Procesamiento de Lenguaje Natural",
      contenido:
        "Expertos de todo el mundo se reunirán para discutir los últimos avances en procesamiento de lenguaje natural, incluyendo modelos de aprendizaje profundo y aplicaciones en la industria.",
      fecha: "2024-05-15",
      lugar: "Centro de Convenciones TechHub, San Francisco",
      hora: "10:00 - 16:00",
    },
    {
      id: 2,
      categoria: "Ciberseguridad",
      titulo: "Taller sobre Prevención de Amenazas Cibernéticas",
      contenido:
        "Este taller proporcionará a los asistentes información actualizada sobre las últimas amenazas cibernéticas y las mejores prácticas para proteger sus sistemas y datos.",
      fecha: "2024-06-02",
      lugar: "Universidad Tecnológica CyberDefense, Londres",
      hora: "09:30 - 17:00",
    },
    {
      id: 3,
      categoria: "Realidad Virtual",
      titulo: "Exposición de Avances en Tecnología de Realidad Virtual",
      contenido:
        "Descubre las últimas innovaciones en tecnología de realidad virtual en esta exposición, que incluirá demos de nuevos dispositivos y aplicaciones emocionantes.",
      fecha: "2024-07-10",
      lugar: "Centro de Convenciones VR World, Tokio",
      hora: "11:00 - 18:00",
    },
  ];

  return (
    <>
      {JSONTest.map((evento) => (
        <div key={evento.id} className="flex justify-center mx-5">
          <div className="w-full relative flex bg-clip-border rounded-xl bg-white text-gray-700 shadow-md max-w-6xl flex-row max-h-80 mt-5">
            <div className="relative w-2/5 m-0 overflow-hidden text-gray-700 bg-white rounded-r-none bg-clip-border rounded-xl shrink-0">
              <img
                src="https://images.unsplash.com/photo-1522202176988-66273c2fd55f?ixlib=rb-4.0.3&amp;ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&amp;auto=format&amp;fit=crop&amp;w=1471&amp;q=80"
                alt="card-image"
                className="object-cover w-full h-full"
              />
            </div>
            <div className="p-6">
              <h6
                id="category"
                className="block mb-4 font-sans text-base antialiased font-semibold leading-relaxed tracking-normal text-gray-700 uppercase"
              >
                {evento.categoria}
              </h6>
              <h4
                id="title"
                className="block mb-2 font-sans text-2xl antialiased font-semibold leading-snug tracking-normal text-blue-gray-900"
              >
                {evento.titulo}
              </h4>
              <p
                id="text"
                className="block mb-4 font-sans text-base antialiased font-normal leading-relaxed text-gray-700"
              >
                {evento.contenido.length < 170
                  ? evento.contenido
                  : evento.contenido.slice(0, 170) + "..."}
              </p>
              <div className="grid grid-cols-4 gap-4">
                <div className="col-span-3">
                  <div className="grid grid-rows-4 gap-2">
                    <div className="row-span-1 flex items-center">
                      <div className="font-semibold">Fecha:</div>
                      <div id="date" className="ml-2">
                        {evento.fecha}
                      </div>
                    </div>
                    <div className="row-span-1 flex items-center">
                      <div className="font-semibold">Hora:</div>
                      <div id="hour" className="ml-2">
                        {evento.hora}
                      </div>
                    </div>
                    <div className="row-span-1 flex items-center">
                      <div className="font-semibold">Lugar:</div>
                      <div id="place" className="ml-2">
                        {evento.lugar}
                      </div>
                    </div>
                  </div>
                </div>
                <div className="col-span-1 row-span-3  items-center justify-center mt-4">
                  <Link
                    to={`/events/${evento.id}`}
                    className="col-span-1 row-span-3  items-center justify-center mt-4"
                  >
                    <button className="px-4 py-2 bg-blue-500 text-white shadow">
                      Quiero saber más
                    </button>
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      ))}
      <div className="flex justify-center mx-5">
        <div className="w-full relative flex bg-clip-border rounded-xl bg-white text-gray-700 shadow-md max-w-6xl flex-row max-h-80 mt-5">
          <div className="relative w-2/5 m-0 overflow-hidden text-gray-700 bg-white rounded-r-none bg-clip-border rounded-xl shrink-0">
            <img
              src="https://images.unsplash.com/photo-1522202176988-66273c2fd55f?ixlib=rb-4.0.3&amp;ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&amp;auto=format&amp;fit=crop&amp;w=1471&amp;q=80"
              alt="card-image"
              className="object-cover w-full h-full"
            />
          </div>
          <div className="p-6">
            <h6
              id="category"
              className="block mb-4 font-sans text-base antialiased font-semibold leading-relaxed tracking-normal text-gray-700 uppercase"
            >
              startups
            </h6>
            <h4
              id="title"
              className="block mb-2 font-sans text-2xl antialiased font-semibold leading-snug tracking-normal text-blue-gray-900"
            >
              Lyft launching cross-platform service this week
            </h4>
            <p
              id="text"
              className="block mb-4 font-sans text-base antialiased font-normal leading-relaxed text-gray-700"
            >
              Like so many organizations these days, Autodesk is a company in
              transition. It was until recently a traditional boxed software
              company selling licenses. Yet its own business model disruption is
              only part of the story
            </p>
            <div className="grid grid-cols-4 gap-4">
              <div className="col-span-3">
                <div className="grid grid-rows-4 gap-2">
                  <div className="row-span-1 flex items-center">
                    <div className="font-semibold">Fecha:</div>
                    <div id="date" className="ml-2">
                      asd
                    </div>
                  </div>
                  <div className="row-span-1 flex items-center">
                    <div className="font-semibold">Hora:</div>
                    <div id="hour" className="ml-2">
                      asd
                    </div>
                  </div>
                  <div className="row-span-1 flex items-center">
                    <div className="font-semibold">Lugar:</div>
                    <div id="place" className="ml-2">
                      asd
                    </div>
                  </div>
                </div>
              </div>
              <div className="col-span-1 row-span-3  items-center justify-center mt-4">
                <button className="px-4 py-2 bg-blue-500 text-white shadow">
                  Quiero saber más
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className="flex justify-center mx-5">
        <div className="w-full relative flex bg-clip-border rounded-xl bg-white text-gray-700 shadow-md max-w-6xl flex-row max-h-80 mt-5">
          <div className="relative w-2/5 m-0 overflow-hidden text-gray-700 bg-white rounded-r-none bg-clip-border rounded-xl shrink-0">
            <img
              src="https://images.unsplash.com/photo-1522202176988-66273c2fd55f?ixlib=rb-4.0.3&amp;ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&amp;auto=format&amp;fit=crop&amp;w=1471&amp;q=80"
              alt="card-image"
              className="object-cover w-full h-full"
            />
          </div>
          <div className="p-6">
            <h6
              id="category"
              className="block mb-4 font-sans text-base antialiased font-semibold leading-relaxed tracking-normal text-gray-700 uppercase"
            >
              startups
            </h6>
            <h4
              id="title"
              className="block mb-2 font-sans text-2xl antialiased font-semibold leading-snug tracking-normal text-blue-gray-900"
            >
              Lyft launching cross-platform service this week
            </h4>
            <p
              id="text"
              className="block mb-4 font-sans text-base antialiased font-normal leading-relaxed text-gray-700"
            >
              Like so many organizations these days, Autodesk is a company in
              transition. It was until recently a traditional boxed software
              company selling licenses. Yet its own business model disruption is
              only part of the story
            </p>
            <div className="grid grid-cols-4 gap-4">
              <div className="col-span-3">
                <div className="grid grid-rows-4 gap-2">
                  <div className="row-span-1 flex items-center">
                    <div className="font-semibold">Fecha:</div>
                    <div id="date" className="ml-2">
                      asd
                    </div>
                  </div>
                  <div className="row-span-1 flex items-center">
                    <div className="font-semibold">Hora:</div>
                    <div id="hour" className="ml-2">
                      asd
                    </div>
                  </div>
                  <div className="row-span-1 flex items-center">
                    <div className="font-semibold">Lugar:</div>
                    <div id="place" className="ml-2">
                      asd
                    </div>
                  </div>
                </div>
              </div>
              <div className="col-span-1 row-span-3  items-center justify-center mt-4">
                <button className="px-4 py-2 bg-blue-500 text-white shadow">
                  Quiero saber más
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
export default EventsList;
