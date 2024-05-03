import { useState } from "react";
import StepOne from "./StepOne";
import StepTwo from "./StepTwo";
import StepThree from "./StepThree";

const EventWizard = () => {
  const [step, setStep] = useState(1);

  const handleNext = () => {
    if (step < 3) {
      setStep(step + 1);
    }
  };

  const handleBack = () => {
    if (step > 1) {
      setStep(step - 1);
    }
  };

  const handleFinish = () => {
    // Handle finish logic here
  };

  return (
    <div className="p-4 bg-white rounded-lg shadow-md mt-5 mx-48">
      <div data-hs-stepper="">
        <ul className="relative flex flex-row gap-x-2">
          {[1, 2, 3].map((index) => (
            <li
              key={index}
              className={`flex items-center gap-x-2 shrink basis-0 flex-1 group ${
                index === step
                  ? "hs-stepper-active:bg-blue-600 hs-stepper-active:text-white"
                  : ""
              } ${
                index < step
                  ? "hs-stepper-completed:bg-teal-500 hs-stepper-completed:group-focus:bg-teal-600"
                  : ""
              }`}
              data-hs-stepper-nav-item={`{"index": ${index}}`}
            >
              <span className="min-w-7 min-h-7 group inline-flex items-center text-xs align-middle">
                <span className="size-7 flex justify-center items-center flex-shrink-0 bg-gray-100 font-medium text-gray-800 rounded-full group-focus:bg-gray-200">
                  {index}
                </span>
                <span className="ms-2 text-sm font-medium text-gray-800">
                  Step
                </span>
              </span>
              <div className="w-full h-px flex-1 bg-gray-200 group-last:hidden"></div>
            </li>
          ))}
        </ul>
        <div className="mt-5 sm:mt-8">
          {[1, 2, 3].map((index) => (
            <div
              key={index}
              className="p-4 h-max bg-gray-50 flex justify-center items-center border border-dashed border-gray-200 rounded-xl"
              data-hs-stepper-content-item={`{"index": ${index}}`}
              style={{ display: index === step ? "block" : "none" }}
            >
              {index === 1 && <StepOne />}
              {index === 2 && <StepTwo />}
              {index === 3 && <StepThree />}
            </div>
          ))}
          <div className="mt-5 flex justify-between items-center gap-x-2">
            <button
              disabled={step === 1}
              type="button"
              className="py-2 px-3 inline-flex items-center gap-x-1 text-sm font-medium rounded-lg border border-gray-200 bg-white text-gray-800 shadow-sm hover:bg-gray-50 disabled:opacity-50 disabled:pointer-events-none"
              data-hs-stepper-back-btn=""
              onClick={handleBack}
            >
              Back
            </button>
            <button
              type="button"
              className="py-2 px-3 inline-flex items-center gap-x-1 text-sm font-semibold rounded-lg border border-transparent bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50 disabled:pointer-events-none"
              data-hs-stepper-next-btn=""
              onClick={handleNext}
              style={{ display: step === 3 ? "none" : "inline-flex" }}
            >
              Next
            </button>
            {step === 3 && (
              <button
                type="button"
                className="py-2 px-3 inline-flex items-center gap-x-1 text-sm font-semibold rounded-lg border border-transparent bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50 disabled:pointer-events-none"
                data-hs-stepper-finish-btn=""
                onClick={handleFinish}
              >
                Finish
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default EventWizard;
