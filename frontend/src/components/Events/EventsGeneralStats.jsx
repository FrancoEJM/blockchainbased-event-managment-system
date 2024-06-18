import React, { useEffect, useState } from "react";
import axios from "axios";
import GeneralGenderGraph from "./GeneralGenderGraph";
import GeneralAgeGraph from "./GeneralAgeGraph";
import GeneralAttendeeStats from "./GeneralAttendeeStats";

const EventsGeneralStats = () => {
  const [userId, setUserId] = useState(null);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUserId = async () => {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get(
          `${import.meta.env.VITE_BACKEND_URL}/api/users/me`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        setUserId(response.data.id_usuario);
      } catch (err) {
        setError("Error fetching user ID");
        console.error(err);
      }
    };

    fetchUserId();
  }, []);

  useEffect(() => {
    if (userId !== null) {
      const fetchUserStats = async () => {
        try {
          const response = await axios.get(
            `${import.meta.env.VITE_BACKEND_URL}/api/user/stats`,
            {
              params: { user_id: userId },
            }
          );
          setStats(response.data);
          setLoading(false);
        } catch (err) {
          setError("Error fetching user stats");
          console.error(err);
          setLoading(false);
        }
      };

      fetchUserStats();
    }
  }, [userId]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div>
      <div className="flex items-start justify-center h-screen mt-10">
        <div className="bg-white w-full max-w-5xl px-10 py-10 shadow-lg border-2 border-gray-200">
          <h1 className="text-2xl font-semibold text-center">
            Felicidades, tus eventos han alcanzado a {stats.length} asistentes
          </h1>
          <div className="grid grid-cols-9 gap-4 mt-5">
            <div className="col-span-2">
              <div className="flex items-center justify-center ">Género</div>
              <GeneralGenderGraph gender_stats={stats} />
            </div>
            <div className="col-span-5">
              <div className="flex items-center justify-center ">Edad</div>
              <GeneralAgeGraph age_stats={stats} />
            </div>
            <div className="col-span-2 ml-3">
              <div className="flex items-center justify-center">
                Asistentes por evento
              </div>
              <GeneralAttendeeStats attendee_stats={stats} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EventsGeneralStats;
