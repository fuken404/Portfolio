document.addEventListener("DOMContentLoaded", () => {
  const trigger = document.getElementById("umb");

  trigger.addEventListener("click", () => {
    Swal.fire({
      title: 'Ingeniero de Software',
      html: '<p style="font-size: 1.2rem;">Pte. por culminar</p>',
      icon: 'info',
      showCloseButton: true,
      showConfirmButton: false,
    });
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const trigger = document.getElementById("sena");

  trigger.addEventListener("click", () => {
    Swal.fire({
      title: 'Técnico en Sistemas',
      html: `
        <iframe src="./resources/certs/sena.pdf" 
                width="100%" 
                height="500px" 
                style="border: none;"></iframe>
      `,
      showCloseButton: true,
      showConfirmButton: false,
      width: '80%',
      padding: '1rem',
    });
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const trigger = document.getElementById("mintic");

  trigger.addEventListener("click", () => {
    Swal.fire({
      title: 'Desarrollador',
      html: `
        <iframe src="./resources/certs/mintic.pdf" 
                width="100%" 
                height="500px" 
                style="border: none;"></iframe>
      `,
      showCloseButton: true,
      showConfirmButton: false,
      width: '80%',
      padding: '1rem',
    });
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const trigger = document.getElementById("scrum");

  trigger.addEventListener("click", () => {
    Swal.fire({
      title: 'Fundamentos de Scrum',
      html: `
        <iframe src="./resources/certs/scrum.pdf" 
                width="100%" 
                height="500px" 
                style="border: none;"></iframe>
      `,
      showCloseButton: true,
      showConfirmButton: false,
      width: '80%',
      padding: '1rem',
    });
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const trigger = document.getElementById("infra2");

  trigger.addEventListener("click", () => {
    Swal.fire({
      title: 'Infraestructura 2',
      html: `
        <iframe src="./resources/certs/infra2.pdf" 
                width="100%" 
                height="500px" 
                style="border: none;"></iframe>
      `,
      showCloseButton: true,
      showConfirmButton: false,
      width: '80%',
      padding: '1rem',
    });
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const trigger = document.getElementById("infra1");

  trigger.addEventListener("click", () => {
    Swal.fire({
      title: 'Infraestructura 1',
      html: `
        <iframe src="./resources/certs/infra1.pdf" 
                width="100%" 
                height="500px" 
                style="border: none;"></iframe>
      `,
      showCloseButton: true,
      showConfirmButton: false,
      width: '80%',
      padding: '1rem',
    });
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const trigger = document.getElementById("linux");

  trigger.addEventListener("click", () => {
    Swal.fire({
      title: 'Linux',
      html: `
        <iframe src="./resources/certs/linux.pdf" 
                width="100%" 
                height="500px" 
                style="border: none;"></iframe>
      `,
      showCloseButton: true,
      showConfirmButton: false,
      width: '80%',
      padding: '1rem',
    });
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const trigger = document.getElementById("python");

  trigger.addEventListener("click", () => {
    Swal.fire({
      title: 'Python',
      html: `
        <iframe src="./resources/certs/python.pdf" 
                width="100%" 
                height="500px" 
                style="border: none;"></iframe>
      `,
      showCloseButton: true,
      showConfirmButton: false,
      width: '80%',
      padding: '1rem',
    });
  });
});