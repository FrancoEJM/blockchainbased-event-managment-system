import React, { useState } from "react";
import { Scanner } from "@yudiel/react-qr-scanner";
import axios from "axios";
import { Button } from "flowbite-react";
import { IoIosQrScanner } from "react-icons/io";

function QrReaderButton() {
  const [qrData, setQrData] = useState("");
  const [isScanning, setIsScanning] = useState(false);
  const [error, setError] = useState(null);

  const handleScan = (detectedCodes) => {
    if (detectedCodes && detectedCodes.length > 0) {
      const data = detectedCodes[0].rawValue;
      setQrData(data);
      try {
        const userData = JSON.parse(data.replace(/'/g, '"'));
        validateUser(userData);
        alert("Data del código QR leído:\n" + data);
        setIsScanning(false);
      } catch (error) {
        console.error("Error al parsear JSON:", error, data);
        alert("Error al parsear JSON. Verifica que el código QR sea válido.");
      }
    }
  };

  const handleError = (error) => {
    console.error("Error al escanear código QR:", error);
    setError(
      "No se pudo acceder a la cámara. Asegúrate de que los permisos estén habilitados."
    );
  };

  const validateUser = async ({ event_id, email, token }) => {
    try {
      const response = await axios.post(
        `${import.meta.env.VITE_BACKEND_URL}/api/user/validate_by_qr`,
        {},
        {
          params: {
            event_id: event_id,
            email: email,
            token: token,
          },
        }
      );
      if (response.status === 200) {
        console.log("response", response);
      }
    } catch (error) {
      console.error("Error validating user:", error);
    }
  };

  const handleStartScan = async () => {
    if (!navigator.mediaDevices || !navigator.mediaDevices.enumerateDevices) {
      setError("El navegador no soporta acceso a dispositivos de medios.");
      return;
    }

    try {
      const devices = await navigator.mediaDevices.enumerateDevices();
      const hasVideoInput = devices.some(
        (device) => device.kind === "videoinput"
      );

      if (!hasVideoInput) {
        throw new Error("No se encontró ningún dispositivo de cámara.");
      }

      setIsScanning(true);
    } catch (error) {
      console.error("Error al iniciar el escaneo:", error);
      setError(
        error.message || "Error al iniciar el escaneo. Inténtalo de nuevo."
      );
    }
  };

  return (
    <div>
      {isScanning ? (
        <Scanner
          onScan={handleScan}
          onError={handleError}
          scanDelay={300}
          constraints={{
            video: {
              facingMode: "environment",
              width: { ideal: 1280 },
              height: { ideal: 720 },
            },
          }}
          style={{ width: "100%" }}
        />
      ) : (
        <Button
          onClick={handleStartScan}
          className=" mt-6 ring-cyan-700 border border-gray-200 bg-white text-gray-900 focus:text-cyan-700 focus:ring-4 enabled:hover:bg-gray-100 enabled:hover:text-violet-700 dark:border-gray-600 dark:bg-transparent dark:text-gray-400 dark:enabled:hover:bg-gray-700 dark:enabled:hover:text-white"
        >
          <div className="flex items-center">
            <div className="hidden sm:block mr-1">Escanear QR</div>
            <IoIosQrScanner size={32} />
          </div>
        </Button>
      )}
      {error && <p style={{ color: "red" }}>{error}</p>}
      <br />
      <p>{qrData}</p>
    </div>
  );
}

export default QrReaderButton;
