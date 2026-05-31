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


const modal = document.querySelector(".modal");


function showModal() {
    modal.classList.add("show");
    title.textContent = "Скачивание началось";
    loaderBar.style.display = "block";
}


function hideModal() {
    modal.classList.remove("show");
}

const title = document.querySelector(".modal-title");
const loaderBar = document.querySelector(".loader-bar");


function showError(errorText = "Что-то пошло не так") {
    title.textContent = "Произошла ошибка";
    console.error(`Ошибка: ${errorText}`)

    modal.classList.add("show");

    loaderBar.style.display = "none";

    setTimeout(() => {
        modal.classList.remove("show");
        loaderBar.style.display = "block";
    }, 10000);
}


const btn = document.getElementById("dwn");

btn.addEventListener("click", () => {
    const inp = document.getElementById("inp_url");
    const url = inp.value;

    const formatText = document.getElementById("formatText");
    const quality = formatText.textContent;

    console.log(url, quality);

    eel.prepare_download(url, quality)(function(res) {

        if (!res.success) {
            error_url();
            return;
        }

        showModal();

        eel.download_video(url, quality)(function(result) {

            if (result) {
                title.textContent = "Видео успешно скачано!";
                loaderBar.style.display = "none";

                setTimeout(() => {
                    hideModal();
                }, 10000);
            }

            if (!result.success) {
                showError(result.error || "Ошибка загрузки");
                return;
            }
        });
    });
});


function error_url(state) {
    let inp = document.getElementById("inp_url");

    inp.classList.toggle("error", !state);
}