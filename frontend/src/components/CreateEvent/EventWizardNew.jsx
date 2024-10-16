import React, { useState, useRef, useEffect } from "react";
import {
  Button,
  Label,
  TextInput,
  Textarea,
  Select,
  FileInput,
  Modal,
  Datepicker,
  Badge,
} from "flowbite-react";
import axios from "axios";
import { MapContainer, TileLayer, Marker, useMapEvents } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import popoverImage from "../../assets/popover.jpg";

function EventWizardNew() {
  const [openModal, setOpenModal] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [eventData, setEventData] = useState({
    categoria: [],
    modalidad: [],
    idioma: [],
    privacidad: [],
  });
  const [selectedPrivacidad, setSelectedPrivacidad] = useState("");
  const [formData, setFormData] = useState({
    nombre: "",
    descripcion: "",
    fecha: "",
    hora_inicio: "",
    hora_fin: "",
    idioma: "0",
    categoria: "0",
    privacidad: "0",
    direccion: "",
  });
  const [file, setFile] = useState(null);
  const [mapImageFile, setMapImageFile] = useState(null);
  const [markerPosition, setMarkerPosition] = useState([
    -39.833333, -73.231389,
  ]);
  const mapRef = useRef(null);

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

  const onPageChange = (page) => setCurrentPage(page);

  const handleInputChange = (e) => {
    const { id, value } = e.target;
    setFormData((prevFormData) => ({
      ...prevFormData,
      [id]: value,
    }));
  };

  const handleDateChange = (date) => {
    console.log(date);
    // Asegúrate de convertir la fecha a una cadena en formato ISO
    const fecha = date ? date.toISOString().split("T")[0] : ""; // Formato YYYY-MM-DD
    setFormData({ ...formData, fecha });
  };

  const handleFileChange = (e) => {
    if (e.target.id === "file") {
      console.log("cargado el archivo");

      setFile(e.target.files[0]);
    } else if (e.target.id === "file-upload") {
      setMapImageFile(e.target.files[0]);
    }
  };

  const validateStepOne = () => {
    console.log("formData.nombre: ", formData.nombre);
    console.log("formData.descripcion &&: ", formData.descripcion);
    console.log("formData.fechaDesde: ", formData.fecha);
    console.log("formData.horaDesde: ", formData.hora_inicio);
    console.log("formData.horaHasta: ", formData.hora_fin);
    console.log("formData.idioma: ", formData.idioma);
    console.log("formData.categoria: ", formData.categoria);
    console.log("formData.privacidad: ", formData.privacidad);
    console.log(
      'formData.privacidad !== "1" || file: ',
      formData.privacidad !== "1" || file
    );
    return (
      formData.nombre &&
      formData.descripcion &&
      formData.fecha &&
      formData.hora_inicio &&
      formData.hora_fin &&
      formData.idioma &&
      formData.categoria &&
      formData.privacidad &&
      (formData.privacidad !== "2" || file) // Valida que si privacidad es 'Privado' (2), el archivo esté cargado
    );
  };

  const parseCSVToJSON = (csvContent) => {
    const lines = csvContent
      .split("\n")
      .map((line) => line.trim())
      .filter((line) => line); // Elimina espacios y líneas vacías
    const headers = lines[0].split(",").map((header) => header.trim());
    const result = [];

    for (let i = 1; i < lines.length; i++) {
      const currentLine = lines[i].split(",").map((value) => value.trim());

      // Verifica que la línea tenga el mismo número de columnas que los encabezados
      if (currentLine.length === headers.length) {
        const obj = {};
        headers.forEach((header, index) => {
          obj[header] = currentLine[index];
        });
        result.push(obj);
      } else {
        console.warn(
          `La línea ${
            i + 1
          } del CSV tiene un número incorrecto de columnas y será omitida.`
        );
      }
    }

    return result;
  };

  const handleCreateEvent = async () => {
    if (!markerPosition) {
      alert("Por favor, asegúrese de seleccionar una ubicación y una imagen.");
      return;
    }
    const formatTime = (timeString) => {
      console.log(timeString);

      const [hours, minutes] = timeString.split(":");
      return `${hours}:${minutes}:00`; // Aseguramos que el formato sea HH:mm:ss
    };
    try {
      // Primero, crea el evento
      const formattedData = {
        id_creador: localStorage.id_usuario,
        nombre: formData.nombre,
        categoria: parseInt(formData.categoria, 10), // Convertir a entero
        hora_inicio: formatTime(formData.hora_inicio), // Formato de hora
        hora_fin: formatTime(formData.hora_fin), // Formato de hora
        fecha: formData.fecha, // Suponiendo que `formData.fecha` ya está en formato YYYY-MM-DD
        idioma: parseInt(formData.idioma, 10), // Convertir a entero
        privacidad: parseInt(formData.privacidad, 10), // Convertir a entero
        direccion: formData.direccion,
        descripcion: formData.descripcion,
        latitud: markerPosition[0],
        longitud: markerPosition[1],
      };
      const response = await axios.post(
        `${import.meta.env.VITE_BACKEND_URL}/api/event/create`,
        formattedData
      );
      const event_id = response.data.id_evento;
      console.log(event_id);

      if (!mapImageFile) {
        await axios.post(
          `${
            import.meta.env.VITE_BACKEND_URL
          }/api/event/upload_default?id=${event_id}`
        );
      } else {
        // Luego, carga la imagen
        const formDataForImage = new FormData();
        formDataForImage.append("file", mapImageFile); // Cambiar a "file" para coincidir con el backend

        await axios.post(
          `${import.meta.env.VITE_BACKEND_URL}/api/event/upload?id=${event_id}`,
          formDataForImage,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );
        console.log("Imagen cargada exitosamente");
      }

      // Finalmente, envía los correos a los invitados
      if (file) {
        // Leer el archivo CSV
        const csvContent = await file.text();
        const guests = parseCSVToJSON(csvContent); // Asumiendo que tienes una función para convertir el CSV a JSON
        setTimeout(async () => {
          try {
            await axios.post(
              `${
                import.meta.env.VITE_BACKEND_URL
              }/api/event/guests?event_id=${event_id}`,
              guests,
              {
                headers: {
                  "Content-Type": "application/json",
                },
              }
            );
            console.log("Correos enviados exitosamente");
          } catch (error) {
            console.error("Error sending emails:", error);
          }
        }, 0);
      }

      alert("Evento creado exitosamente.");
      setCurrentPage(1); // Regresa al primer paso
    } catch (error) {
      console.error("Error creating event:", error);
      alert("Hubo un error al crear el evento.");
    }
  };

  function LocationMarker({ setPosition }) {
    useMapEvents({
      click(event) {
        setPosition([event.latlng.lat, event.latlng.lng]);
      },
    });

    return null;
  }

  return (
    <div className="flex justify-center items-center max-h-screen mt-24">
      <div className="max-w-2xl rounded-lg overflow-hidden shadow-lg bg-white p-6">
        <div className="text-slate-700 font-semibold mb-3 text-lg">
          Crea un nuevo evento
        </div>
        {currentPage === 1 ? (
          <form className="flex flex-col gap-4">
            {/* Nombre */}
            <div>
              <Label htmlFor="nombre" value="Nombre" />
              <TextInput
                id="nombre"
                type="text"
                placeholder="Ingrese el nombre del evento"
                required
                value={formData.nombre}
                onChange={handleInputChange}
                maxLength={70}
              />
            </div>

            {/* Descripción */}
            <div>
              <Label htmlFor="descripcion" value="Descripción" />
              <Textarea
                id="descripcion"
                placeholder="Ingrese la descripción del evento"
                required
                rows={4}
                value={formData.descripcion}
                onChange={handleInputChange}
                maxLength={200}
              />
            </div>

            {/* Fecha Desde */}
            <div className="flex gap-2">
              <div className="flex-2">
                <Label htmlFor="fecha" value="Fecha" />
                <Datepicker
                  id="fecha"
                  placeholder="Seleccione la fecha"
                  onSelectedDateChanged={(date) => handleDateChange(date)}
                  required
                  language="es-ES"
                />
              </div>

              {/* Hora Desde */}
              <div className="flex-1">
                <Label htmlFor="hora_inicio" value="Desde" />
                <TextInput
                  id="hora_inicio"
                  type="time"
                  placeholder="Ingrese la hora de inicio"
                  required
                  value={formData.hora_inicio}
                  onChange={handleInputChange}
                />
              </div>

              {/* Hora Hasta */}
              <div className="flex-1">
                <Label htmlFor="hora_fin" value="Hasta" />
                <TextInput
                  id="hora_fin"
                  type="time"
                  placeholder="Ingrese la hora de finalización"
                  required
                  value={formData.hora_fin}
                  onChange={handleInputChange}
                />
              </div>
            </div>

            {/* Idioma y Categoría */}
            <div className="flex gap-4">
              {/* Idioma */}
              <div className="flex-1">
                <Label htmlFor="idioma" value="Idioma" />
                <Select
                  id="idioma"
                  required
                  value={formData.idioma}
                  onChange={handleInputChange}
                >
                  <option value="0" disabled>
                    Seleccione un idioma
                  </option>
                  {eventData.idioma.map((idioma) => (
                    <option key={idioma.id_idioma} value={idioma.id_idioma}>
                      {idioma.descripcion}
                    </option>
                  ))}
                </Select>
              </div>

              {/* Categoría */}
              <div className="flex-1">
                <Label htmlFor="categoria" value="Categoría" />
                <Select
                  id="categoria"
                  required
                  value={formData.categoria}
                  onChange={handleInputChange}
                  placeholder="Seleccione una categoría"
                >
                  <option value="0" disabled>
                    Seleccione una categoría
                  </option>
                  {eventData.categoria.map((categoria) => (
                    <option
                      key={categoria.id_categoria}
                      value={categoria.id_categoria}
                    >
                      {categoria.descripcion}
                    </option>
                  ))}
                </Select>
              </div>
            </div>

            {/* Privacidad y Cargador de archivo */}
            <div className="flex gap-4 items-start mt-1">
              {/* Privacidad */}
              <div className="flex-2">
                <Label htmlFor="privacidad" value="Privacidad" />
                <Select
                  id="privacidad"
                  required
                  value={formData.privacidad}
                  onChange={(e) => {
                    setSelectedPrivacidad(e.target.value);
                    handleInputChange(e);
                  }}
                  className={selectedPrivacidad === "1" ? "w-1/2" : ""} // Clases dinámicas basadas en selectedPrivacidad
                >
                  <option value="0" disabled>
                    Seleccione una opción
                  </option>
                  {eventData.privacidad.map((priv) => (
                    <option key={priv.id_privacidad} value={priv.id_privacidad}>
                      {priv.descripcion}
                    </option>
                  ))}
                </Select>
              </div>

              {/* Archivo */}
              {selectedPrivacidad === "2" && (
                <div className="flex-3">
                  <div>
                    <Label htmlFor="file" value="Subir archivo CSV" />
                  </div>
                  <div className="flex items-center space-x-3">
                    {" "}
                    {/* Flex para alinear el FileInput y el Button */}
                    <FileInput
                      id="file"
                      helperText="Cargar archivo de asistentes"
                      onChange={handleFileChange}
                      accept=".csv"
                      className="flex-2"
                    />
                    <Button
                      className="flex flex-1 items-center justify-center mb-2 w-8 h-8 rounded-full bg-purple-500 text-white text-lg font-bold"
                      color="purple"
                      onClick={() => setOpenModal(true)}
                    >
                      <span className="text-bold">?</span>
                    </Button>
                  </div>
                </div>
              )}
            </div>

            {/* Botón Siguiente */}
            <div className="flex justify-end mt-4">
              <Button
                onClick={() => {
                  if (validateStepOne()) onPageChange(2);
                  else
                    alert(
                      "Por favor complete todos los campos antes de continuar."
                    );
                }}
              >
                Siguiente
              </Button>
            </div>
          </form>
        ) : (
          <div className="w-full max-w-3xl mx-auto">
            {/* Dirección */}
            <div className="flex mb-3">
              <div className="flex-1">
                <Label htmlFor="direccion" value="Dirección" />
                <TextInput
                  id="direccion"
                  type="text"
                  placeholder="Ingrese la dirección del evento"
                  required
                  value={formData.direccion}
                  onChange={handleInputChange}
                  maxLength={70}
                />
              </div>
            </div>

            {/* Cargar Imagen */}
            <div className="flex">
              <div className="flex-1">
                <Label
                  htmlFor="file-upload"
                  value="Ingrese una imagen para el evento"
                />
                <FileInput
                  id="file-upload"
                  sizing="sm"
                  onChange={handleFileChange}
                />
              </div>
            </div>

            {/* Mapa para Selección de Ubicación */}
            <div className="flex my-3">
              <div className="flex-1">
                <MapContainer
                  center={[-39.833333, -73.231389]}
                  zoom={13}
                  scrollWheelZoom={true}
                  className="w-96"
                  style={{ height: "400px" }}
                  whenCreated={(mapInstance) => {
                    mapRef.current = mapInstance;
                  }}
                >
                  <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                  />
                  <LocationMarker setPosition={setMarkerPosition} />
                  <Marker position={markerPosition} />
                </MapContainer>
              </div>
            </div>

            {/* Botones de Navegación */}
            <div className="flex justify-between">
              <Button onClick={() => onPageChange(1)}>Anterior</Button>
              <Button onClick={handleCreateEvent}>Crear</Button>
            </div>
          </div>
        )}
      </div>

      {/* Modal */}
      <Modal show={openModal} onClose={() => setOpenModal(false)}>
        <Modal.Header>Información sobre el archivo CSV</Modal.Header>
        <Modal.Body>
          <div className="flex gap-4">
            <div className="flex-1">
              <p className="text-base leading-relaxed text-gray-500 dark:text-gray-400">
                Para gestionar las invitaciones de tus invitados, es necesario
                que cargues un archivo .csv siguiendo el formato mostrado en la
                imagen. A cada persona incluida en este archivo se le enviará un
                correo electrónico con un código QR privado, que podrás escanear
                en la entrada del evento.
              </p>
              <br />
              <p className="text-base leading-relaxed text-gray-500 dark:text-gray-400">
                Si desconoces el género de algún invitado, puedes utilizar la
                letra "D" (desconocido). Además, la fecha de nacimiento es
                opcional y puede dejarse en blanco.
              </p>
              <br />
              <p className="text-base leading-relaxed text-gray-500 dark:text-gray-400">
                Archivo .csv de ejemplo:
              </p>
            </div>
          </div>
          <img
            src={popoverImage}
            className="w-full h-48 object-contain"
            alt="Información del archivo"
          />
        </Modal.Body>
        <Modal.Footer>
          <Button onClick={() => setOpenModal(false)}>Cerrar</Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
}

export default EventWizardNew;
