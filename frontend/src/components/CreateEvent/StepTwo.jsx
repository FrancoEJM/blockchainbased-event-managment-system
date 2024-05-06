/* eslint-disable react/prop-types */
import { useState } from "react";
import arte from "../../assets/categorias/arte_y_cultura.png";
import deportes from "../../assets/categorias/deportes.png";
import educacion from "../../assets/categorias/educacion.png";
import entretenimiento from "../../assets/categorias/entretenimiento.png";
import gastronomia from "../../assets/categorias/gastronomia.png";
import musica from "../../assets/categorias/musica.png";
import negocios from "../../assets/categorias/negocios.png";
import tecnologia from "../../assets/categorias/tecnologia.png";
import viajes from "../../assets/categorias/viajes.png";

function StepTwo({ categorias, onChange }) {
  const [selectedCategory, setSelectedCategory] = useState(null);
  const imagenes = [
    arte,
    deportes,
    educacion,
    entretenimiento,
    gastronomia,
    musica,
    negocios,
    tecnologia,
    viajes,
  ];

  const categories = categorias.map((categoria, index) => ({
    id: categoria.id_categoria,
    name: categoria.descripcion,
    image: imagenes[index],
  }));

  const handleCategoryClick = (categoryId) => {
    setSelectedCategory(categoryId);
    onChange(categoryId);
  };

  return (
    <div className="grid grid-cols-3 gap-4">
      {categories.map((category) => (
        <div
          key={category.id}
          className={`${
            selectedCategory === category.id
              ? "bg-violet-300 shadow-2xl"
              : "bg-gray-200"
          } shadow-md p-4 flex flex-col items-center justify-center text-center cursor-pointer`}
          onClick={() => handleCategoryClick(category.id)}
        >
          <img
            src={category.image}
            alt={category.name}
            className="w-24 h-24 object-cover mb-2"
          />
          <span className="text-md font-medium font-mono">{category.name}</span>
        </div>
      ))}
    </div>
  );
}

export default StepTwo;
