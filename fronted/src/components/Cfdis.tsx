import { Button, Form, Modal, Placeholder, Spinner, type ModalProps } from "react-bootstrap"
import { TableFixedHeader, Template } from "./Common"
import { useEffect, useState } from "react";


interface CfdiFormModalProps extends ModalProps {
    onLoadFinished?: (item: Record<string, any>) => void;
}

export const CfdiFormModal = (props: CfdiFormModalProps) => {

    const [loading, setLoading] = useState(false)

    const uploadFile = (ev: React.FormEvent<HTMLFormElement>) => {
        ev.preventDefault();
        setLoading(true)
        const body = new FormData(ev.currentTarget)

        fetch('/api/documentos_fiscales/save', { method: 'post', body })
            .then(response => response.json())
            .then(response => {
                if (response.error) return alert(response.message);
                setLoading(false);
                props.onLoadFinished && props.onLoadFinished(response)
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

type TablaComprobantesProps = {
    comprobantes: Record<string, any>[];
    onRowClick?: (item: Record<string, any>) => void;
}

export const TablaComprobantes = (props: TablaComprobantesProps) => {

    const getDate = (datestr: string) => {
        if (!datestr) return ''
        const fecha = new Date(datestr);
        const yyyy = fecha.getFullYear();
        const mm = String(fecha.getMonth() + 1).padStart(2, '0'); // getMonth() devuelve 0-11
        const dd = String(fecha.getDate()).padStart(2, '0');
        return `${dd}/${mm}/${yyyy}`
    }

    const renderRows = () => (
        props.comprobantes.map((doc) => {
            return (
                <tr key={doc.uuid_comprobante} onClick={() => props.onRowClick && props.onRowClick(doc)}>
                    <td>{getDate(doc.fecha) || ''}</td>
                    <td>{doc.emisor}</td>
                    <td>{doc.emisor_rfc || ''}</td>
                    <td>{doc.receptor || ''}</td>
                    <td>{doc.receptor_rfc || ''}</td>
                    <td>{parseFloat(doc.total || 0).toLocaleString('en-US', { maximumFractionDigits: 2 })}</td>
                </tr>
            )
        })
    )

    const renderRowsShadown = () => {
        const rows: any[] = [];
        const cells: any[] = [];

        for (let i = 0; i < 10; i++) rows.push(null);
        for (let i = 0; i < 6; i++) cells.push(null);

        return rows.map((_, i) => (
            <tr key={"row-shadown-id-" + i}>
                {
                    cells.map((_, n) => (
                        <td key={"cell-shadown-id" + n}>
                            <Placeholder animation="glow">
                                {' '}
                                <Placeholder xs={12} size="lg" />
                            </Placeholder>
                        </td>
                    ))
                }
            </tr>
        ))
    }

    return (
        <TableFixedHeader>
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
                    props.comprobantes.length > 0
                        ? renderRows()
                        : renderRowsShadown()
                }
            </tbody>
        </TableFixedHeader>
    )
}

export default () => {

    const [comprobantes, setComprobantes] = useState<Record<string, any>[]>([])
    const [showModal, setShowModal] = useState(false);
    const [pagination, setPagination] = useState<Record<string, any>>({})

    const searchDocuments = async () => {
        const handleError = (response: Record<string, any>) => {
            alert(response.message);
            setComprobantes([{}]);
        }
        const request = await fetch('/api/documentos_fiscales/?orderby=fecha_timbrado desc')
        if (!request.ok) {
            handleError({
                message: "Ocurrio un error " + request.status + " - " + request.statusText
            })
            return;
        }
        const response = await request.json()
        if (response.error) {
            handleError(response)
            return;
        };
        setComprobantes(response.data)
        setPagination(prev => ({ ...prev, total: response.total_rows }))
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
                    <div className="col">
                        <strong>Total de documentos: </strong>
                        {pagination.total || 0}
                    </div>
                </div>
                <TablaComprobantes comprobantes={comprobantes} />
            </div>
            <CfdiFormModal
                show={showModal}
                onLoadFinished={(response) => {
                    setPagination((prev) => ({ ...prev, total: response.total_rows }))
                    searchDocuments();
                }}
                onHide={() => setShowModal(false)} />
        </Template>
    )
}