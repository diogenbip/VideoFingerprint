import { useCallback } from "react";
import Particles from "react-tsparticles";
import { loadConfettiPreset } from "tsparticles-preset-confetti";
import { Engine, ISourceOptions } from "tsparticles-engine";

const Confetti = () => {
  const particlesInit = useCallback(async (engine: Engine) => {
    await loadConfettiPreset(engine);
  }, []);

  const options: ISourceOptions = {
    preset: "confetti",
    particles: {
      shape: {
        type: "square"
      }
    }
  };

  return <Particles init={particlesInit} options={options} />;
};

export default Confetti;