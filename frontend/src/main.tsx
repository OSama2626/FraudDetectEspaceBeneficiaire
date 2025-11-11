<<<<<<< HEAD
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { ClerkProvider } from '@clerk/clerk-react'

const PUBLISHABLE_KEY = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY
=======
// FraudDetect-feature-auth/frontend/src/main.tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import { ClerkProvider } from '@clerk/clerk-react';
import App from './App';
import './index.css';

// Récupérez la clé depuis les variables d'environnement
const PUBLISHABLE_KEY = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY;

>>>>>>> 11d76b0be2cf1a1493e6f0021a77a5054f6026a8
if (!PUBLISHABLE_KEY) {
  throw new Error("Missing Publishable Key");
}
<<<<<<< HEAD
createRoot(document.getElementById('root')!).render(
  <StrictMode>
=======

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
>>>>>>> 11d76b0be2cf1a1493e6f0021a77a5054f6026a8
    <ClerkProvider publishableKey={PUBLISHABLE_KEY}>
      <App />
    </ClerkProvider>
  </React.StrictMode>
);