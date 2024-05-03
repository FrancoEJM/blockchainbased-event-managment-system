import { useState, useEffect } from 'react';
import axios from 'axios';

function EventWizard() {
  const [step, setStep] = useState(1);
  const [categorias, setCategorias] = useState([]);
  const [modalidades, setModalidades] = useState([]);
  const [idiomas, setIdiomas] = useState([]);
  const [privacidades, setPrivacidades] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/api/event/create`);
        const data = response.data;
        console.log(response.data);

        setCategorias(data.categoria);
        setModalidades(data.modalidad);
        setIdiomas(data.idioma);
        setPrivacidades(data.privacidad);
      } catch (error) {
        console.error('Error al cargar los datos:', error);
      }
    };

    fetchData();
  }, []);

  const handleNext = () => {
    if (step < 4) {
      setStep(step + 1);
    }
  };

  const handleBack = () => {
    if (step > 1) {
      setStep(step - 1);
    }
  };

  return (
    <div className="flex justify-center items-center max-h-screen">
      <div className="bg-white p-8 border-2 border-gray-200 shadow-lg rounded-lg w-5/6 h-[75vh] overflow-hidden mt-8 relative">
        <div className="flex space-x-4">
          <div className="flex-1">
            <div>
              <label htmlFor="nombre" className="block mb-1">Nombre:</label>
              <input type="text" id="nombre" className="w-full border border-gray-300 rounded-md p-2" />
            </div>
            <div>
              <label htmlFor="descripcion" className="block mb-1">Descripción:</label>
              <textarea id="descripcion" className="w-full border border-gray-300 rounded-md p-2 h-20"></textarea>
            </div>
          </div>
          <div className="flex-1">
            <div>
              <label htmlFor="desde" className="block mb-1">Desde:</label>
              <input type="date" id="desde" className="w-full border border-gray-300 rounded-md p-2" />
            </div>
            <div>
              <label htmlFor="privacidad" className="block mb-1">Privacidad:</label>
              <select id="privacidad" className="w-full border border-gray-300 rounded-md p-2">
                {privacidades.map((privacidad) => (
                  <option key={privacidad.id_privacidad} value={privacidad.id_privacidad}>{privacidad.descripcion}</option>
                ))}
              </select>
            </div>
            <div>
              <label htmlFor="invitados" className="block mb-1">Lista de Invitados:</label>
              <input type="text" id="invitados" className="w-full border border-gray-300 rounded-md p-2" />
            </div>
          </div>
          <div className="flex-1">
            <div>
              <label htmlFor="hasta" className="block mb-1">Hasta:</label>
              <input type="date" id="hasta" className="w-full border border-gray-300 rounded-md p-2" />
            </div>
            <div>
              <label htmlFor="idioma" className="block mb-1">Idioma:</label>
              <select id="idioma" className="w-full border border-gray-300 rounded-md p-2">
                {idiomas.map((idioma) => (
                  <option key={idioma.id_idioma} value={idioma.id_idioma}>{idioma.descripcion}</option>
                ))}
              </select>
            </div>
            <div>
              <label htmlFor="modalidad" className="block mb-1">Modalidad:</label>
              <select id="modalidad" className="w-full border border-gray-300 rounded-md p-2">
              {modalidades && modalidades.map((modalidad) => (
                <option key={modalidad.id_modalidad} value={modalidad.id_modalidad}>{modalidad.descripcion}</option>
              ))}

              </select>
              {modalidades === 'online' && (
                <div>
                  <label htmlFor="url" className="block mb-1 mt-2">URL:</label>
                  <input type="text" id="url" className="w-full border border-gray-300 rounded-md p-2" />
                </div>
              )}
            </div>
          </div>
        </div>
        <div className="flex justify-end">
          {step > 1 && (
            <button type="button" className="bg-blue-500 text-white px-4 py-2 rounded-md mr-2" onClick={handleBack}>Atrás</button>
          )}
          {step < 4 ? (
            <button type="button" className={`bg-blue-500 text-white px-4 py-2 rounded-md ${step === 1 ? 'ml-auto' : ''}`} onClick={handleNext}>Siguiente</button>
          ) : (
            <button type="button" className="bg-blue-500 text-white px-4 py-2 rounded-md" onClick={() => console.log('Registro completado')}>Finalizar</button>
          )}
        </div>
      </div>
    </div>
  );
}

export default EventWizard;
