import React from 'react';
import { Link } from 'react-router-dom';

const LandingPage: React.FC = () => {
  return (
    <div className="bg-gray-100 min-h-screen">
      {/* Header */}
      <header className="bg-white shadow-md">
        <div className="container mx-auto px-6 py-4 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-800">DetectFraud</h1>
          <nav>
            <Link to="/Login" className="text-gray-600 hover:text-gray-800 mx-4">Sign In</Link>
            <Link to="/signup" className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600">Sign Up</Link>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="bg-blue-600 text-white py-20">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-4xl font-bold mb-4">Advanced Check Fraud Detection</h2>
          <p className="text-lg mb-8">Protect your financial institution from fraudulent checks with our cutting-edge AI-powered solution.</p>
          <Link to="/sign-up" className="bg-white text-blue-600 px-6 py-3 rounded-md font-bold hover:bg-gray-200">Get Started</Link>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20">
        <div className="container mx-auto px-6">
          <h3 className="text-3xl font-bold text-center text-gray-800 mb-12">Key Features</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h4 className="text-xl font-bold text-gray-800 mb-2">Real-Time Analysis</h4>
              <p className="text-gray-600">Our system analyzes checks in real-time to detect any signs of fraud instantly.</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h4 className="text-xl font-bold text-gray-800 mb-2">AI-Powered Detection</h4>
              <p className="text-gray-600">Leverage the power of artificial intelligence to identify even the most sophisticated fraud patterns.</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h4 className="text-xl font-bold text-gray-800 mb-2">Comprehensive Reporting</h4>
              <p className="text-gray-600">Get detailed reports and alerts to stay on top of all potential security threats.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action Section */}
      <section className="bg-gray-200 py-20">
        <div className="container mx-auto px-6 text-center">
          <h3 className="text-3xl font-bold text-gray-800 mb-4">Ready to Secure Your Bank?</h3>
          <p className="text-lg text-gray-600 mb-8">Join the leading financial institutions that trust DetectFraud to protect their assets.</p>
          <Link to="/sign-up" className="bg-blue-500 text-white px-6 py-3 rounded-md font-bold hover:bg-blue-600">Sign Up Now</Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-white py-6">
        <div className="container mx-auto px-6 text-center text-gray-600">
          <p>&copy; {new Date().getFullYear()} DetectFraud. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;