import xml.etree.ElementTree as ET
from .models import (
    Comprobante,
    List,
    Concepto,
    TimbreFiscal,
    Emisor,
    Receptor,
    Pagos,
    Pago,
    DocumentoRelacionado,
    RetencionDR,
    TrasladoDR,
    Complementos
)

namespaces = {
    "cfdi": "http://www.sat.gob.mx/cfd/4",
    "pago20": "http://www.sat.gob.mx/Pagos20",
    "tfd": "http://www.sat.gob.mx/TimbreFiscalDigital",
}


class ComprobantePago:
    comprobante: Comprobante
    emisor: Emisor
    receptor: Receptor
    conceptos: List[Concepto]
    timbrefiscal: TimbreFiscal
    complementos: List

    @staticmethod
    def obtener_retenciones(tag: ET.Element) -> List[RetencionDR]:

        retenciones = []
        retenciones_tag = tag.findall(".//pago20:RetencionesDR", namespaces)

        if retenciones_tag is None:
            return retenciones

        for _retencion in retenciones_tag:
            _r = RetencionDR()
            _r.set_from_dict(_retencion.attrib)
            retenciones.append(_r)

        return retenciones

    @staticmethod
    def obtener_traslados(tag: ET.Element) -> List[TrasladoDR]:

        traslados = []
        traslados_tag = tag.findall(".//pago20:TrasladosDR", namespaces)

        if traslados_tag is None:
            return traslados

        for _traslado in traslados_tag:
            _r = TrasladoDR()
            _r.set_from_dict(_traslado.attrib)
            traslados.append(_r)

        return traslados

    @staticmethod
    def obtener_documentos_relacionados(tag: ET.Element) -> List[DocumentoRelacionado]:
        relacionados = []
        if tag is None:
            return relacionados

        doc_rel_tag = tag.findall(".//pago20:DoctoRelacionado", namespaces)

        if doc_rel_tag is None:
            return relacionados

        for dr_tag in doc_rel_tag:

            dr = DocumentoRelacionado()
            dr.set_from_dict(dr_tag.attrib)
            dr.impuestos_retencion = ComprobantePago.obtener_retenciones(dr_tag)
            dr.impuestos_traslado = ComprobantePago.obtener_traslados(dr_tag)
            relacionados.append(dr)

        return relacionados

    @staticmethod
    def obtener_pagos(tag: ET.Element) -> List[Pago]:
        pagos = []

        pagos_tag = tag.findall(".//pago20:Pago", namespaces)

        if pagos_tag is None:
            return []

        for _pago in pagos_tag:
            p = Pago()
            p.set_from_dict(_pago.attrib)
            p.documentos_relacionados = ComprobantePago.obtener_documentos_relacionados(
                _pago
            )

            pagos.append(p)

        return pagos

    @staticmethod
    def convertir_xml(xml: str) -> "ComprobantePago":

        if not isinstance(xml, str):
            return None

        if xml.endswith(".xml"):
            root = ET.parse(xml)
            root = root.getroot()
        else:
            root = ET.fromstring(text=xml)

        if root is None:
            return None

        comprobante = Comprobante()
        comprobante.set_from_dict(root.attrib)

        emisor_tag = root.find(".//cfdi:Emisor", namespaces)

        if emisor_tag is not None:
            emisor = Emisor()
            emisor.set_from_dict(emisor_tag.attrib)

        receptor_tag = root.find(".//cfdi:Receptor", namespaces)

        if receptor_tag is not None:
            receptor = Receptor()
            receptor.set_from_dict(receptor_tag.attrib)

        timbrefiscal_tag = root.find(".//tfd:TimbreFiscalDigital", namespaces)

        if timbrefiscal_tag is not None:
            timbrefiscal = TimbreFiscal()
            timbrefiscal.set_from_dict(timbrefiscal_tag.attrib)

        conceptos = []
        for _concepto_tag in root.findall(".//cfdi:Concepto", namespaces):
            if _concepto_tag is not None:
                _concepto = Concepto()
                _concepto.set_from_dict(_concepto_tag.attrib)
                conceptos.append(_concepto)

        pagos = Pagos()
        pagos_tag = root.find(".//pago20:Pagos", namespaces)

        pagos.Version = "2.0"

        if pagos_tag is not None:
            pagos_totales_tag = pagos_tag.find(".//pago20:Totales", namespaces)
            if pagos_totales_tag is not None:
                pagos.set_from_dict(pagos_totales_tag.attrib)

            pagos.pagos = ComprobantePago.obtener_pagos(pagos_tag)
        
        complementos = Complementos()
        complementos.pagos = Pagos
        # Declarar comprobante

        comprobante_pago = ComprobantePago()
        comprobante_pago.comprobante = comprobante
        comprobante_pago.emisor = emisor
        comprobante_pago.receptor = receptor
        comprobante_pago.timbrefiscal = timbrefiscal
        comprobante_pago.conceptos = conceptos
        comprobante_pago.complementos = complementos

        return comprobante_pago
