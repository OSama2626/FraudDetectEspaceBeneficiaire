import React from 'react';
import { Link } from 'react-router-dom';

interface AuthLayoutProps {
  children: React.ReactNode;
}

const AuthLayout: React.FC<AuthLayoutProps> = ({ children }) => {
  return (
    <div className="bg-gray-100 min-h-screen">
      <header className="bg-white shadow-md">
        <div className="container mx-auto px-6 py-4">
          <Link to="/" className="text-3xl font-bold text-gray-800">DetectFraud</Link>
        </div>
      </header>
      <main className="flex justify-center items-center py-20">
        {children}
      </main>
    </div>
  );
};

export default AuthLayout;