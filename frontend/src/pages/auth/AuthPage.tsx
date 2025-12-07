// AuthPage.tsx
import { useSignIn, useSignUp, useClerk } from "@clerk/clerk-react";
import { Button } from "../../components/ui/button";
import { useState } from "react";
import { Input } from "../../components/ui/input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../../components/ui/tabs";
import PasswordStrengthMeter from "../../components/PasswordStrengthMeter";
import { FaEye, FaEyeSlash } from "react-icons/fa";
<<<<<<< HEAD
import ForgotPassword from "../../components/ForgotPassword";
import { saveUserExtra } from "../../lib/saveUserExtra";
=======
import ForgotPassword from "../../components/ForgotPassword"; 
// Les imports pour 'Select' ont été supprimés
>>>>>>> feature/auth

const AuthPage = () => {
  const { signIn, isLoaded: isSignInLoaded } = useSignIn();
  const { signUp, isLoaded: isSignUpLoaded } = useSignUp();
  const { setActive } = useClerk();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [cin, setCin] = useState("");
  const [rib, setRib] = useState("");
  // const [role, setRole] = useState(""); // <-- Supprimé
  const [activeTab, setActiveTab] = useState("login");
  const [pendingVerification, setPendingVerification] = useState(false);
  const [code, setCode] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [showPassword, setShowPassword] = useState(false);
  const [showForgotPassword, setShowForgotPassword] = useState(false);
<<<<<<< HEAD

  const [cin, setCin] = useState("");
  const [phone, setPhone] = useState("");
  const [rib, setRib] = useState("");
  const [role, setRole] = useState("Beneficiaire");
=======
>>>>>>> feature/auth

  if (!isSignInLoaded || !isSignUpLoaded) return null;

  const handleEmailSignIn = async () => {
    try {
      const result = await signIn.create({
        identifier: email,
        password,
      });

      if (result.status === "complete") {
        await setActive({ session: result.createdSessionId });
        window.location.href = "/auth-callback";
      }
    } catch (err: any) {
      console.error("Erreur de connexion:", err);
      setError(err.errors?.[0]?.longMessage || "Erreur de connexion.");
    }
  };

  const handleSignUp = async () => {
    // Validation des champs supplémentaires
    if (!cin.trim()) {
      setError("Le CIN est obligatoire");
      return;
    }
    if (!rib.trim()) {
      setError("Le RIB est obligatoire");
      return;
    }
    // La validation du rôle a été supprimée

    try {
<<<<<<< HEAD
      const newUser = await signUp.create({
=======
      // Sauvegarder les données supplémentaires dans le localStorage
      const userData = { cin, rib }; // 'role' a été supprimé de cet objet
      localStorage.setItem('userRegistrationData', JSON.stringify(userData));

      await signUp.create({
>>>>>>> feature/auth
        emailAddress: email,
        password,
        firstName,
        lastName,
        unsafeMetadata: {
          cin,
          phone,
          rib,
          role,
        },
      });

      await signUp.prepareEmailAddressVerification({ strategy: "email_code" });
      setPendingVerification(true);

      await saveUserExtra(
        newUser.id!,
        firstName,
        lastName,
        email,
        cin,
        phone,
        rib,
        role
      );
    } catch (err: any) {
      console.error("Erreur d'inscription:", err);
<<<<<<< HEAD
      setError(err.errors?.[0]?.longMessage || "Erreur lors de l'inscription.");
=======
      setError(err.errors?.[0]?.longMessage || "Une erreur s'est produite lors de l'inscription.");
      // Nettoyer en cas d'erreur
      localStorage.removeItem('userRegistrationData');
>>>>>>> feature/auth
    }
  };

  const handleVerification = async () => {
    try {
      const completeSignUp = await signUp.attemptEmailAddressVerification({ code });

      if (completeSignUp.status === "complete") {
        await setActive({ session: completeSignUp.createdSessionId });
        window.location.href = "/auth-callback";
      }
    } catch (err: any) {
      console.error("Erreur de vérification:", err);
      setError(err.errors?.[0]?.longMessage || "Code invalide.");
    }
  };

  if (showForgotPassword) {
    return <ForgotPassword onBack={() => setShowForgotPassword(false)} />;
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-white p-6">
      <div className="w-full max-w-md mx-auto flex flex-col gap-4">
        <div className="bg-gradient-to-br from-purple-700 to-purple-800 text-white rounded-2xl shadow-2xl overflow-hidden">
          <div className="p-6 lg:p-8">
          

            <h1 className="text-2xl font-bold text-white mb-2 text-center anago-font">BIENVENUE</h1>

            <p className="text-purple-200 text-center mb-6 italic-text">Connectez-vous ou créez un compte pour accéder au tableau de bord.</p>

            {pendingVerification ? (
              <>
                <p className="text-purple-200 mb-4 text-center">Un code a été envoyé à {email}.</p>

                <Input
                  type="text"
                  placeholder="Code de vérification"
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  className="mb-4 bg-white text-black border-gray-200"
                />

<<<<<<< HEAD
                {error && <p className="text-red-300 text-sm mb-4">{error}</p>}

                <Button onClick={handleVerification} className="w-full bg-white text-purple-800 font-semibold mb-3">Vérifier</Button>
                <Button onClick={() => setPendingVerification(false)} variant="outline" className="w-full border-white text-white">Retour</Button>
              </>
            ) : (
              <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
                <div className="flex justify-between">
    <TabsList className="grid w-full grid-cols-2 bg-white p-1 rounded-full overflow-hidden">
      <TabsTrigger value="login" className="text-black font-semibold data-[state=active]:bg-purple-100 data-[state=active]:text-purple-800">
        Connexion
      </TabsTrigger>
      <TabsTrigger value="signup" className="text-black font-semibold data-[state=active]:bg-purple-100 data-[state=active]:text-purple-800">
        Inscription
      </TabsTrigger>
    </TabsList>
  </div>

                <TabsContent value="login">
                  <div className="space-y-4 mt-4">
                    <Input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} className="bg-white text-black border-gray-200" />

                    <div className="relative">
                      <Input type={showPassword ? "text" : "password"} placeholder="Mot de passe" value={password} onChange={(e) => setPassword(e.target.value)} className="bg-white text-black pr-12 border-gray-200" />
                        <button
                          type="button"
                          aria-label={showPassword ? "Masquer le mot de passe" : "Afficher le mot de passe"}
                          onClick={() => setShowPassword(!showPassword)}
                          className="absolute inset-y-0 right-2 flex items-center justify-center px-2 rounded-md bg-white/90 text-purple-800 hover:bg-white focus:outline-none focus-visible:ring-2 focus-visible:ring-white/60"
                        >
                          {showPassword ? <FaEyeSlash /> : <FaEye />}
                        </button>
                    </div>

                    {error && <p className="text-red-300 text-sm">{error}</p>}

                    <Button onClick={handleEmailSignIn} className="w-full bg-white text-purple-800 font-semibold">Se connecter</Button>

                    <div className="text-center">
                      <Button variant="link" onClick={() => setShowForgotPassword(true)} className="text-purple-800 hover:text-dark-200">Mot de passe oublié ?</Button>
                    </div>
                  </div>
                </TabsContent>

                <TabsContent value="signup">
                  <div className="space-y-4 mt-4">
                    <div className="flex gap-4">
                      <Input type="text" placeholder="Prénom" value={firstName} onChange={(e) => setFirstName(e.target.value)} className="bg-white text-black border-gray-200 flex-1" />
                      <Input type="text" placeholder="Nom" value={lastName} onChange={(e) => setLastName(e.target.value)} className="bg-white text-black border-gray-200 flex-1" />
                    </div>

                    <Input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} className="bg-white text-black border-gray-200" />

                    <div className="relative">
                      <Input type={showPassword ? "text" : "password"} placeholder="Mot de passe" value={password} onChange={(e) => setPassword(e.target.value)} className="bg-white text-black pr-12 border-gray-200" />
                        <button
                          type="button"
                          aria-label={showPassword ? "Masquer le mot de passe" : "Afficher le mot de passe"}
                          onClick={() => setShowPassword(!showPassword)}
                          className="absolute inset-y-0 right-2 flex items-center justify-center px-2 rounded-md bg-white/90 text-purple-800 hover:bg-white focus:outline-none focus-visible:ring-2 focus-visible:ring-white/60"
                        >
                          {showPassword ? <FaEyeSlash /> : <FaEye />}
                        </button>
                    </div>

                    <Input type="text" placeholder="CIN" value={cin} onChange={(e) => setCin(e.target.value)} className="bg-white text-black border-gray-200" />
                    <Input type="text" placeholder="Numéro de téléphone" value={phone} onChange={(e) => setPhone(e.target.value)} className="bg-white text-black border-gray-200" />
                    <Input type="text" placeholder="RIB" value={rib} onChange={(e) => setRib(e.target.value)} className="bg-white text-black border-gray-200" />
                    <Input type="text" placeholder="Role" value={role} onChange={(e) => setRole(e.target.value)} disabled className="bg-white text-black border-gray-200" />

                    {error && <p className="text-red-300 text-sm">{error}</p>}
                    <PasswordStrengthMeter password={password} />

                    <Button onClick={handleSignUp} className="w-full bg-white text-purple-800 font-semibold">S'inscrire</Button>
                  </div>
                </TabsContent>
              </Tabs>
            )}

            {!pendingVerification && <div className="relative my-6"><div className="absolute inset-0 flex items-center"><span className="w-full border-t border-white/30" /></div></div>}
          </div>
        </div>
=======
            <TabsContent value="signup">
              <div className="space-y-4 mt-4">
                <div className="flex gap-4">
                  <Input
                    type="text"
                    placeholder="Prénom"
                    value={firstName}
                    onChange={(e) => setFirstName(e.target.value)}
                    className="bg-zinc-800 border-zinc-700 text-white flex-1"
                  />
                  <Input
                    type="text"
                    placeholder="Nom"
                    value={lastName}
                    onChange={(e) => setLastName(e.target.value)}
                    className="bg-zinc-800 border-zinc-700 text-white flex-1"
                  />
                </div>
                <Input
                  type="email"
                  placeholder="Email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="bg-zinc-800 border-zinc-700 text-white"
                />
                <div className="relative">
                  <Input
                    type={showPassword ? "text" : "password"}
                    placeholder="Mot de passe"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="bg-zinc-800 border-zinc-700 text-white pr-10"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute inset-y-0 right-0 pr-3 flex items-center text-zinc-400 hover:text-white"
                  >
                    {showPassword ? <FaEyeSlash /> : <FaEye />}
                  </button>
                </div>
                
                {/* CHAMPS CIN ET RIB */}
                <div className="grid grid-cols-2 gap-4">
                  <Input
                    type="text"
                    placeholder="CIN"
                    value={cin}
                    onChange={(e) => setCin(e.target.value)}
                    className="bg-zinc-800 border-zinc-700 text-white"
                  />
                  <Input
                    type="text"
                    placeholder="RIB"
                    value={rib}
                    onChange={(e) => setRib(e.target.value)}
                    className="bg-zinc-800 border-zinc-700 text-white"
                  />
                </div>
                
                {/* Le bloc <Select> pour le rôle a été supprimé d'ici */}

                {error && <p className="text-red-500 text-sm text-center">{error}</p>}
                <PasswordStrengthMeter password={password} />
                <Button
                  onClick={handleSignUp}
                  className="w-full bg-emerald-500 hover:bg-emerald-600 text-black"
                >
                  S'inscrire
                </Button>
              </div>
            </TabsContent>
          </Tabs>
        )}
      </div>
      <div className="flex-1 hidden lg:block">
        <AuthImagePattern
          title="FraudDetect"
          subtitle="Bienvenue sur la plateforme de détection de fraude"
        />
>>>>>>> feature/auth
      </div>
    </div>
  );
};

export default AuthPage;
