let modal = null;


const openModal = function (e){
    e.preventDefault();
    const modal_id = e.target.getAttribute("href");
    const target = document.getElementById(modal_id);
    target.style.display = null;
    modal = target;
    modal.addEventListener("click", closeModal)
    modal.querySelector(".js-modal-close").addEventListener("click", closeModal);
    modal.querySelector(".js-modal-stop").addEventListener("click", stopPropagation);

};


const closeModal = function (e){
    if (modal === null) return;
    e.preventDefault();
    modal.style.display = "none";
    modal.removeEventListener("click", closeModal);
    modal.querySelector(".js-modal-close").removeEventListener("click", closeModal);
    modal.querySelector(".js-modal-stop").removeEventListener("click", stopPropagation);

    modal = null;

};

const stopPropagation = function (e) {
    e.stopPropagation();
};

{
    console.log("start js")
    // prepare Modal
    modalLinks =document.getElementsByClassName("js-modal");
    for (const a of modalLinks){
        a.addEventListener("click", openModal);
    }

    window.addEventListener("keydown", function (e) {
        if (e.key === "Escape" || e.key === "Esc"){
            closeModal(e)
        }
    })
}


