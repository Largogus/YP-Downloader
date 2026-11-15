window.addEventListener('DOMContentLoaded', () => {
    window.resizeTo(1000, 610);


    const combo = document.querySelector(".combo");
    const selected = combo.querySelector(".combo-selected");
    const items = combo.querySelectorAll(".combo-item");
    const text = document.getElementById("formatText");
    const text1 = document.getElementById("formatText1");

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


    //function showSettings() {
    //    settings.classList.add("show");
    //    title.textContent = "Настройки";
    //}


    //function hideSettings() {
    //    settings.classList.remove("show");
    //}


    function hideModal() {
        modal.classList.remove("show");
    }

    const title = document.querySelector(".modal-title");
    const sidetitle = document.getElementById("side-title");
    const loaderBar = document.querySelector(".loader-bar");


    function showError(errorText = "Что-то пошло не так") {
        title.textContent = "Произошла ошибка";
        sidetitle.textContent = errorText;
        sidetitle.style.display = 'block';

        console.error(`Ошибка: ${errorText}`)

        modal.classList.add("show");

        loaderBar.style.display = "none";

        setTimeout(() => {
            modal.classList.remove("show");
            sidetitle.style.display = 'none';
            loaderBar.style.display = "block";
        }, 10000);
    }


    const btn = document.getElementById("dwn");
//    const sett_btn = document.getElementById("sett");

//    sett_btn.addEventListener("click", () => {
//        showSettings();
//    });

    btn.addEventListener("click", () => {
        const inp = document.getElementById("inp_url");
        const url = inp.value;

        const formatText = document.getElementById("formatText");
        const quality = formatText.textContent;

        console.log(url, quality);

        eel.prepare_download(url, quality)(function(res) {

            error_url(res.success);

            if (!res.success) {
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

    document.getElementById("side-title").addEventListener('click', function(event) {
      navigator.clipboard.writeText(sidetitle.textContent);
      showToast()
    });

    function showToast() {
        const toast = document.getElementById("toast");
        toast.textContent = toast.textContent;
        toast.classList.add("show");

        setTimeout(() => {
            toast.classList.remove("show");
        }, 1000);
    }

    const rept = document.getElementById("rept")
    const p = document.querySelectorAll("p")

    rept.addEventListener('click', function() {
        eel.open_tab(rept.getAttribute("link"))
    })

    p.forEach(i => {
        i.onclick = () => {
            eel.open_tab(i.getAttribute("link"))
        };
    });

});