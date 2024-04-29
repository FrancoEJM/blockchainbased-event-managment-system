import RegisterLayout from "../../components/Register/RegisterLayout";

function Register() {
  return (
    <>
      <div className="flex w-full h-screen">
        <div className="w-full flex items-center justify-center lg:w-1/2">
          <RegisterLayout />
        </div>
        <div className="bg-gray-200"></div>
      </div>
    </>
  );
}
export default Register;
