import { Button, Form, Modal, Spinner, Table, type ModalProps } from "react-bootstrap"
import { Template } from "./Common"
import { useEffect, useState } from "react";


export const CfdiFormModal = (props: ModalProps) => {

    const [loading, setLoading] = useState(false)

    const uploadFile = (ev: React.FormEvent<HTMLFormElement>) => {
        ev.preventDefault();
        setLoading(true)
        const body = new FormData(ev.currentTarget)

        fetch('/api/documentos_fiscales/save', { method: 'post', body })
            .then(response => response.json())
            .then(response => {
                if (response.error) return alert(response.message);
                setLoading(false)
                props.onHide && props.onHide();
            })

    }

    return (
        <Modal {...props}>
            <Form onSubmit={uploadFile}>
                <Modal.Header closeButton>
                    <Modal.Title>Cargar un XML o varios en ZIP</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form.Control disabled={loading} type="file" name="xml_file" placeholder="ZIP" accept=".xml, .zip" />
                </Modal.Body>
                <Modal.Footer>
                    {
                        loading
                            ? (<Button variant="primary" disabled>
                                <Spinner
                                    as="span"
                                    animation="grow"
                                    size="sm"
                                    role="status"
                                    aria-hidden="true"
                                />
                                Cargando...
                            </Button>)
                            : (<Button type="submit">CARGAR</Button>)
                    }

                </Modal.Footer>
            </Form>
        </Modal>
    )
}

export default () => {

    const [comprobantes, setComprobantes] = useState<Record<string, any>[]>([])
    const [showModal, setShowModal] = useState(false)

    const searchDocuments = async () => {
        const request = await fetch('/api/documentos_fiscales/?orderby=fecha_timbrado asc')
        const response = await request.json()
        if (response.error) return alert(response.message);
        setComprobantes(response.data)
    }

    const getDate = (datestr: string) => {
        const fecha = new Date(datestr);
        const yyyy = fecha.getFullYear();
        const mm = String(fecha.getMonth() + 1).padStart(2, '0'); // getMonth() devuelve 0-11
        const dd = String(fecha.getDate()).padStart(2, '0');
        return `${dd}/${mm}/${yyyy}`
    }

    useEffect(() => {
        searchDocuments()
    }, [])

    return (
        <Template>
            <div className="sheet mt-4">
                <div className="row">
                    <div className="col">
                        <Button onClick={() => setShowModal(true)}>CARGAR CFDI</Button>
                    </div>
                </div>
            </div>
            <div className="sheet mt-4">
                <div className="row">
                    <Table striped hover bordered responsive>
                        <thead>
                            <tr>
                                <th>Fecha</th>
                                <th>Emisor</th>
                                <th>RFC Emisor</th>
                                <th>Receptor</th>
                                <th>RFC Receptor</th>
                                <th>Total</th>
                            </tr>
                        </thead>
                        <tbody>
                            {
                                comprobantes.map((doc) => {
                                    return (
                                        <tr key={doc.uuid_comprobante}>
                                            <td>{getDate(doc.fecha)}</td>
                                            <td>{doc.emisor}</td>
                                            <td>{doc.emisor_rfc}</td>
                                            <td>{doc.receptor}</td>
                                            <td>{doc.receptor_rfc}</td>
                                            <td>{parseFloat(doc.total).toLocaleString('en-US', { maximumFractionDigits: 2 })}</td>
                                        </tr>
                                    )
                                })
                            }
                        </tbody>
                    </Table>
                </div>
            </div>
            <CfdiFormModal show={showModal} onHide={() => {
                setShowModal(false);
                searchDocuments()
            }} />
        </Template>
    )
}