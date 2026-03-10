document.addEventListener("DOMContentLoaded", function() {

    /* ========== Helper de validación para cualquier form ========== */
    function setupValidation(formId) {
        const form = document.getElementById(formId);
        if (!form) return;

        // evitar validación nativa del navegador
        form.setAttribute('novalidate', 'novalidate');
        form._attempted = false;

        const fields = Array.from(form.querySelectorAll('[required]'));

        fields.forEach(f => {
            const v = (f.value === null) ? "" : String(f.value).trim();
            if (v !== "") {
                f.classList.add('is-valid');
            } else {
                f.classList.remove('is-valid','is-invalid');
            }

            const handler = function() {
                const val = (f.value === null) ? "" : String(f.value).trim();
                if (val !== "") {
                    f.classList.remove('is-invalid');
                    f.classList.add('is-valid');
                } else {
                    if (form._attempted) {
                        f.classList.remove('is-valid');
                        f.classList.add('is-invalid');
                    } else {
                        f.classList.remove('is-valid','is-invalid');
                    }
                }
            };
            f.addEventListener('input', handler);
            f.addEventListener('change', handler);
        });

        form.addEventListener('submit', function(e) {
            e.preventDefault();
            form._attempted = true;
            let allValid = true;

            // REFRESCAMOS LOS FIELDS POR SI CAMBIARON LOS 'REQUIRED' DINÁMICAMENTE
            const currentFields = Array.from(form.querySelectorAll('[required]'));

            for (const f of currentFields) {
                const val = (f.value === null) ? "" : String(f.value).trim();
                if (!val) {
                    f.classList.remove('is-valid');
                    f.classList.add('is-invalid');
                    if (allValid) f.focus(); // focus primer inválido
                    allValid = false;
                } else {
                    f.classList.remove('is-invalid');
                    f.classList.add('is-valid');
                }
            }
            if (allValid) {
                form.submit();
            } else {
                window.scrollTo({ top: (form.getBoundingClientRect().top + window.scrollY - 20), behavior: 'smooth' });
            }
        });
    }

    // activar validación en ambos formularios (página buscar)
    setupValidation('form-buscar');
    setupValidation('participante-form');

    /* ========== CASCADA: pais -> departamento -> provincia -> distrito ========== */
    const paisSelect = document.getElementById("pais");
    const depSelect  = document.getElementById("departamento");
    const provSelect = document.getElementById("provincia");
    const distSelect = document.getElementById("distrito");

    function limpiarSelect(select, placeholder) {
        if (!select) return;
        select.innerHTML = `<option value="">${placeholder}</option>`;
    }

    function fetchDepartamentos(paisId) {
        return fetch(`/participante/api/departamentos/?pais_id=${encodeURIComponent(paisId)}`)
            .then(r => r.ok ? r.json() : { departamentos: [] })
            .then(j => j.departamentos || [])
            .catch(()=>[]);
    }
    function fetchProvincias(depId) {
        return fetch(`/participante/api/provincias/?departamento_id=${encodeURIComponent(depId)}`)
            .then(r => r.ok ? r.json() : { provincias: [] })
            .then(j => j.provincias || [])
            .catch(()=>[]);
    }
    function fetchDistritos(provId) {
        return fetch(`/participante/api/distritos/?provincia_id=${encodeURIComponent(provId)}`)
            .then(r => r.ok ? r.json() : { distritos: [] })
            .then(j => j.distritos || [])
            .catch(()=>[]);
    }

    if (paisSelect) {
        paisSelect.addEventListener("change", function() {
            limpiarSelect(depSelect, "--Seleccione Departamento--");
            limpiarSelect(provSelect, "--Seleccione Provincia--");
            limpiarSelect(distSelect, "--Seleccione Distrito--");
            
            // LÓGICA PERÚ (ID = 1, asumiendo que 1 es Perú u obtener por texto)
            // Si el texto seleccionado es "Perú" o "Peru" hacemos obligatorios los combos
            const selectedText = this.options[this.selectedIndex]?.text.toLowerCase() || "";
            const esPeru = selectedText.includes("perú") || selectedText.includes("peru");

            if (esPeru) {
                depSelect.setAttribute("required", "required");
                provSelect.setAttribute("required", "required");
                distSelect.setAttribute("required", "required");
            } else {
                depSelect.removeAttribute("required");
                provSelect.removeAttribute("required");
                distSelect.removeAttribute("required");
                
                // Limpiamos estilos de validación si ya no son requeridos
                [depSelect, provSelect, distSelect].forEach(sel => {
                    sel.classList.remove("is-invalid", "is-valid");
                });
            }

            if (this.value) {
                fetchDepartamentos(this.value).then(data => {
                    data.forEach(d => {
                        depSelect.innerHTML += `<option value="${d.id}">${d.nombre}</option>`;
                    });
                    depSelect.dispatchEvent(new Event('change'));
                });
            }
        });

        // Disparar validación on load por si ya hay un país preseleccionado al editar
        setTimeout(() => paisSelect.dispatchEvent(new Event('change')), 100);
    }

    if (depSelect) {
        depSelect.addEventListener("change", function() {
            limpiarSelect(provSelect, "--Seleccione Provincia--");
            limpiarSelect(distSelect, "--Seleccione Distrito--");
            if (this.value) {
                fetchProvincias(this.value).then(data => {
                    data.forEach(p => {
                        provSelect.innerHTML += `<option value="${p.id}">${p.nombre}</option>`;
                    });
                    provSelect.dispatchEvent(new Event('change'));
                });
            }
        });
    }

    if (provSelect) {
        provSelect.addEventListener("change", function() {
            limpiarSelect(distSelect, "--Seleccione Distrito--");
            if (this.value) {
                fetchDistritos(this.value).then(data => {
                    data.forEach(d => {
                        distSelect.innerHTML += `<option value="${d.id}">${d.nombre}</option>`;
                    });
                    distSelect.dispatchEvent(new Event('change'));
                });
            }
        });
    }

});
