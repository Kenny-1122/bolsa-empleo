// //1. Definir el API
// const API_BASE2 = "http://127.0.0.1:8000"

// let empresaUpdate=null;

// $(document).ready(function() {
//     $('#empresaTable').DataTable({
//       ajax: {
//         url: 'http://127.0.0.1:8000/empresa/get-empresa',
//         dataSrc: 'data'
//       },
//       columns: [
//         { data: 'nit' },
//         { data: 'nombre' },
//         { data: 'ciudad' },
//         { data: 'direccion' },
//         { data: 'correo' },
//         { data: 'telefono' },
//         {
//           data: null,
//           render: function(data, type, row) {
//             return `
//               <button onclick="openEditModal(${data.nit})">Editar</button>
//               <button onclick="deleteEmpresa(${data.nit})">Borrar</button>
//             `;
//           }
//         }
//       ],
//       paging: true,
//       searching: true,
//       ordering: true
//     });
//   });
  
//   function deleteEmpresa(nit){
//     Swal.fire({
//       title: '¿Eliminar empresa?',
//       text: `¿Está seguro de eliminar la empresa NIT ${nit}?`,
//       icon: 'warning',
//       showCancelButton: true,
//       confirmButtonText: 'Sí, eliminar'
//     }).then((result) => {
//       if(result.isConfirmed){
//         fetch(`${API_BASE2}/empresa/delete-empresa/${nit}`, { method: 'DELETE' })
//         .then(res => res.json())
//         .then(data => {
//           if(data.success){
//             Swal.fire('Eliminado', data.message, 'success');
//             $('#empresaTable').DataTable().ajax.reload();
//           } else {
//             Swal.fire('Error', data.detail, 'error');
//           }
//         });
//       }
//     });
//   }
  


//1. Definir el API
const API_BASE2 = "http://127.0.0.1:8000"

let empresaUpdate=null;

//2. Listar datos desde el API
async function fetchEmpresa(){

  const res= await fetch(`${API_BASE2}/empresa/get-empresa`);
  const data =await res.json();

  const tbody= document.querySelector("#empresaTable tbody");
  tbody.innerHTML = "";

  data.data.forEach((e)=>{

    const row = `<tr>
    <td>${e.nit}</td>
    <td>${e.nombre}</td>
    <td>${e.ciudad}</td>
    <td>${e.correo}</td>
    <td>${e.direccion}</td>
    <td>${e.telefono}</td>
    <td>
<i class="fa-solid fa-pencil" title="Editar" onclick="openEditModal('${e.nit}')"></i></td>
    </tr>`;

    tbody.innerHTML += row;
  });
}

//Gestión del modal
function openEmpresaModal(){
  document.getElementById("empresaModal").style.display= "flex";
  if(empresaUpdate){
    document.getElementById("formTitle").textContent="Actualizar Empresa";
    document.getElementById("submitButton").textContent="Actualizar";
  }
  else{
    document.getElementById("formTitle").textContent="Crear Empresa";
    document.getElementById("submitButton").textContent="Crear";
    document.getElementById("empresaForm").reset();
  }
  
}

function closeModal(){
  document.getElementById("modal").style.display= "none";
  empresaUpdate= null;
}


async function openEditModal(correo){
  const res= await fetch(`${API_BASE2}/empresa/get-empresa/${nit}`);
  const response= await res.json();

  if(!res.ok || !response.data){
    return Swal.fire(
      "Error",
      "No se pudo cargar el usuario",
      "error"
    )
  }

  const empresa=response.data;

 
  document.getElementById("nit").value = empresa.nit || "";
  document.getElementById("nombre").value = empresa.nombre || "";
  document.getElementById("ciudad").value = empresa.ciudad || "";
  document.getElementById("direccion").value = empresa.direccion || "";
  document.getElementById("correo").value = empresa.correo || "";
  document.getElementById("telefono").value = empresa.telefono || "";

  empresaUpdate= nit;
  openModal();
}

//2. Create / Update
async function createUser() {

  const empresa={
      nit: document.getElementById("nit").value,
      nombre: document.getElementById("nombre").value,
      ciudad: document.getElementById("ciudad").value,
      direccion: document.getElementById("direccion").value,
      correo: document.getElementById("correo").value,
      telefono: document.getElementById("telefono").value,
  }

  const endpoint= empresaUpdate
  ? `${API_BASE2}/empresa/update-empresa/${empresaUpdate}` 
  : `${API_BASE2}/empresa/create-empresa`;
  
  const method = empresaUpdate ? "PUT" : "POST";

  const res= await fetch(endpoint, {
    method,
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(nit)
  });

  console.log(res)

  if(res.ok){
    Swal.fire(
      "Ëxito",
      empresaUpdate ? "Empresa Actualizada" : "Empresa creada",
      "success"
    )
  closeModal();
  fetchEmpresa();

  }else{
    const error= await res.json();
    Swal.fire(
      "Error",
      error.detail || "Ocurrió un problema", "error",
      "error"
    )
  }

  
}


//Cargar data
fetchEmpresa()

document.getElementById("empresaForm").addEventListener("submit", function(e){
  e.preventDefault();
  createUser();
}) 