// AuthCallbackPage.tsx
import { Card, CardContent } from "@/components/ui/card";
import { apiClient } from "@/lib/axios";
import { useUser, useAuth } from "@clerk/clerk-react";
import { Loader } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";

const AuthCallbackPage = () => {
  const { isLoaded, user } = useUser();
  const { getToken } = useAuth();
  const navigate = useNavigate();
  const syncAttempted = useRef(false);
  const [userData, setUserData] = useState(() => {
    // Récupérer les données depuis le localStorage
    const saved = localStorage.getItem('userRegistrationData');
    return saved ? JSON.parse(saved) : null;
  });

  useEffect(() => {
    const syncUser = async () => {
      // 1. Check basic conditions
      if (!isLoaded || !user || syncAttempted.current) return;

      try {
        syncAttempted.current = true;
        const token = await getToken();

        // 2. Build the payload for backend sync
        const basePayload = {
          firstName: user.firstName,
          lastName: user.lastName,
          imageUrl: user.imageUrl,
          email: user.primaryEmailAddress?.emailAddress,
        };

        const payload = userData ? {
          // New user synchronization (using stored CIN/RIB)
          ...basePayload,
          cin: userData.cin,
          rib: userData.rib,
          // NOTE: Role is assumed to be 'Beneficiaire' for new signups based on AuthPage logic
        } : {
          // Existing user (CIN/RIB are sent as null, backend should fetch them)
          ...basePayload,
          cin: null, 
          rib: null,
        };

        await apiClient.post(
          "/auth/callback",
          payload,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        // 3. Clean up and determine FINAL REDIRECTION target
        if (userData) {
          localStorage.removeItem('userRegistrationData');
        }

        // Redirect beneficiaries to their dashboard (single destination)
        navigate("/beneficiary", { replace: true });
        
      } catch (error) {
        console.error("Erreur pendant la synchronisation /auth/callback", error);
        // Even on backend error, still redirect to beneficiary since user is authenticated in Clerk
        navigate("/beneficiary", { replace: true });
      }
    };

    // If the user is already signed in (user object exists), sync and redirect immediately.
    // Otherwise, wait for Clerk to finish loading.
    if (isLoaded && user && !syncAttempted.current) {
        syncUser();
    } else if (isLoaded && !user) {
        // If loaded but no user, redirect them to the auth page
        navigate("/auth", { replace: true });
    }
    
  }, [isLoaded, user, getToken, navigate, userData]);

  // While processing, show the loading screen
  return (
    <div className="h-screen w-full bg-white flex items-center justify-center">
      <Card className="w-[90%] max-w-md bg-zinc-900 border-zinc-800">
        <CardContent className="flex flex-col items-center gap-4 pt-6">
          <Loader className="size-6 text-emerald-500 animate-spin" />
          <h3 className="text-zinc-400 text-xl font-bold">Connexion en cours</h3>
          <p className="text-zinc-400 text-sm">Synchronisation...</p>
        </CardContent>
      </Card>
    </div>
  );
};

export default AuthCallbackPage;