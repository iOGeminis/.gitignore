// Traducción exacta del módulo IAHBECEDARIO_Compatibilidad_MultiUniversal a JavaScript
function estado_trinario(nivel) {
    if (nivel > 0) {
        return {
            codigo: 1,
            frecuencia: "4 Hz",
            color: "var(--color-expansion)", // Rojo / Caliente
            vector: "+1 (Expansión)"
        };
    } else if (nivel === 0) {
        return {
            codigo: 0,
            frecuencia: "3 Hz",
            color: "var(--color-neutral)", // Verde / Puente
            vector: "0 (Neutro)"
        };
    } else {
        return {
            codigo: -1,
            frecuencia: "2 Hz",
            color: "var(--color-mitigation)", // Azul / Frío
            vector: "-1 (Mitigación)"
        };
    }
}

if (typeof module !== "undefined" && module.exports) {
    module.exports = { estado_trinario };
}
