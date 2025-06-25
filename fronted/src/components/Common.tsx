import { Container, Form, Nav, Navbar } from "react-bootstrap";
import { useParams, Link } from "../Router";
import { MdDarkMode, MdOutlineLightMode } from "react-icons/md";
import { useEffect, useState } from "react";
import { isDarkTheme, setTheme } from "../tools";

export const NavbarApp = () => {
    const params = useParams()
    const [isDark, setDark] = useState(true);


    const switchTheme = (ev: React.MouseEvent<HTMLOrSVGElement>) => {
        if (ev.currentTarget) {
            const theme = (ev.currentTarget as HTMLElement).getAttribute('data-name')
            if (theme === "dark") setDark(true)
            if (theme === "light") setDark(false)
            if (theme) setTheme(theme)
        }

    }

    const iconProps = {
        className: "pointer ml-3",
        size: 18,
        onClick: switchTheme
    }

    useEffect(() => {
        if (!isDarkTheme()) setDark(false)
    }, [])

    return (
        <Navbar className="bg-body-tertiary">
            <Container fluid>
                <Navbar.Brand>EVAPP</Navbar.Brand>
                <Navbar.Toggle aria-controls="evapp-navbar" />
                <Navbar.Collapse id="evapp-navbar">
                    <Nav className="me-auto">
                        <Link href={params.makeUrl('/')} >Dashboard</Link>
                        <Link href={params.makeUrl('/clients')} >Clientes</Link>
                        <Link href={params.makeUrl('/cfdi')} >CFDI</Link>
                    </Nav>
                </Navbar.Collapse>
                <div className="d-flex justify-content-between">
                    <Link href="/app/logout">Cerrar Sesión</Link>
                    {
                        isDark
                            ? <MdOutlineLightMode data-name="light" {...iconProps} />
                            : <MdDarkMode data-name="dark" {...iconProps} />
                    }
                </div>
            </Container>
        </Navbar>
    )
}

export const Template = ({ children }: { children: React.ReactNode }) => {
    return (
        <>
            <NavbarApp />
            <Container>
                {children}
            </Container>
        </>
    )
}

// type SelectProps = React.ComponentProps<typeof Form.Select>;
interface SelectProps extends React.ComponentProps<typeof Form.Select> {
    tipo?: number;
}

type APISelectProps = {
    model: string;
    labelKey: string;
    valueKey: string;
    placeholder?: string;
    onItemSelcted?: (item: React.ChangeEvent<HTMLSelectElement>) => void;
}


export const RegimenFiscalList = (props: SelectProps) => {

    const [regimenes, setRegimens] = useState<Record<string, any>[]>([])
    const getData = async () => {
        const url = '/api/regimenes_fiscales?fields=id,codigo,descripcion&tipo_codigo=' + props.tipo;
        const request = await fetch(url);
        const response = await request.json();
        if (response.error) return alert(response.message);
        setRegimens(response.data);
    }

    useEffect(() => {
        getData()
    }, [props.tipo])

    return (
        <Form.Select defaultValue={""} {...props}>
            <option value="" disabled>Selecciona un regimen fiscal</option>
            {
                regimenes.map(r => (
                    <option value={r.id} key={"option-rf-" + r.id}
                    >{r.codigo + " - " + r.descripcion}</option>
                ))
            }
        </Form.Select>
    )

}

export const MetodoPagoList = (props: SelectProps) => {

    const [metodos, setMetodos] = useState<Record<string, any>[]>([])

    useEffect(() => {
        fetch('/api/metodo_pago?fields=id,codigo,descripcion').then(response => response.json())
            .then(response => {
                if (response.error) return alert(response.message);
                setMetodos(response.data)
            })
    }, [])

    return (
        <Form.Select defaultValue={""} {...props}>
            <option value="" disabled>Selecciona un metodo de pago</option>
            {
                metodos.map(r => (
                    <option value={r.id} key={"option-rf-" + r.id}
                    >{r.codigo + " - " + r.descripcion}</option>
                ))
            }
        </Form.Select>
    )

}

export const APISelect = (props: APISelectProps) => {

    const [items, setItems] = useState<Record<string, any>[]>([])

    useEffect(() => {
        const url = `/api/${props.model}`
        fetch(url).then(response => response.json())
            .then(response => {
                if (response.error) return alert(response.message);
                setItems(response.data)
            })
    }, [])

    return (
        <Form.Select defaultValue={""} onChange={props.onItemSelcted}>
            <option value="" disabled>{props.placeholder}</option>
            {
                items.map(item => (
                    <option value={item[props.valueKey]} key={"option-api-" + item.id}>{item[props.labelKey]}</option>
                ))
            }
        </Form.Select>
    )

}