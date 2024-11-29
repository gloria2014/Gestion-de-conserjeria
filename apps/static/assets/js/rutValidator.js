// Función genérica para validar y formatear RUT en tiempo real
function configurarValidacionRut(selector) {
    document.querySelectorAll(selector).forEach((campo) => {
        campo.addEventListener('input', function () {
            let rut = this.value;

            // Eliminar caracteres no válidos
            rut = rut.replace(/[^0-9kK\-\.]/g, '');

            // Formatear el RUT
            rut = formatearRut(rut);

            // Actualizar el valor del campo
            this.value = rut;

            // Validar el RUT si tiene al menos 9 caracteres
            if (rut.length >= 9) {
                if (validarRut(rut)) {
                    this.style.borderColor = 'green'; // Válido
                    document.getElementById('rut_visita_error2').innerHTML = '';
                } else {
                    this.style.borderColor = 'red'; // Inválido
                }
            } else {
                this.style.borderColor = ''; // Restablecer estilo
            }
        });
    });
}

// Función para formatear el RUT con puntos y guion
function formatearRut(rut) {
    // Eliminar puntos y guion anteriores
    rut = rut.replace(/\./g, '').replace(/-/g, '');

    // Agregar puntos y guion
    if (rut.length > 1) {
        const cuerpo = rut.slice(0, -1);
        const dv = rut.slice(-1);
        return cuerpo.replace(/\B(?=(\d{3})+(?!\d))/g, '.') + '-' + dv;
    }
    return rut;
}

// Función para validar el RUT
function validarRut(rut) {
    // Eliminar puntos y guion
    rut = rut.replace(/\./g, '').replace(/-/g, '');

    const cuerpo = rut.slice(0, -1);
    const dv = rut.slice(-1).toUpperCase();

    // Validar que el cuerpo sea numérico
    if (!/^\d+$/.test(cuerpo)) return false;

    // Calcular dígito verificador
    let suma = 0;
    let multiplicador = 2;

    for (let i = cuerpo.length - 1; i >= 0; i--) {
        suma += parseInt(cuerpo[i]) * multiplicador;
        multiplicador = multiplicador === 7 ? 2 : multiplicador + 1;
    }

    const resto = suma % 11;
    const dvCalculado = resto === 0 ? '0' : resto === 1 ? 'K' : (11 - resto).toString();
    return dv === dvCalculado;
}

// Función para validar el RUT en el evento submit del formulario
function validarFormularioRut(event) {
    const rutCampo = document.querySelector('.rut');
    const rut = rutCampo.value;

    if (!validarRut(rut)) {
        event.preventDefault(); // Evitar el envío del formulario
        document.getElementById('rut_visita_error2').innerHTML = 'Formato de Rut incorrecto.';
       
        //rutCampo.style.borderColor = 'red'; // Marcar el campo como inválido 
     }
}

