import axios from "axios";
function EventSigningButton() {
  const handleInscription = () => {
    console.log("handleInscription");
  };
  return (
    <button
      className="bg-violet-500 hover:bg-violet-400 text-white font-bold py-2 px-4 border-b-4 border-violet-800 hover:border-violet-500 shadow-md"
      onClick={handleInscription}
    >
      + Inscribirse
    </button>
  );
}
export default EventSigningButton;
