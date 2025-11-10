// FraudDetect-feature-auth/frontend/src/App.tsx

import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import AuthPage from './pages/auth/AuthPage';
import AuthCallbackPage from './pages/auth-callback/AuthCallbackPage';
import ProfilePage from './pages/profile/ProfilePage';
// 4. (Optionnel) Importez votre layout principal si vous en avez un
// import MainLayout from './components/layout/MainLayout'; 

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/auth"
          element={
              <AuthPage />
          }
        />

        {/* Page de callback pour les connexions OAuth (Google, etc.)
        */}
        <Route path="/auth-callback" element={<AuthCallbackPage />} />


        {/* Page de profil utilisateur
        */}
        <Route
          path="/profile"
          element={
<ProfilePage />
          }
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;