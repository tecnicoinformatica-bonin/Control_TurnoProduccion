const inputBusqueda = document.getElementById("busqueda");
const filas = document.querySelectorAll(".record");

const arrows = document.querySelectorAll(".arrow");
const arrowsUp = document.querySelectorAll(".arrow__up");
const arrowsDown = document.querySelectorAll(".arrow__down");

inputBusqueda.addEventListener("keyup", function () {
  const texto = inputBusqueda.value.toLowerCase();

  filas.forEach((fila) => {
    const nombre = fila.querySelector(".record-name").textContent.toLowerCase();

    if (nombre.includes(texto)) {
      fila.style.display = "";
    } else {
      fila.style.display = "none";
    }
  });
});

let isSorted = true;
function ordenarTabla(colIndex, tipo = "texto") {
  const tbody = document.querySelector(".tbody-list");
  const filasArray = Array.from(tbody.querySelectorAll(".tr-list"));

  if (isSorted) {
    filasArray.sort((a, b) => {
      activeArrow(colIndex, "uarr");
      isSorted = false;
      let valA = a.children[colIndex].textContent.trim();
      let valB = b.children[colIndex].textContent.trim();

      if (tipo === "numero") {
        return Number(valA) - Number(valB);
      }

      return valA.localeCompare(valB);
    });
  } else {
    activeArrow(colIndex, "darr");
    isSorted = true;
    filasArray.sort((b, a) => {
      let valA = a.children[colIndex].textContent.trim();
      let valB = b.children[colIndex].textContent.trim();

      if (tipo === "numero") {
        return Number(valA) - Number(valB);
      }

      return valA.localeCompare(valB);
    });
  }

  filasArray.forEach((fila) => tbody.appendChild(fila));
}

const activeArrow = function (colIndex, type) {
  arrows.forEach((arrow) => {
    arrow.classList.remove("arrow-active");
    /* console.log(arrow); */

    if (+arrow.dataset.column === +colIndex && arrow.dataset.type === type) {
      arrow.classList.add("arrow-active");
    }
  });
};

function submitDeleteRuta(idRol, idRuta) {
  // console.log("Hola submitDelete");

  document.getElementById("delete_idRol").value = idRol;
  document.getElementById("delete_idRuta").value = idRuta;
  document.getElementById("deleteRutaForm").submit();
}

function confirmarFormCreacionAutomaticaProgramacion() {
  document.getElementById("formCreacionAutomaticaProgramacion").submit();
}

async function confirmarFormCerrarProgramacion() {
  const selectElaboradoPor = document.getElementById("elaborado_por");
  const estadoLabel = document.querySelector(".estado-data__programacion");
  const btn = document.querySelector(".btn-cerrar__programacion button");

  const idProgramacion = document.querySelector(
    "input[name='idProgramacion']",
  ).value;

  if (!selectElaboradoPor.value) {
    alert("Seleccione quién elaboró el reporte.");
    return;
  }

  if (estadoLabel.textContent.trim() === "CERRADO") {
    alert("El reporte ya está cerrado");
    return;
  }

  if (!confirm("¿Desea cerrar la edición del reporte?")) return;

  console.log(idProgramacion);

  btn.disabled = true;
  btn.textContent = "Cerrando...";

  try {
    const response = await fetch("/json/programacion/cerrarProgramacion_json", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        idProgramacion: idProgramacion,
        elaborado_por: selectElaboradoPor.value,
        cerrado_por: document.getElementById("input__cerrado_por").value,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Error al cerrar");
    }

    estadoLabel.textContent = "CERRADO";
    estadoLabel.style.color = "lime";

    btn.textContent = "Cerrado";
    btn.classList.remove("btn-success");
    btn.classList.add("btn-secondary");

    if (window.table) {
      table.replaceData(); // vuelve a pedir datos al ajaxURL
    }
  } catch (error) {
    console.error(error);
    alert(error.message);

    btn.disabled = false;
    btn.textContent = "Cerrar reporte";
  }
}

const mostrarBotonesEliminarRol = function (btn) {
  const contenedor = btn.closest("td");
  const btnsRoles = contenedor.querySelector(".rol__form__btn");
  const btnX = contenedor.querySelector(".rol__btn-delete");

  // console.log(btnsRoles);

  btnX.style.display = "none";
  btnsRoles.style.display = "flex";
};

const cancelarEliminarRol = function (btn) {
  const contenedor = btn.closest("td");
  const btnsRoles = contenedor.querySelector(".rol__form__btn");
  const btnX = contenedor.querySelector(".rol__btn-delete");

  // console.log(btnsRoles);

  btnX.style.display = "";
  btnsRoles.style.display = "none";
};

function submitDeleteRol(idUsuario, idRol) {
  // console.log("Hola submitDelete");

  document.getElementById("delete_idUsuario").value = idUsuario;
  document.getElementById("delete_idRol").value = idRol;
  document.getElementById("deleteRolForm").submit();
}

const mostrarBotonesEliminarPermiso = function (btn) {
  const contenedor = btn.closest("td");
  const btnsPermisos = contenedor.querySelector(".permiso__form__btn");
  const btnX = contenedor.querySelector(".permiso__btn-delete");

  // console.log(btnsPermisos);

  btnX.style.display = "none";
  btnsPermisos.style.display = "flex";
};

const cancelarEliminarPermiso = function (btn) {
  const contenedor = btn.closest("td");
  const btnsPermisos = contenedor.querySelector(".permiso__form__btn");
  const btnX = contenedor.querySelector(".permiso__btn-delete");

  // console.log(btnsPermisos);

  btnX.style.display = "";
  btnsPermisos.style.display = "none";
};

function submitDeletePermiso(idUsuario, idPermiso) {
  // console.log("Hola submitDelete");

  document.getElementById("delete_idUsuarioP").value = idUsuario;
  document.getElementById("delete_idPermiso").value = idPermiso;
  document.getElementById("deletePermisoForm").submit();
}

function submitDeletePermisoRol(idRol, idPermiso) {
  // console.log("Hola submitDelete");

  document.getElementById("delete_idRolP").value = idRol;
  document.getElementById("delete_idPermiso").value = idPermiso;
  document.getElementById("deletePermisoForm").submit();
}

const mostrarBotonesEliminarDepartamento = function (btn) {
  const contenedor = btn.closest("td");
  const btnsDepartamentos = contenedor.querySelector(
    ".departamento__form__btn",
  );
  const btnX = contenedor.querySelector(".departamento__btn-delete");

  btnX.style.display = "none";
  btnsDepartamentos.style.display = "flex";
};

const cancelarEliminarDepartamento = function (btn) {
  const contenedor = btn.closest("td");
  const btnsDepartamentos = contenedor.querySelector(
    ".departamento__form__btn",
  );
  const btnX = contenedor.querySelector(".departamento__btn-delete");

  btnX.style.display = "";
  btnsDepartamentos.style.display = "none";
};

function submitDeleteDepartamento(idUsuario, idDepartment) {
  // console.log("Hola submitDelete");

  document.getElementById("delete_idUsuarioD").value = idUsuario;
  document.getElementById("delete_idDepartment").value = idDepartment;
  document.getElementById("deleteDepartamentoForm").submit();
}
