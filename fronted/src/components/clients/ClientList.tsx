import { Table } from "react-bootstrap"
import { Link, useParams } from "../../Router"
import { Template } from "../Common"
import { useEffect, useState } from "react"

export default () => {
    const params = useParams()

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

    return (
        <Template>

            <div className="mt-2">
                <div className="row">
                    <div className="col d-flex">
                        <h3>Lista de clientes</h3>
                        &nbsp;&nbsp;&nbsp;&nbsp;
                        <Link href={params.makeUrl('/client/form?mode=new')} as="button">
                            NUEVO
                        </Link>
                    </div>
                </div>
            </div>

            <div className="sheet mt-4">
                <Table>
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
                                    <tr key={"row-client-" + i}>
                                        <td>{client.id}</td>
                                        <td>{client.name}</td>
                                        <td>{client.email}</td>
                                        <td>{client.rfc}</td>
                                        <td>{client.regimen_fiscal}</td>
                                        <td>{client.zip_code}</td>
                                    </tr>
                                )
                            })
                        }
                    </tbody>
                </Table>
            </div>

        </Template>
    )
}