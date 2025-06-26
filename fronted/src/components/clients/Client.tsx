import { useParams } from "react-router"
import { Template } from "../Common"
import { useEffect, useState } from "react"
import { Tab, Tabs } from "react-bootstrap"
import { TablaComprobantes } from "../Cfdis"

export default () => {

    const [documents, setDocument] = useState<Record<string, any>>({})

    const params: Record<string, any> = useParams()

    const searchDocuments = async () => {

        const handleError = (message: string) => {
            alert(message);
        }
        const request = await fetch('/api/documentos_fiscales/' + params.rfc)

        if (!request.ok) {
            handleError(request.status + " - " + request.statusText);
            return;
        }

        const response = await request.json();

        if (response.error) return handleError(response.message);

        setDocument(response.data)

    }

    useEffect(() => {
        searchDocuments()
    }, [])

    return (
        <Template>
            <div className="sheet mt-4">
                <div className="row row-cols-1">
                    <div className="col">
                        <h3>{documents.client && documents.client.razon_social}</h3>
                    </div>
                    <div className="col">
                        <h4>RFC: {documents.client && documents.client.rfc.toUpperCase()}</h4>
                    </div>
                </div>
            </div>
            <div className="sheet mt-4 mb-4">
                <div className="row mt-4">
                    <div className="col">
                        <h4>Comprobantes Fiscales</h4>
                    </div>
                </div>

                <div className="row p-3">
                    <Tabs>
                        <Tab title="Emitidas" eventKey="emitidas">
                            <TablaComprobantes comprobantes={documents.documentos_emitidos || []} />
                        </Tab>
                        <Tab title="Recibidas" eventKey="recibidas">
                            <TablaComprobantes comprobantes={documents.documentos_recibidos || []} />
                        </Tab>
                    </Tabs>
                </div>
            </div>
        </Template>
    )
}