import { Container, Nav, Navbar } from "react-bootstrap";
import { useParams, Link } from "../Router";

export const NavbarApp = () => {
    const params = useParams()
    return (
        <Navbar className="bg-body-tertiary">
            <Container>
                <Navbar.Brand>EVAPP</Navbar.Brand>
            </Container>
            <Navbar.Toggle aria-controls="evapp-navbar" />
            <Navbar.Collapse id="evapp-navbar">
                <Nav className="me-auto">
                    <Link href={params.makeUrl('/')} >Dashboard</Link>
                    <Link href={params.makeUrl('/cfdi')} >CFDI</Link>
                </Nav>
            </Navbar.Collapse>
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