import { useEffect, useState } from "react";
import { Nav } from "react-bootstrap";

export type RouteProp = {
    path: string;
    component: React.JSX.Element;
}

export type RouterProps = {
    routes: RouteProp[];
    notfound?: React.ReactElement
}

export type LinkProps = {
    children: React.ReactNode;
    href: string;
    title?: string;
    as?: React.ElementType;
}

export const useParams = (): Record<string, any> => {

    const url = new URL(window.location.href)
    const makeUrl = (path: string) => {
        const baseURL = import.meta.env.BASE_URL
        return baseURL + path
    }

    let _params: Record<string, any> = {
        makeUrl: makeUrl
    }
    url.searchParams.forEach((value, key) => {
        _params[key] = value
    })
    return _params
}

export const navigate = (path: string) => {
    window.history.pushState('', '', path)
    window.dispatchEvent(new PopStateEvent("popstate"))
}

export const Link = (props: LinkProps) => {
    const handleHref = (ev: React.MouseEvent<HTMLElement>) => {
        ev.preventDefault();
        window.history.pushState(props.title, '', props.href);
        window.dispatchEvent(new PopStateEvent("popstate")); // <--- clave
    };

    if (props.as) {
        const As = props.as;
        if (props.as === "button") {
            return <a className="rounded-button" href={props.href} title={props.title} onClick={handleHref}>{props.children}</a>
        }
        return <As href={props.href} title={props.title} onClick={handleHref}>{props.children}</As>
    }

    return (
        <Nav.Link href={props.href} onClick={handleHref}>
            {props.children}
        </Nav.Link>
    );
};

export default (props: RouterProps) => {
    const baseUrl = import.meta.env.BASE_URL

    const [currentPath, setCurrentPath] = useState(window.location.pathname);

    useEffect(() => {
        const onPopState = () => setCurrentPath(window.location.pathname);
        window.addEventListener("popstate", onPopState);
        return () => window.removeEventListener("popstate", onPopState);
    }, []);

    let Child = props.notfound || <div>404 Not Found</div>;

    props.routes.forEach(item => {
        let url = baseUrl + item.path;
        if (url.endsWith('/')) url = url.slice(0, -1);

        let path = currentPath;
        if (path.endsWith('/')) path = path.slice(0, -1);

        if (url === path) {
            Child = item.component;
        }
    });


    return Child
}