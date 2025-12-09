import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import { AuthenticateWithRedirectCallback, useUser } from "@clerk/clerk-react";

// --- AUTHENTICATION IMPORTS ---
import AuthPage from './pages/auth/AuthPage';
import AuthCallbackPage from './pages/auth-callback/AuthCallbackPage';
import SignUpWithEmail from "./components/SignUpWithEmail";
import FloatingShape from "./components/FloatingShape";

// --- BENEFICIARY IMPORTS ---
import BeneficiaryLayout from './pages/beneficiary/layouts/BeneficiaryLayout';
import Dashboard from './pages/beneficiary/Dashboard';
import CheckList from './pages/beneficiary/components/CheckList';
import CheckHistory from './pages/beneficiary/components/CheckHistory';
import Notifications from './pages/beneficiary/components/Notifications';
import { BeneficiaryProvider } from './pages/beneficiary/BeneficiaryContext';


// --- ROUTE GUARD COMPONENT ---
// This component ensures only authenticated users can access the Beneficiary routes.
const ProtectedRoute = () => {
  const { isLoaded, isSignedIn } = useUser();

  if (!isLoaded) {
    // Show a loading spinner or null while checking user status
    return <div>Loading...</div>; 
  }

  // If the user is signed in, render the child routes (the BeneficiaryLayout)
  if (isSignedIn) {
    return <Outlet />;
  }

  // If the user is NOT signed in, redirect them to the authentication page
  return <Navigate to="/auth" replace />;
};


function App() {
  return (
    <Router>
      <BeneficiaryProvider>
        <Routes>
          {/* --- 1. AUTHENTICATION ROUTES --- */}
          <Route path="/sso-callback" element={<AuthenticateWithRedirectCallback signUpForceRedirectUrl={"/auth-callback"} />} />
          <Route path="/auth-callback" element={<AuthCallbackPage />} />
          <Route path="/sign-up-email" element={<div className="h-screen bg-black flex items-center justify-center"><SignUpWithEmail /></div>} />
          
          {/* Main Auth Page Route */}
          <Route 
            path="/auth" 
            element={
              <div className='min-h-screen bg-gradient-to-br from-gray-900 via-green-900 to-emerald-900 flex items-center justify-center relative overflow-hidden'>
                <FloatingShape color='bg-green-500' size='w-64 h-64' top='-5%' left='10%' delay={0} />
                <FloatingShape color='bg-emerald-500' size='w-48 h-48' top='70%' left='80%' delay={5} />
                <FloatingShape color='bg-lime-500' size='w-32 h-32' top='40%' left='-10%' delay={2} />
                <AuthPage />
              </div>
            } 
          />
          
          {/* --- 2. PROTECTED BENEFICIARY ROUTES --- */}
          <Route element={<ProtectedRoute />}>
              <Route path="/beneficiary" element={<BeneficiaryLayout />}>
                  <Route index element={<Dashboard />} />
                  <Route path="checks" element={<CheckList />} />
                  <Route path="history" element={<CheckHistory />} />
                  <Route path="notifications" element={<Notifications />} />
              </Route>
          </Route>

          {/* --- 3. FALLBACK/HOME ROUTE --- */}
          {/* Redirects the root path to the authentication page, or change to Home component if needed */}
          <Route path="/" element={<Navigate to="/auth" replace />} />

        </Routes>
      </BeneficiaryProvider>
    </Router>
  );
}

export default App;