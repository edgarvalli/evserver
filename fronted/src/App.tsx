import 'bootstrap/dist/css/bootstrap.min.css';
import './assets/styles.css';
import { Route, Routes, BrowserRouter as Router } from 'react-router';

import Cfdis from './components/Cfdis';
import Dashboard from './components/Dashboard';
import Client from './components/clients/Client';
import ClientList from './components/clients/ClientList';
import ClientForm from './components/clients/ClientForm';
import { isDarkTheme } from './tools';


function App() {

  if (isDarkTheme()) {
    window.document.body.setAttribute('data-bs-theme', 'dark')
  } else {
    window.document.body.setAttribute('data-bs-theme', 'light')
  }

  const routes = [
    { path: '/', element: <Dashboard /> },
    { path: '/cfdi', element: <Cfdis /> },
    { path: '/clients', element: <ClientList /> },
    { path: '/client/form', element: <ClientForm /> },
    {path: '/client/:rfc', element: <Client />}
  ]

  return (
    <Router basename='/app'>
      <Routes>
        {
          routes.map((props, i) => <Route {...props} key={'route-id-' + i} />)
        }
      </Routes>
    </Router>
  )
}

export default App
