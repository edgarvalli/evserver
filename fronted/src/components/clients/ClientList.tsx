import { Link, useNavigate } from "react-router"
import { TableFixedHeader, Template } from "../Common"
import { useEffect, useState } from "react"

export default () => {

    const [clients, setClients] = useState<Record<string, any>[]>([])

    const searchClients = async () => {
        const request = await fetch('/api/clients/')
        const response = await request.json();
        if(response.error) return alert(response.message);
        setClients(response.data)
    }

    useEffect(()=> {
        searchClients()
    },[])

    const navigate = useNavigate()

    return (
        <Template>

            <div className="mt-2">
                <div className="row">
                    <div className="col d-flex">
                        <h3>Lista de clientes</h3>
                        &nbsp;&nbsp;&nbsp;&nbsp;
                        <Link to={'/client/form'} className="rounded-button">
                            NUEVO
                        </Link>
                    </div>
                </div>
            </div>

            <div className="sheet mt-4">
                <TableFixedHeader>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Cliente</th>
                            <th>Correo</th>
                            <th>RFC</th>
                            <th>Regimen Fiscal</th>
                            <th>C.P.</th>
                        </tr>
                    </thead>
                    <tbody>
                        {
                            clients.map((client, i) => {
                                return (
                                    <tr key={"row-client-" + i} onClick={() => navigate(`/client/${client.rfc}`)}>
                                        <td>{client.id}</td>
                                        <td>{client.name}</td>
                                        <td>{client.email}</td>
                                        <td>{client.rfc.toUpperCase() || ''}</td>
                                        <td>{client.regimen_fiscal}</td>
                                        <td>{client.zip_code}</td>
                                    </tr>
                                )
                            })
                        }
                    </tbody>
                </TableFixedHeader>
            </div>

        </Template>
    )
}