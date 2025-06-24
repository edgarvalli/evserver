import 'bootstrap/dist/css/bootstrap.min.css';
import Router from './Router';

import Cfdis from './components/Cfdis';
import Dashboard from './components/Dashboard';
import { isDarkTheme } from './tools';
function App() {

  if (isDarkTheme()) {
    window.document.body.setAttribute('data-bs-theme','dark')
  } else {
    window.document.body.setAttribute('data-bs-theme','light')
  }

  const routes = [
    { path: '/', component: <Dashboard /> },
    {path: '/cfdi', component: <Cfdis />}
  ]

  return <Router routes={routes} />
}

export default App
