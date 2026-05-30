window.addEventListener('DOMContentLoaded', () => {
    window.resizeTo(1000, 455);
});


const combo = document.querySelector(".combo");
const selected = document.querySelector(".combo-selected");
const items = document.querySelectorAll(".combo-item");
const text = document.getElementById("formatText");

selected.onclick = () => {
    combo.classList.toggle("open");
};

items.forEach(item => {
    item.onclick = () => {

        items.forEach(i => i.classList.remove("active"));
        item.classList.add("active");

        text.textContent = item.textContent;

        combo.classList.remove("open");
    };
});

const modal = document.getElementById("modal");

eel.expose(showModal);

function showModal() {
    modal.classList.add("show");
}

eel.expose(hideModal);

function hideModal() {
    modal.classList.remove("show");
}

eel.expose(showError);

function showError(errorText = "Что-то пошло не так") {
    title.textContent = "Произошла ошибка";
    subtitle.textContent = errorText;

    modal.classList.add("show");

    document.querySelector(".loader-bar").style.display = "none";

    setTimeout(() => {
        modal.classList.remove("show");
        document.querySelector(".loader-bar").style.display = "block";
    }, 2500);
}


const btn = document.getElementById("dwn");

btn.addEventListener("click", () => {
    let inp = document.getElementById("inp_url");
    let info = inp.value
    let format = document.getElementById("formatText").textContent;
    eel.download_video(info, format)
    console.log(info, format)
})


eel.expose(error_url);

function error_url(state) {
    let inp = document.getElementById("inp_url");

    inp.classList.toggle("error", !state);
}