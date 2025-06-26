import { Button, Form, Tab, Tabs } from "react-bootstrap";
import { MetodoPagoList, RegimenFiscalList, Template } from "../Common"
import { useState } from "react";
import { useNavigate } from "react-router";

export default () => {

    const [tipoContribuyente, setTipoContribuyente] = useState(0)
    
    const navigate = useNavigate()


    const onSubmit = (ev: React.FormEvent<HTMLFormElement>) => {
        ev.preventDefault();
        const formData = new FormData(ev.currentTarget);
        fetch('/api/clients/save', {
            body: formData,
            method: 'POST'
        })
        .then(response => response.json())
        .then(response => {
            if (response.error) return alert(response.message);
            navigate('/clients')
        })
        
        // const data = Object.fromEntries(formData.entries());
        // console.log(data)
        return
    }

    const revisarTipoContribuyente = (ev: React.FocusEvent<HTMLInputElement>) => {
        const totalCaracteres = ev.target.value.length;

        switch (totalCaracteres) {
            case 13:
                setTipoContribuyente(1);
                break;
            case 12:
                setTipoContribuyente(2);
                break;
            default:
                console.log('No cumple con la longitud de un RFC');
                ev.target.focus()
        }
    }

    return (
        <Template>

            <div className="mt-2">
                <div className="row">
                    <div className="col d-flex">
                        <h3>Lista de clientes</h3>
                    </div>
                </div>
            </div>

            <Form action="#" onSubmit={onSubmit}>
                <div className="sheet">
                    <div className="row">
                        <div className="col">
                            <Button type="submit">ENVIAR</Button>
                        </div>
                    </div>
                </div>
                <div className="sheet mt-4">
                    <div className="row row-cols-1 row-cols-lg-2 g-2">
                        <div className="col">
                            <Form.Group controlId="name-id">
                                <Form.Label>Nombre del Cliente</Form.Label>
                                <Form.Control name="name" placeholder="Nombre del cliente" />
                            </Form.Group>
                        </div>
                        <div className="col">
                            <Form.Group controlId="email-id">
                                <Form.Label>Correo</Form.Label>
                                <Form.Control name="email" required placeholder="username@dominio.com" />
                            </Form.Group>
                        </div>
                    </div>
                    <Tabs className="mt-4">
                        <Tab eventKey="DF" title="Datos Fiscales">
                            <div className="row row-cols-1 row-cols-lg-2 g-2 mt-2">
                                <div className="col mb-3">
                                    <Form.Group controlId="fiscal-razon-social-id">
                                        <Form.Label>Razon Social</Form.Label>
                                        <Form.Control className="uppercase" name="razon_social" placeholder="Razon Social" required />
                                    </Form.Group>
                                </div>

                                <div className="col mb-3">
                                    <Form.Group controlId="fiscal-rfc-id">
                                        <Form.Label>RFC</Form.Label>
                                        <Form.Control
                                            className="uppercase"
                                            name="rfc"
                                            placeholder="XAXX010101000"
                                            maxLength={13}
                                            onBlur={revisarTipoContribuyente}
                                            required />
                                    </Form.Group>
                                </div>

                                <div className="col mb-3">
                                    <Form.Group controlId="fiscal-regimen-id">
                                        <Form.Label>Regimen Fiscal</Form.Label>
                                        <RegimenFiscalList name="regimen_fiscal_id" required tipo={tipoContribuyente} />
                                    </Form.Group>
                                </div>
                                <div className="col mb-3">
                                    <Form.Group controlId="fiscal-mtodo-pago-id">
                                        <Form.Label>Metodo de Pago Preferido</Form.Label>
                                        <MetodoPagoList required  name="metodo_pago_id"/>
                                    </Form.Group>
                                </div>

                                <div className="col-12 mb-3">
                                    <Form.Group controlId="fiscal-csf-id">
                                        <Form.Label>Constancia de Situacion Fiscal</Form.Label>
                                        <Form.Control type="file" name="csf" accept=".pdf" />
                                    </Form.Group>
                                </div>
                            </div>
                        </Tab>
                        <Tab eventKey="address" title="Direccion">
                            <div className="row row-cols-1 row-cols-lg-2 g-2 mt-2">
                                <div className="col">
                                    <Form.Group controlId="address-add-id">
                                        <Form.Label>Dirección</Form.Label>
                                        <Form.Control name="a_address" placeholder="Calle #100, Ciudad" />
                                    </Form.Group>
                                </div>
                                <div className="col">
                                    <Form.Group controlId="address-zip-id">
                                        <Form.Label>Codigo Postal</Form.Label>
                                        <Form.Control placeholder="C.P." name="a_zip_code" required />
                                    </Form.Group>
                                </div>
                                <div className="col">
                                    <Form.Group controlId="address-city-id">
                                        <Form.Label>Ciudad</Form.Label>
                                        <Form.Control placeholder="Monterrey" name="a_city" />
                                    </Form.Group>
                                </div>
                                <div className="col">
                                    <Form.Group controlId="address-state-id">
                                        <Form.Label>Estado</Form.Label>
                                        <Form.Control placeholder="Estado" name="a_state" />
                                    </Form.Group>
                                </div>
                                <div className="col">
                                    <Form.Group controlId="address-country-id">
                                        <Form.Label>Pais</Form.Label>
                                        <Form.Control placeholder="México" name="a_country" />
                                    </Form.Group>
                                </div>
                            </div>
                        </Tab>
                    </Tabs>
                </div>
            </Form>
        </Template>
    )
}