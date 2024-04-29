import RegisterForm from "./RegisterForm";

function RegisterLayout() {
  return (
    <div className="bg-white px-10 py-20 border-2 border-gray-200 shadow-lg">
      <h1 className="text-5xl font-semibold">Registrarse</h1>
      <RegisterForm />
    </div>
  );
}
export default RegisterLayout;
