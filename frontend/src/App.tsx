import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import BeneficiarySpace from './pages/beneficiary/BeneficiarySpace';
import { Button } from './components/ui/button';

function Home() {
  return (
    <>
      <h1 className='text-red-500'>Vite + React</h1>
      <h2 className="text-blue-600 font-bold text-2xl mt-4">
        Tailwind fonctionne !
        <Button className="ml-4">Cliquez-moi</Button>
      </h2>
    </>
  )
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/beneficiary" element={<BeneficiarySpace />} />
      </Routes>
    </Router>
  )
}

export default App;
