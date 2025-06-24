import { Form } from "react-bootstrap"
import { Template } from "./Common"

export default () => {

    const uploadFile = (ev: React.ChangeEvent<HTMLInputElement>) => {
        const allowedTypes = ['application/x-zip-compressed','text/xml']
        
        const files = ev.target.files;
        if (files) {
            for (let i = 0; i < files.length; i++) {
                const file: File = files[i];
                if(allowedTypes.some(type => type === file.type)) {
                    console.log(file)
                }
            }
        }

    }

    return (
        <Template>
            <div className="row mt-4">
                <div className="col">
                    <Form.FloatingLabel label="ZIP">
                        <Form.Control type="file" placeholder="ZIP" onChange={uploadFile}/>
                    </Form.FloatingLabel>
                </div>
            </div>
        </Template>
    )
}