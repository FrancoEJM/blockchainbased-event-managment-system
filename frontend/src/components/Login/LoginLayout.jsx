import LoginCube from "../../assets/LoginCube.png";
import LoginForm from "./LoginForm";

function LoginLayout() {
  return (
    <div className="flex w-full h-screen">
      <div className="w-full flex items-center justify-center">
        <div className="bg-white px-10 py-10 shadow-lg border-2 border-gray-200">
          <h1 className="text-5xl font-semibold text-center">Bienvenido</h1>
          <div className="bg-transparent flex justify-center mt-5">
            <div className="max-w-16">
              <img
                className="object-cover w-full"
                src={LoginCube}
                alt="LoginCube"
              />
            </div>
          </div>
          <LoginForm />
        </div>
      </div>
    </div>
  );
}

export default LoginLayout;
