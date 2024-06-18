import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const groupAges = (ages) => {
  const ageGroups = {
    "0-17": 0,
    "18-23": 0,
    "24-35": 0,
    "36-47": 0,
    "48-60": 0,
    "60+": 0,
  };

  ages.forEach((age) => {
    if (age >= 0 && age <= 17) {
      ageGroups["0-17"]++;
    } else if (age >= 18 && age <= 23) {
      ageGroups["18-23"]++;
    } else if (age >= 24 && age <= 35) {
      ageGroups["24-35"]++;
    } else if (age >= 36 && age <= 47) {
      ageGroups["36-47"]++;
    } else if (age >= 48 && age <= 60) {
      ageGroups["48-60"]++;
    } else {
      ageGroups["60+"]++;
    }
  });

  const data = Object.keys(ageGroups).map((range, index) => ({
    id: index,
    name: range,
    Participantes: ageGroups[range],
  }));

  return data;
};

function GeneralAgeGraph({ age_stats }) {
  const ages = age_stats.map((participant) => participant.edad);
  const data = groupAges(ages);

  return (
    <div style={{ width: "100%", height: 350 }}>
      <ResponsiveContainer>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="Participantes" fill="#8884d8" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default GeneralAgeGraph;
