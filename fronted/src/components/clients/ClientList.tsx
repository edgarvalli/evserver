import { Link, useParams } from "../../Router"
import { Template } from "../Common"

export default () => {
    const params = useParams()
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
                <div className="row">
                    <div className="col">
                        <button className="ev-button">NUEVO</button>
                    </div>
                </div>
            </div>

        </Template>
    )
}