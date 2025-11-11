import { Card, CardContent } from "@/components/ui/card";
import { apiClient } from "@/lib/axios"; // <== (1) Utilise votre apiClient
import { useUser } from "@clerk/clerk-react";
import { Loader } from "lucide-react";
import { useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";

const AuthCallbackPage = () => {
	const { isLoaded, user } = useUser();
	const navigate = useNavigate();
	const syncAttempted = useRef(false);

	useEffect(() => {
		const syncUser = async () => {
			if (!isLoaded || !user || syncAttempted.current) return;

			try {
				syncAttempted.current = true;
				
				// (2) Appelle la NOUVELLE route de votre backend FastAPI
				await apiClient.post("/api/v1/auth/callback", {
					// Le backend utilise l'ID du token, mais on envoie
					// les données pour remplir la base de données
					firstName: user.firstName,
					lastName: user.lastName,
					imageUrl: user.imageUrl,
					email: user.primaryEmailAddress?.emailAddress // (3) Envoie l'email
				});
			} catch (error) {
				console.error("Erreur pendant la synchronisation /api/v1/auth/callback", error);
			} finally {
				// (4) Redirige vers la page d'accueil de FraudDetect
				navigate("/"); 
			}
		};

		syncUser();
	}, [isLoaded, user, navigate]);

	return (
		<div className='h-screen w-full bg-white flex items-center justify-center'>
			<Card className='w-[90%] max-w-md bg-zinc-900 border-zinc-800'>
				<CardContent className='flex flex-col items-center gap-4 pt-6'>
					<Loader className='size-6 text-emerald-500 animate-spin' />
					<h3 className="text-zinc-400 text-xl font-bold">Connexion en cours</h3>
					<p className="text-zinc-400 text-sm">Synchronisation...</p>
				</CardContent>
			</Card>
		</div>
	);
};
export default AuthCallbackPage;