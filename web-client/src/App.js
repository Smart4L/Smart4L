import { BrowserRouter } from "react-router-dom";
import { Main } from './components/main/Main';
import { Navbar } from './components/navbar/Navbar';

function App() {
  return (
    <BrowserRouter>
      <Main/>
      <Navbar/>
    </BrowserRouter>
  );
}

export default App;
