const test = require("node:test");
const assert = require("node:assert/strict");
const { estado_trinario } = require("./iahbecedario");

test("estado_trinario returns expansion state when nivel > 0", () => {
    const result = estado_trinario(5);
    assert.deepEqual(result, {
        codigo: 1,
        frecuencia: "4 Hz",
        color: "var(--color-expansion)",
        vector: "+1 (Expansión)"
    });
});

test("estado_trinario returns neutral state when nivel === 0", () => {
    const result = estado_trinario(0);
    assert.deepEqual(result, {
        codigo: 0,
        frecuencia: "3 Hz",
        color: "var(--color-neutral)",
        vector: "0 (Neutro)"
    });
});

test("estado_trinario returns mitigation state when nivel < 0", () => {
    const result = estado_trinario(-3);
    assert.deepEqual(result, {
        codigo: -1,
        frecuencia: "2 Hz",
        color: "var(--color-mitigation)",
        vector: "-1 (Mitigación)"
    });
});
