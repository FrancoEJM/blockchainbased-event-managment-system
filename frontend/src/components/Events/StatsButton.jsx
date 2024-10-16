import { useNavigate } from "react-router-dom";
import { Button } from "flowbite-react";

function StatsButton({ event_id }) {
  const navigate = useNavigate();
  const handleRedirectStats = () => {
    navigate(`/stats/${event_id}`);
  };
  return (
    <Button
      className=" ring-cyan-700 border border-gray-200 bg-white text-gray-900 focus:text-cyan-700 focus:ring-4 enabled:hover:bg-gray-100 enabled:hover:text-violet-700 dark:border-gray-600 dark:bg-transparent dark:text-gray-400 dark:enabled:hover:bg-gray-700 dark:enabled:hover:text-white"
      title="Ver estadísticas"
      onClick={handleRedirectStats}
    >
      <div className="flex items-center">
        <div className="hidden sm:block mr-1">Ver estadísticas</div>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="icon icon-tabler icon-tabler-device-desktop-analytics"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          strokeWidth="1.5"
          stroke="#2c3e50"
          fill="none"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path stroke="none" d="M0 0h24v24H0z" fill="none" />
          <path d="M3 4m0 1a1 1 0 0 1 1 -1h16a1 1 0 0 1 1 1v10a1 1 0 0 1 -1 1h-16a1 1 0 0 1 -1 -1z" />
          <path d="M7 20h10" />
          <path d="M9 16v4" />
          <path d="M15 16v4" />
          <path d="M9 12v-4" />
          <path d="M12 12v-1" />
          <path d="M15 12v-2" />
          <path d="M12 12v-1" />
        </svg>
      </div>
    </Button>
  );
}
export default StatsButton;
