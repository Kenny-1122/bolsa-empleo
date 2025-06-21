// Definir el API
const API_BASE2 = "http://127.0.0.1:8000"

let empresaUpdate=null;
let tablaEmpresas;



//Listar datos desde el API
async function fetchEmpresa() {
  const res = await fetch(`${API_BASE2}/empresa/get-empresa`);
  const data = await res.json();

  // Limpia todas las filas de la tabla
  tablaEmpresas.clear();

  // Agrega nuevas filas
  data.data.forEach((e) => {
    tablaEmpresas.row.add([
      e.nit,
      e.nombre,
      e.ciudad,
      e.direccion,
      e.correo,
      e.telefono,
      `<i class="fa-solid fa-pencil" title="Editar" onclick="openEditModal('${e.nit}')"></i>
      &nbsp;
      <i class="fa-solid fa-trash" style="color: red; cursor: pointer;" title="Eliminar" onclick="confirmDeleteEmpresa('${e.nit}')"></i>
      `
    ]);
  });

  // Refresca la tabla -> para mostrar datos actualizados
  tablaEmpresas.draw();
}

$(document).ready(function () {
  tablaEmpresas = $("#empresaTable").DataTable();
  fetchEmpresa();  // Carga los datos al cargar la página
});


// modal  crear empresa
function openEmpresaModal() {
  empresaUpdate = null;
  document.getElementById("formTitle").textContent = "Crear Empresa";
  document.getElementById("empresaSubmitButton").textContent = "Crear";
  document.getElementById("empresaForm").reset();
  document.getElementById("empresaModal").style.display = "flex";
}

//  modal editar empresa
async function openEditModal(nit) {
  const res = await fetch(`${API_BASE2}/empresa/get-empresa/${nit}`);
  const data = await res.json();
  const empresa = data.data;

  empresaUpdate = empresa.nit;

  document.getElementById("formTitle").textContent = "Editar Empresa";
  document.getElementById("empresaSubmitButton").textContent = "Actualizar";

  document.getElementById("nit").value = empresa.nit;
  document.getElementById("nombre").value = empresa.nombre;
  document.getElementById("ciudad").value = empresa.ciudad;
  document.getElementById("direccion").value = empresa.direccion;
  document.getElementById("correo").value = empresa.correo;
  document.getElementById("telefono").value = empresa.telefono;

  document.getElementById("empresaModal").style.display = "flex";
  document.getElementById("correo").disabled = true; // Para evitar modificar correo
  document.getElementById("nit").disabled = true; // Para evitar modificar nit
}

// Cerrar modal
function closeEmpresaModal() {
  document.getElementById("empresaModal").style.display = "none";
  document.getElementById("nit").disabled = false;   // para volver a habilitar este campo en creacion de empresa
  document.getElementById("correo").disabled = false;

}

// Enviar formulario
document.getElementById("empresaForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const data = {
    nit: document.getElementById("nit").value,
    nombre: document.getElementById("nombre").value,
    ciudad: document.getElementById("ciudad").value,
    direccion: document.getElementById("direccion").value,
    correo: document.getElementById("correo").value,
    telefono: document.getElementById("telefono").value
  };

  try {
    let res;
    if (empresaUpdate) {
      // Actualizar
      res = await fetch(`${API_BASE2}/empresa/update-empresa/${empresaUpdate}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });
    } else {
      // Crear
      res = await fetch(`${API_BASE2}/empresa/create-empresa`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });
    }

    const result = await res.json();

    if (result.success) {
      Swal.fire("Éxito", result.message, "success");
      fetchEmpresa();
      closeEmpresaModal();
    } else {
      Swal.fire("Error", result.detail, "error");
    }
  } catch (error) {
    console.error(error);
    Swal.fire("Error", "Error de comunicación con el servidor", "error");
  }
});

//1.borrar empresa -> sweetalert
async function confirmDeleteEmpresa(nit) {
  const confirm = await Swal.fire({
    title: '¿Estás seguro?',
    text: "Esta acción no se puede deshacer.",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#d33',
    cancelButtonColor: '#3085d6',
    confirmButtonText: 'Sí, eliminar',
    cancelButtonText: 'Cancelar'
  });

  if (confirm.isConfirmed) {    //aqui llamo a la funcion deletempresa y se elimina
    deleteEmpresa(nit);
  }
}


//2.borrar empresa ->DELETE

async function deleteEmpresa(nit) {
  try {
    const res = await fetch(`${API_BASE2}/empresa/delete-empresa/${nit}`, {
      method: 'DELETE'
    });

    const result = await res.json();

    if (result.success) {
      Swal.fire("Eliminado", result.message, "success");
      fetchEmpresa();  // actualiza la tabla
    } else {
      Swal.fire("Error", result.detail, "error");
    }
  } catch (error) {
    console.error(error);
    Swal.fire("Error", "Error de comunicación con el servidor", "error");
  }
}

// Cerrar modal al hacer click fuera
window.onclick = function (event) {
  const modal = document.getElementById("empresaModal");
  if (event.target === modal) {
    closeEmpresaModal();
  }
};



