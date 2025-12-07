import React from "react";

interface AuthImagePatternProps {
  title: string;
  subtitle: string;
}

const AuthImagePattern: React.FC<AuthImagePatternProps> = ({ title, subtitle }) => {
<<<<<<< HEAD
=======
  const images = ["/cheque.jpg"];

  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentIndex((prevIndex) => (prevIndex + 1) % images.length);
    }, 3000);
    return () => clearInterval(interval);
  }, [images.length]);

>>>>>>> feature/auth
  return (
    <div className="hidden lg:flex items-center justify-center h-full w-full relative">
      {/* Decorative gradient background instead of an external image */}
      <div className="absolute inset-0 bg-gradient-to-br from-indigo-700 via-sky-700 to-slate-900" />

      {/* subtle decorative shapes */}
      <svg className="absolute -left-20 -top-20 opacity-20" width="420" height="420" viewBox="0 0 420 420" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden>
        <defs>
          <linearGradient id="g1" x1="0" x2="1">
            <stop offset="0%" stopColor="#7c3aed" stopOpacity="0.6" />
            <stop offset="100%" stopColor="#06b6d4" stopOpacity="0.4" />
          </linearGradient>
        </defs>
        <circle cx="210" cy="210" r="140" fill="url(#g1)" />
      </svg>

      <div className="relative max-w-md text-left flex flex-col justify-end h-full pb-12 px-8 w-full">
        <h2 className="text-3xl font-extrabold mb-3 text-white drop-shadow">{title}</h2>
        <p className="text-zinc-300">{subtitle}</p>
      </div>
    </div>
  );
};

export default AuthImagePattern;
