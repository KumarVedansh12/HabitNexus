document.querySelectorAll(".stat-card")
.forEach(card => {

    card.addEventListener("mouseenter", () => {
        card.style.transform =
            "translateY(-8px) scale(1.03)";
    });

    card.addEventListener("mouseleave", () => {
        card.style.transform =
            "translateY(0) scale(1)";
    });

});