import { useParams } from "react-router"
import { Template } from "../Common"
import { useEffect, useState } from "react"
import { Button, Col, Form, Modal, Row, Tab, Tabs, type ModalProps } from "react-bootstrap"
import { TablaComprobantes } from "../Cfdis"
import { MdFilterAlt } from "react-icons/md"

interface FilterDatesModalProps extends ModalProps {
    onFilter: (startdate: string, enddate: string) => void;
}

export const FilterDatesModal = (props: FilterDatesModalProps) => {

    const [startdate, setStartDate] = useState("")
    const [enddate, setEndDate] = useState("")

    return (
        <Modal {...props}>
            <Modal.Header>
                <Modal.Title>Buscar entre fechas</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Row>
                    <Form.Group as={Col} controlId="startdate">
                        <Form.Label>Fecha Inicial:</Form.Label>
                        <Form.Control type="date" value={startdate} onChange={(ev) => setStartDate(ev.target.value)} />
                    </Form.Group>
                    <Form.Group as={Col} controlId="enddate">
                        <Form.Label>Fecha Final:</Form.Label>
                        <Form.Control type="date" value={enddate} onChange={(ev) => setEndDate(ev.target.value)} />
                    </Form.Group>
                </Row>
            </Modal.Body>
            <Modal.Footer>
                <Button onClick={() => {
                    setStartDate('')
                    setEndDate('')
                    props.onFilter(startdate, enddate);
                    props.onHide && props.onHide();
                }}>FILTRAR</Button>
            </Modal.Footer>
        </Modal>
    )
}

export default () => {

    const [documents, setDocument] = useState<Record<string, any>>({});
    const [showFilter, setShowFilter] = useState(false);

    const params: Record<string, any> = useParams()

    const searchDocuments = async (startdate: string, enddate: string) => {

        const handleError = (message: string) => {
            alert(message);
        }

        let url = '/api/documentos_fiscales/' + params.rfc;

        if (startdate !== "" && enddate !== "") {
            url += `?startdate=${startdate}&enddate=${enddate}`
        }

        const request = await fetch(url)

        if (!request.ok) {
            handleError(request.status + " - " + request.statusText);
            return;
        }

        const response = await request.json();

        if (response.error) return handleError(response.message);
        if (
            response.data.documentos_emitidos.length === 0 ||
            response.data.documentos_recibidos.length === 0) {
            setDocument([])
        } else {
            setDocument(response.data)
        }

    }

    useEffect(() => {
        searchDocuments("", "")
    }, [])

    return (
        <Template>

            <FilterDatesModal
                show={showFilter}
                onFilter={(start, end) => searchDocuments(start, end)}
                onHide={() => setShowFilter(false)}
            />

            <div className="sheet mt-4">
                <div className="row row-cols-1">
                    <div className="col">
                        <h3>{documents.client && documents.client.razon_social}</h3>
                    </div>
                    <div className="col">
                        <span>
                            <strong>RFC:&nbsp;</strong>
                            {documents.client && documents.client.rfc.toUpperCase()}
                        </span>
                    </div>
                    <div className="col">
                        <span>
                            <strong>Regimen:&nbsp;</strong>
                            {documents.client && documents.client.regimen_fiscal}
                        </span>
                    </div>
                    <div className="col-11"></div>
                    <div className="col-1">
                        <div className="row">
                            <div className="col">
                                <MdFilterAlt
                                    size={20}
                                    className="pointer"
                                    onClick={() => setShowFilter(true)} />
                            </div>
                        </div>
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