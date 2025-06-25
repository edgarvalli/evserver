import { Form, Tab, Tabs } from "react-bootstrap";
// import { useParams } from "../../Router"
import { MetodoPagoList, RegimenFiscalList, Template } from "../Common"

export default () => {

    // const params = useParams();

    return (
        <Template>

            <div className="mt-2">
                <div className="row">
                    <div className="col d-flex">
                        <h3>Lista de clientes</h3>
                    </div>
                </div>
            </div>

            <Form action="#" className="sheet mt-4">
                <div className="row row-cols-1 row-cols-lg-2 g-2">
                    <div className="col">
                        <Form.FloatingLabel label="Nombre">
                            <Form.Control name="name" placeholder="Nombre del Cliente" />
                        </Form.FloatingLabel>
                    </div>
                    <div className="col">
                        <Form.FloatingLabel label="Correo">
                            <Form.Control name="email" placeholder="Correo" />
                        </Form.FloatingLabel>
                    </div>
                </div>
                <Tabs className="mt-4">
                    <Tab eventKey="DF" title="Datos Fiscales">
                        <div className="row row-cols-1 row-cols-lg-2 g-2 mt-2">
                            <div className="col mb-3">
                                <Form.Group  controlId="fiscal-razon-social-id">
                                    <Form.Label>Razon Social</Form.Label>
                                    <Form.Control name="razon_social" placeholder="Razon Social" required/>
                                </Form.Group>
                            </div>

                            <div className="col mb-3">
                                <Form.Group controlId="fiscal-rfc-id">
                                    <Form.Label>RFC</Form.Label>
                                    <Form.Control  name="rfc" placeholder="XAXX010101000" required/>
                                </Form.Group>
                            </div>

                            <div className="col mb-3">
                                <Form.Group controlId="fiscal-regimen-id">
                                    <Form.Label>Regimen Fiscal</Form.Label>
                                    <RegimenFiscalList required/>
                                </Form.Group>
                            </div>
                            <div className="col mb-3">
                                <Form.Group controlId="fiscal-mtodo-pago-id">
                                    <Form.Label>Metodo de Pago Preferido</Form.Label>
                                    <MetodoPagoList required/>
                                </Form.Group>
                            </div>

                            <div className="col-12 mb-3">
                                <Form.Group controlId="fiscal-csf-id">
                                    <Form.Label>Constancia de Situacion Fiscal</Form.Label>
                                    <Form.Control type="file" name="csf" accept=".pdf"/>
                                </Form.Group>
                            </div>
                        </div>
                    </Tab>
                    <Tab eventKey="address" title="Direccion">
                        <div className="row row-cols-1 row-cols-lg-2 g-2 mt-2">
                            <div className="col">
                                <Form.Group controlId="address-add-id">
                                    <Form.Label>Dirección</Form.Label>
                                    <Form.Control name="address" placeholder="Calle #100, Ciudad" />
                                </Form.Group>
                            </div>
                            <div className="col">
                                <Form.Group controlId="address-zip-id">
                                    <Form.Label>Codigo Postal</Form.Label>
                                    <Form.Control placeholder="C.P." name="zip_code" required/>
                                </Form.Group>
                            </div>
                            <div className="col">
                                <Form.Group controlId="address-city-id">
                                    <Form.Label>Ciudad</Form.Label>
                                    <Form.Control placeholder="Monterrey" name="city" />
                                </Form.Group>
                            </div>
                            <div className="col">
                                <Form.Group controlId="address-state-id">
                                    <Form.Label>Estado</Form.Label>
                                    <Form.Control placeholder="Nuevo León" name="state" />
                                </Form.Group>
                            </div>
                            <div className="col">
                                <Form.Group controlId="address-country-id">
                                    <Form.Label>Pais</Form.Label>
                                    <Form.Control placeholder="México" name="country" />
                                </Form.Group>
                            </div>
                        </div>
                    </Tab>
                </Tabs>
            </Form>
        </Template>
    )
}