// EventWizard.jsx
import { useState, useEffect } from "react";
import axios from "axios";
import StepOne from "./StepOne";
import StepTwo from "./StepTwo";
import StepThree from "./StepThree";

const EventWizard = () => {
  const [step, setStep] = useState(1);
  const [eventData, setEventData] = useState(null);
  const [stepOneData, setStepOneData] = useState({
    name: "",
    fecha: "",
    desde: "",
    hasta: "",
    descripcion: "",
    privacidad: "",
    idioma: "",
    modalidad: "",
    lista: [],
    url: "",
  });
  const [stepTwoData, setStepTwoData] = useState({});
  const [locationData, setLocationData] = useState({ latitud: 0, longitud: 0 });
  const [adressData, setAddressData] = useState("");
  const [imageData, setImageData] = useState("");

  useEffect(() => {
    axios
      .get(`${import.meta.env.VITE_BACKEND_URL}/api/event/create`)
      .then((response) => {
        setEventData(response.data);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, []);

  const handleNext = () => {
    if (step < 3) {
      setStep(step + 1);
    }
  };

  const handleBack = () => {
    if (step > 1) {
      setStep(step - 1);
    }
  };

  const handleFinish = async () => {
    console.log(stepOneData, "stepOneData");
    const data = {
      id_creador: localStorage.getItem("id_usuario"),
      nombre: stepOneData.name,
      descripcion: stepOneData.descripcion,
      categoria: stepTwoData,
      hora_inicio: stepOneData.desde,
      hora_fin: stepOneData.hasta,
      fecha: stepOneData.fecha,
      idioma: stepOneData.idioma,
      privacidad: stepOneData.privacidad,
      modalidad: stepOneData.modalidad,
      url_evento: stepOneData.url,
      direccion: adressData,
      ...locationData,
    };
    try {
      const response = await axios.post(
        `${import.meta.env.VITE_BACKEND_URL}/api/event/create`,
        data
      );
      if (response.status == 200) {
        const id_evento = response.data.id_evento;
        if (imageData) {
          console.log("El evento se ha creado correctamente", response);
          const formData = new FormData();
          formData.append("id", localStorage.getItem("id_usuario"));
          formData.append("file", imageData);
          try {
            const response_img = await axios.post(
              `${
                import.meta.env.VITE_BACKEND_URL
              }/api/event/upload?id=${id_evento}`,
              formData,
              {
                headers: {
                  "Content-Type": "multipart/form-data",
                },
              }
            );
            if (response_img.status == 200) {
              console.log("La imagen se ha ingresado correctamente");
            }
          } catch (error) {
            console.error("Error al subir la imagen", error);
          }
        } else {
          try {
            const response_img = await axios.post(
              `${
                import.meta.env.VITE_BACKEND_URL
              }/api/event/upload_default?id=${id_evento}`
            );
            if (response_img.status == 200) {
              console.log("La imagen se ha ingresado correctamente");
            }
          } catch (error) {
            console.error("Error al subir la imagen", error);
          }
        }
        if (stepOneData.lista && stepOneData.lista.length > 0) {
          try {
            const queryParams = stepOneData.lista
              .map((email) => `q=${encodeURIComponent(email)}`)
              .join("&");
            const url = `${
              import.meta.env.VITE_BACKEND_URL
            }/api/event/guests?event_id=${id_evento}&${queryParams}`;
            const response = await axios.post(url);
            console.log("Respuesta del servidor:", response.data);
          } catch (error) {
            console.error("Error al ingresar los invitados:", error);
          }
        }
      }
    } catch (error) {
      console.error("Error al crear el evento:", error);
    }
  };

  return (
    <div className="p-4 bg-white rounded-lg shadow-md mt-5 mx-48">
      <div data-hs-stepper="">
        <ul className="relative flex flex-row justify-between gap-x-2">
          {[
            { step: 1, name: "Detalles generales" },
            { step: 2, name: "Categoría" },
            { step: 3, name: "Imagen y lugar" },
          ].map(({ step: currentStep, name }) => (
            <li
              key={currentStep}
              className={`flex items-center gap-x-2 group ${
                currentStep === step
                  ? "hs-stepper-active:bg-blue-600 hs-stepper-active:text-white"
                  : ""
              } ${
                currentStep < step
                  ? "hs-stepper-completed:bg-teal-500 hs-stepper-completed:group-focus:bg-teal-600"
                  : ""
              }`}
              data-hs-stepper-nav-item={`{"index": ${currentStep}}`}
            >
              <span className="min-w-7 min-h-7 group inline-flex items-center text-xs align-middle">
                <span
                  className={`size-7 flex justify-center items-center flex-shrink-0 font-bold text-gray-800 ${
                    currentStep === step ? "bg-violet-400" : "bg-gray-200"
                  }`}
                >
                  {currentStep}
                </span>
                <span className="ms-2 text-sm font-medium text-gray-800">
                  {name}
                </span>
              </span>
              <div className="w-full h-px flex-1 bg-gray-200 group-last:hidden"></div>
            </li>
          ))}
        </ul>

        <div className="mt-5 sm:mt-8">
          {[1, 2, 3].map((index) => (
            <div
              key={index}
              className="p-4 h-max bg-gray-50 flex justify-center items-center border border-dashed border-gray-200 rounded-xl"
              data-hs-stepper-content-item={`{"index": ${index}}`}
              style={{ display: index === step ? "block" : "none" }}
            >
              {index === 1 && eventData && (
                <StepOne
                  modalidad={eventData.modalidad}
                  idioma={eventData.idioma}
                  privacidad={eventData.privacidad}
                  onUpdate={setStepOneData}
                />
              )}
              {index === 2 && eventData && (
                <StepTwo
                  categorias={eventData.categoria}
                  onChange={(data) => setStepTwoData(data)}
                />
              )}
              {index === 3 && (
                <StepThree
                  modalidad={stepOneData.modalidad}
                  onLocationSelected={(location) => setLocationData(location)}
                  onAdressSelected={(address) => setAddressData(address)}
                  onImageUpload={(image) => setImageData(image)}
                />
              )}
            </div>
          ))}
          <div className="mt-5 flex justify-between items-center gap-x-2">
            <button
              disabled={step === 1}
              type="button"
              className="py-2 px-3 inline-flex items-center gap-x-1 text-sm font-medium border border-gray-200 bg-white text-gray-800 shadow-sm hover:bg-gray-50 hover:shadow-sm disabled:opacity-50 disabled:pointer-events-none"
              data-hs-stepper-back-btn=""
              onClick={handleBack}
            >
              Atrás
            </button>
            <button
              type="button"
              className="py-2 px-3 inline-flex items-center gap-x-1 text-sm font-semibold border border-transparent bg-violet-400 text-white hover:bg-violet-500 hover:shadow-md disabled:opacity-50 disabled:pointer-events-none"
              data-hs-stepper-next-btn=""
              onClick={handleNext}
              style={{ display: step === 3 ? "none" : "inline-flex" }}
            >
              Siguiente
            </button>
            {step === 3 && (
              <button
                type="button"
                className="py-2 px-3 inline-flex items-center gap-x-1 text-sm font-semibold border border-transparent bg-violet-400 text-white hover:bg-violet-500 disabled:opacity-50 disabled:pointer-events-none"
                data-hs-stepper-finish-btn=""
                onClick={handleFinish}
              >
                Crear evento
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default EventWizard;
